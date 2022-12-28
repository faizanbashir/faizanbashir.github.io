---
layout: post
comments: true
current: post
cover: assets/images/posts/andreas-gucklhorn-mawU2PoJWfU-unsplash.jpg
navigation: True
title: "How to list Kubernetes Pods using Golang SDK"
date: 2022-12-28 10:00:00
tags: [Kubernetes]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: This article will walk the user through the process of listing Pods and Namespaces in a Kubernetes cluster with the help of go-client sdk.
---

This article will walk the user through the process of listing Pods and Namespaces in a Kubernetes cluster with the help of [go-client sdk](https://github.com/kubernetes/client-go/).

Kubernetes has a powerful, well-designed API to interact with the cluster functionality. We can list, create, update, delete, and watch all kinds of Kubernetes resources using the Kubernetes APIs. In addition, we can do anything that we can do with the `kubectl` command line interface with the APIs. 

To make things easier for developers who want to extend and leverage the functionality provided by Kubernetes, the community has provided Software Development Kits for all major programming languages like `python`, `golang`, `dotnet`, `javascript`, and `c`. You can check out the entire list of supported languages [here](https://kubernetes.io/docs/reference/using-api/client-libraries/).

# Communicating with the Kubernetes API server

There are two ways of communicating with the Kubernetes API server using the go-client SDK. One way is using the [in-client cluster communication](https://github.com/kubernetes/client-go/blob/master/examples/in-cluster-client-configuration/main.go). For this to work out, the code needs to be running inside a Kubernetes Pods, and it should have access to execute the required functionality like creating/deleting Pods via a service account.

The other way is to use the configuration called [out-of-cluster client configuration](https://github.com/kubernetes/client-go/blob/master/examples/out-of-cluster-client-configuration/main.go). This generally works when we are performing development in the local machine, outside of a Kubernetes cluster. However, we need a Kubernetes cluster to perform these actions using the code, like creating/deleting Pods. 

In this setup, we will communicate with the K8s API server from outside the cluster. This configuration is called [out-of-cluster client configuration](https://github.com/kubernetes/client-go/blob/master/examples/out-of-cluster-client-configuration/main.go). In this method, the SDK communicates with the Kubernetes API server using the configuration provided the current context in the local `kubeconfig` file generally stored in the location `~/.kube/config`.

# Creating a client to communicate with the Kubernetes API server

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

In the code snippet, we get the user's home directory using the function `os.UserHomeDir()` and then acquire the path to the `~/.kube/config` file. We then pass the `kubeConfigPath` to the `clientcmd.BuildConfigFromFlags()` function, which returns a `kubeconfig` object next up calling the `kubernetes.NewForConfig(kubeConfig)` returns us the `clientset`, and an error object. If the `err` is `nil`, we have the client object, which we will use to further list Pods/Namespaces in the following sections.

# Listing Kubernetes Pods by Namespace(s)

In the previous section, we created a Kubernetes client. Now we will be using it to perform actions on the Kubernetes resources. For example, this section will use the client to list Kubernetes Pods by namespace(s). First, let's review the function we will use to list Pods.

{% highlight go %}

function ListPods(namespace string, client kubernetes.Interface) (*v1.PodList, error) {
    fmt.Println("Get Kubernetes Pods")
    pods, err := client.CoreV1().Pods(namespace).List(context.Background(), metav1.ListOptions{})
    if err != nil {
        err = fmt.Errorf("error getting pods: %v\n", err)
        return nil, err
    }
    return pods, nil
}

{% endhighlight %}

The `ListPods` function takes in a `namespace` parameter of type `string`. This variable can take the name of a namespace, or we can pass an empty string `""` to list Pods across all namespaces. The second parameter, `client`, is the Kubernetes client of type `kubernetes.Interface`. Finally, the function returns two parameters. The first is of type `*v1.PodList`, a pointer to the Pod List and an `error` data type. If there are no errors, the `error` will return a `nil`.

Next, let's see how we can call this function from the `main()` part.

{% highlight golang %}
    ...
    // An empty string returns all namespaces
    namespace := "kube-system"
    pods, err := ListPods(namespace, clientset)
    if err != nil {
        fmt.Println(err.Error)
        os.Exit(1)
    }
    for _, pod := range pods.Items {
        fmt.Printf("Pod name: %v\n", pod.Name)
    }
    var message string
    if namespace == "" {
        message = "Total Pods in all namespaces"
    } else {
        message = fmt.Sprintf("Total Pods in namespace `%s`", namespace)
    }
    fmt.Printf("%s %d\n", message, len(pods.Items))
    ...
{% endhighlight %}

The `namespace` variable holds the name of the namespace whose Pods we want to list. If we pass it an empty string, we can list all Pod across namespaces will be listed, given the user has permission to access all namespaces. Next, we check the `err` variable to see if we have any errors and exit. Since the `ListPods` function returns a list of Pods, we can iterate over this list in the `for` loop and print the name using the `pod.Name`. Finally, we are printing the number of Pods returned using the `len(pods.Items)`.

# Lisitng Kubernetes Namespaces

In the previous section, we listed the Pods for a given namespace. In this section, we will be using the Kubernetes client to list all Namespaces. So first, let's go through the function we will use to list Namespaces.

{% highlight golang %}

func ListNamespaces(client kubernetes.Interface) (*v1.NamespaceList, error) {
    fmt.Println("Get Kubernetes Namespaces")
    namespaces, err := client.CoreV1().Namespaces().List(context.Background(), metav1.ListOptions{})
    if err != nil {
        err = fmt.Errorf("error getting namespaces: %v\n", err)
        return nil, err
    }
    return namespaces, nil
}

{% endhighlight %}

The `ListNamespaes` function takes in only one parameter. The `client` is the Kubernetes client of type `kubernetes.Interface`. The function returns two parameters. The first is of type `*v1.NamespaceList`, a pointer to the NamespaceList and an `error` data type. If there are no errors, the `error` will return a `nil`.

Next, let's see how we can call this function from the `main()` part.

{% highlight golang %}
    ...
    //ListNamespaces function call returns a list of namespaces in the kubernetes cluster
    namespaces, err := ListNamespaces(clientset)
    if err != nil {
        fmt.Println(err.Error)
        os.Exit(1)
    }
    for _, namespace := range namespaces.Items {
        fmt.Println(namespace.Name)
    }
    fmt.Printf("Total namespaces: %d\n", len(namespaces.Items))
    ...
{% endhighlight %}

The `ListNamespaces()` function returns a list of Namespaces and an error `err` variable to see if we have any errors and exit. We can iterate over this list in the `for` loop and print the name using the `namespace.Name`. Finally, we are printing the number of Pods returned using the `len(namespaces.Items)`.

# Assembling the Pieces

After putting all the pieces together, we have a `main.go` file containing all the code we discussed previously. Secondly, we have a `go.mod` file containing the dependencies, in this case, `k8s.io/apimachinery` and `k8s.io/client-go`.

{% gist 1923b237212f5ebb2adf054eff2601ca %}

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

The Kubernetes SDK allows us to extend Kubernetes based on our use case. We can leverage the power of the Kubernetes SDK by in-cluster client communication. This way, the code is executed inside the Kubernetes cluster in a Pod where we can provide a granular level of access using a service account with proper permissions. The level of automation we can create using the Kubernetes SDK is limited only by our imagination.