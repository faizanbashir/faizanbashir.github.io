---
layout: post
comments: true
current: post
cover: assets/images/posts/mika-korhonen-XJUQB4UAObQ-unsplash.jpg
navigation: True
title: "How to detect CrashLoopBackOff Pods in Kubernetes using Golang SDK"
date: 2023-01-03 10:00:00
tags: [Kubernetes]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: This article will walk the user through the process of detecting CrashLoopBackOff Pods in Kubernetes using Golang client SDK.
---

This article will walk the user through the process of detecting CrashLoopBackOff Pods in the Kubernetes cluster with the help of [go-client sdk](https://github.com/kubernetes/client-go/).

Kubernetes has a powerful, well-designed API to interact with the cluster functionality. We can list, create, update, delete, and watch all kinds of Kubernetes resources using the Kubernetes APIs. In addition, we can do anything that we can do with the `kubectl` command line interface with the APIs. 

To make things easier for developers who want to extend and leverage the functionality provided by Kubernetes, the community has provided Software Development Kits for all major programming languages like `python`, `golang`, `dotnet`, `javascript`, and `C`. You can check out the entire list of supported languages [here](https://kubernetes.io/docs/reference/using-api/client-libraries/).

***
# Table of Contents:

* [Communicating with the Kubernetes API server](#communicating-with-the-kubernetes-api-server)
* [Creating a client to communicate with the Kubernetes API server](#creating-a-client-to-communicate-with-the-kubernetes-api-server)
* [Detecting CrashLoopBackOff Pods in Kubernetes](#detecting-crashloopbackoff-pods-in-kubernetes)
* [Assembling the Pieces](#assembling-the-pieces)
* [Installing the Dependencies and Testing](#installing-the-dependencies-and-testing)
* [Conclusion](#conclusion)

***

## Communicating with the Kubernetes API server

There are two ways of communicating with the Kubernetes API server using the go-client SDK:

1. Using the [in-client cluster communication](https://github.com/kubernetes/client-go/blob/master/examples/in-cluster-client-configuration/main.go). For this to work out, the code needs to be running inside a Kubernetes Pods, and it should have access to execute the required functionality like creating/deleting Pods via a service account.
2. Using the [out-of-cluster client configuration](https://github.com/kubernetes/client-go/blob/master/examples/out-of-cluster-client-configuration/main.go). This generally works when we are performing development in the local machine, outside of a Kubernetes cluster. However, we need a Kubernetes cluster to perform these actions using the code, like creating/deleting Pods. 

In this setup, we will communicate with the K8s API server from outside the cluster. This configuration is called [out-of-cluster client configuration](https://github.com/kubernetes/client-go/blob/master/examples/out-of-cluster-client-configuration/main.go). In this method, the SDK communicates with the Kubernetes API server using the configuration provided the current context in the local `kubeconfig` file generally stored in the location `~/.kube/config`.

## Creating a client to communicate with the Kubernetes API server

Kubernetes go-client SDK provides functionality to create a client to talk with the Kubernetes API server. Using this client, we use functionality like listing Pods and Namespaces. So let's dive right in. We will explain the stuff as we go ahead.

{% highlight golang %}
package main

import (
    "fmt"
    "os"
    "path/filepath"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/tools/clientcmd"
)

func main() {
    userHomeDir, err := os.UserHomeDir()
    if err != nil {
        fmt.Printf("error getting user home dir: %v\n", err)
        os.Exit(1)
    }
    kubeConfigPath := filepath.Join(userHomeDir, ".kube", "config")
    fmt.Printf("Using kubeconfig: %s\n", kubeConfigPath)

    kubeConfig, err := clientcmd.BuildConfigFromFlags("", kubeConfigPath)
    if err != nil {
        fmt.Printf("Error getting kubernetes config: %v\n", err)
        os.Exit(1)
    }

    clientset, err := kubernetes.NewForConfig(kubeConfig)

    if err != nil {
        fmt.Printf("error getting kubernetes config: %v\n", err)
        os.Exit(1)
    }
}
{% endhighlight %}

In the code snippet, we get the user's home directory using the function `os.UserHomeDir()` and then acquire the path to the `~/.kube/config` file. We then pass the `kubeConfigPath` to the `clientcmd.BuildConfigFromFlags()` function, which returns a `kubeconfig` object next up calling the `kubernetes.NewForConfig(kubeConfig)` returns us the `clientset`, and an error object. If the `err` is `nil`, we have the client object, which we will use further to detect crashing Pods in the following sections.

## Detecting CrashLoopBackOff Pods in Kubernetes

To detect `CrashLoopBackOff` Pods in Kubernetes, we will create a Pod `watcher` object and check the Pods for the crashing condition. So let's dive right into the code:

{% highlight golang %}
    ...
    // Empty string for all namespaces
    namespace := ""
    fmt.Println("Watch Kubernetes Pods in CrashLoopBackOff state")
    watcher, err := client.CoreV1().Pods(namespace).Watch(context.Background(), metav1.ListOptions{})
    if err != nil {
        fmt.Printf("error create pod watcher: %v\n", err)
        return
    }

    for event := range watcher.ResultChan() {
        pod, ok := event.Object.(*corev1.Pod)
        if !ok {
            continue
        }
        for _, c := range pod.Status.ContainerStatuses {
            if c.State.Waiting != nil && c.State.Waiting.Reason == "CrashLoopBackOff" {
                fmt.Printf("PodName: %s, Namespace: %s, Phase: %s\n", pod.ObjectMeta.Name, pod.ObjectMeta.Namespace, pod.Status.Phase)
            }
        }
    }
    ...
{% endhighlight %}

In the above code sample, we get a `watcher` object by making a call to the `Watch()` function of the `CoreV1().Pods()` object. The `Watch()` function returns a `watcher` and an `err` object with the error message. Next up, we iterate through the `watcher.ResultChan()` method using a `for` loop. The above is not an infinite loop, as the Channel can timeout. To create a control loop, we can encase the existing `for` loop in an endless `for {}` loop. But, doing so will put a lot of load on the API Server, so using a watcher is not recommended. 

We can convert the `event` object to a Pod object using the `event.Object.(*corev1.Pod)`, which returns a `pod` and `ok`. The `ok` is `true` if the conversion was successful. To determine the crashing loop, we will iterate through the `pod.Status.ContainerStatuses`. First, we will check if the container is waiting using the `c.State.Waiting != nil`. Next up, we will check if the reason for the Waiting state of the container is `CrashLoopBackOff` using the `c.State.Waiting.Reason == "CrashLoopBackOff"`. If both conditions are true, we have found a Pod in the `CrashLoopBackOff` state.

## Assembling the Pieces

After putting all the pieces together, we have a `main.go` file containing all the code we discussed previously. Secondly, we have a `go.mod` file containing the dependencies, in this case, `k8s.io/apimachinery`, `k8s.io/api/` and `k8s.io/client-go`.

{% gist 7e912afe15effe058394e0a11148f498 %}

# Installing the Dependencies and Testing

We are using the go version `1.19`. To install the dependencies, we need to run the following command:

{% highlight shell %}
$ go mod tidy
{% endhighlight %}

We can run the code using the below command:

{% highlight shell %}
$ go run ./main.go
{% endhighlight %}

Before running the code, ensure you can access the target Kubernetes cluster using `kubectl`. The `kubeconfig` file should be in the user's home `.kube` folder for the setup to work as expected.

# Conclusion

The Kubernetes SDK allows us to leverage and extend Kubernetes depending on our use cases. For example, we can leverage the power of the Kubernetes SDK by in-cluster client communication. This way, the code is executed inside the Kubernetes cluster in a Pod where we can provide a granular level of access using a service account with proper permissions. The client-go Kubernetes SDK is written in golang, just like the Kubernetes container orchestration platform and provides native integration with Kubernetes.