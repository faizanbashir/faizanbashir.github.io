---
layout: post
comments: true
current: post
cover: assets/images/posts/adam-chang-IWenq-4JHqo-unsplash.jpg
navigation: True
title: "How to Create Update Scale List Get and Delete a Deployment using Kubernetes Golang SDK"
date: 2023-02-05 10:00:00
tags: [Kubernetes]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: This article will walk the user through the process of Creating, Updating, Scaling, Listing, Getting and Deleting Deployment in a Kubernetes cluster with the help of Kubernetes Golang client SDK.
---

# Introduction

This article will walk the user through the process of Creating, Updating, Scaling, Listing, Getting and Deleting Deployment in a Kubernetes cluster with the help of Kubernetes [golang client SDK](https://github.com/kubernetes/client-go).

***
# Table of Contents:

* [Creating a client to communicate with the Kubernetes API Server](#creating-a-client-to-communicate-with-the-kubernetes-api-server)
* [Creating Deployment](#creating-deployment)
    * [Walk through the Deployment object](#walk-through-the-deployment-object)
    * [Using the Deployment object to create a Deployment](#using-the-deployment-object-to-create-a-deployment)
* [Get Deployment](#get-deployment)
* [Listing Deployment](#listing-deployment)
* [Updating the Image of a Container in Deployment](#updating-the-image-of-a-container-in-deployment)
* [Scaling Deployment](#scaling-deployment)
* [Deleting Deployment](#deleting-deployment)
* [Assembling the Pieces](#assembling-the-pieces)
* [Installing the Dependencies and Testing](#installing-the-dependencies-and-testing)
* [Conclusion](#conclusion)

***

## Creating a client to communicate with the Kubernetes API Server

Kubernetes provides a golang SDK to access the API Server programmatically. We can learn more about communicating with the Kubernetes API Server using go-client SDK [in this article](https://faizanbashir.me/how-to-list-kubernetes-pods-using-golang-sdk#communicating-with-the-kubernetes-api-server).

To perform the operations on Kubernetes Deployments, we need to create a client that will interact with the API Server. We will use the Kubernetes SDK to interact with the `kubeconfig` file and exposes functionality to create a client. Let's dive right into the code. We will explain the stuff as we go ahead.

{% highlight golang %}
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "os"
    "path/filepath"

    appsv1 "k8s.io/api/apps/v1"
    apiv1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    types "k8s.io/apimachinery/pkg/types"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/tools/clientcmd"
)

type K8sClient struct {
    Client kubernetes.Interface
}

func getK8sClient() *K8sClient {
    userHomeDir, err := os.UserHomeDir()
    if err != nil {
        fmt.Printf("error getting user home dir: %v\n", err)
        os.Exit(1)
    }
    kubeConfigPath := filepath.Join(userHomeDir, ".kube", "config")
    fmt.Printf("Using kubeconfig: %s\n", kubeConfigPath)

    kubeConfig, err := clientcmd.BuildConfigFromFlags("", kubeConfigPath)
    if err != nil {
        err := fmt.Errorf("Error getting kubernetes config: %v\n", err)
        log.Fatal(err.Error)
    }
    client, err := kubernetes.NewForConfig(kubeConfig)
    if err != nil {
        err := fmt.Errorf("error getting kubernetes config: %v\n", err)
        log.Fatal(err.Error)
    }

    fmt.Printf("%T\n", client)
    return &K8sClient{
        Client: client,
    }
}

func main() {
    client := getK8sClient()
}
{% endhighlight %}

In the code snippet, we have created a function `getK8sClient()`, which returns a pointer to the `K8sClient` struct. The `K8sClient` struct has a `Client` of type `kubernetes.Interface`, which is the type of the Kubernetes client. We can use this to create method sets when performing operations on the Deployment.

In the code snippet, we get the user's home directory using the function `os.UserHomeDir()` and then acquire the path to the `~/.kube/config` file. We then pass the `kubeConfigPath` to the `clientcmd.BuildConfigFromFlags()` function, which returns a `kubeconfig` object. Next, we pass the `kubeconfig` to the `kubernetes.NewForConfig()` function to obtain the kubernetes `client`. Finally, we return the `K8sClient` with the kubernetes client we will use to perform operations on Deployments.

## Creating Deployment

In the previous section, we created a Kubernetes client. Now we will be using it to perform actions on the Kubernetes resources. For example, this section will use the client to develop Kubernetes Deployment. But first, let's review the Deployment object.

### Walk through the Deployment object

The Kubernetes go client SDK provides a `Create` function to create Deployment. The procedure takes multiple parameters, one of which we will explain in this section: the Deployment object. First, let's walk through the Deployment object.

{% highlight golang %}
...
    deploymentObject := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name: name,
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: int32Ptr(replicas),
            Selector: &metav1.LabelSelector{
                MatchLabels: map[string]string{
                    "app": name,
                },
            },
            Template: apiv1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: map[string]string{
                        "app": name,
                    },
                },
                Spec: apiv1.PodSpec{
                    Containers: []apiv1.Container{
                        {
                            Name:  "web",
                            Image: image,
                            Ports: []apiv1.ContainerPort{
                                {
                                    Name:          "http",
                                    Protocol:      apiv1.ProtocolTCP,
                                    ContainerPort: 80,
                                },
                            },
                        },
                    },
                },
            },
        },
    }
..
{% endhighlight %}

Here in the `&appsv1.Deployment{...}` struct, we pass the intended name of the Deployment in the `metav1.ObjectMeta` struct. Under the `appsv1.DeploymentSpec` struct, we provide the `Replicas` count and `Selector` map. The `Template` uses the `&corev1.PodTemplateSpec` struct defined in the Kubernetes `k8s.io/api/core/v1`. It has a Label map which should be the same as the `Selector` mentioned earlier. The `corev1.PodSpec` struct contains the `[]corev1.Container` struct, which is an array as we can have multiple containers running inside a Pod. Further, we have the `Name`, `Image` and `Ports` related to a container. The `[]corev1.ContainerPort` struct is an array as we can expose multiple ports in our Pod.

### Using the Deployment object to create a Deployment

Now that we have deconstructed the Deployment struct let's go through the `CreateDeployment()` function.

{% highlight go %}

func (c *K8sClient) CreateDeployment(name, namespace, image string, replicas int32) error {
    deploymentObject := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name: name,
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: int32Ptr(replicas),
            Selector: &metav1.LabelSelector{
                MatchLabels: map[string]string{
                    "app": name,
                },
            },
            Template: apiv1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: map[string]string{
                        "app": name,
                    },
                },
                Spec: apiv1.PodSpec{
                    Containers: []apiv1.Container{
                        {
                            Name:  "web",
                            Image: image,
                            Ports: []apiv1.ContainerPort{
                                {
                                    Name:          "http",
                                    Protocol:      apiv1.ProtocolTCP,
                                    ContainerPort: 80,
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    // Create Deployment
    fmt.Println("Creating deployment...")
    result, err := c.Client.AppsV1().Deployments(namespace).Create(context.TODO(), deploymentObject, metav1.CreateOptions{})
    if err != nil {
        return err
    }
    fmt.Printf("Created deployment %q.\n", result.GetName())
    return nil
}

{% endhighlight %}

The `CreateDeploymentConfig()` function receives parameters like the `name` of the Deployment and the `namespace` we need to create the Deployment. The container `image` to be used for the Container, the number of `replicas` that the Deployment should create. The Kubernetes `client` is passed in as the method set `(c *K8sClient)` for interacting with the Kubernetes cluster. Finally, the function returns an `error`, which is `nil` in case the DeploymentConfig gets created.

The `Create()` function takes in a `context`, the `*v1.DeploymentConfig` struct and the `metav1.CreateOptions{}`. It returns an error and a `*v1.DeploymentConfig` struct for the created DeploymentConfig. We will return with an `error` if there is any error while creating the DeploymentConfig. Else, we return with a `nil`.

Using the code below, we can call the `CreateDeployment()` function from the `main()`.

{% highlight golang %}
...
    deploymentName := "<deployment_name>"
    namespace := "<namespace_name>"
    // Creating a new Deployment
    image := "docker.io/httpd:latest"
    err := client.CreateDeployment(deploymentName, namespace, image, 1)
    if err != nil {
        log.Fatal(err)
    }
...
{% endhighlight %}

## Get Deployment

Now that we can create a Deployment using the SDK let's try to get the Deployment we just deployed. This section will use the Kubernetes client to run the Deployment in a namespace. So first, let's go through the function `GetDeployment()`.

{% highlight golang %}

func (c *K8sClient) GetDeployment(name, namespace string) (*appsv1.Deployment, error) {
    fmt.Println("Get Deployment in namespace", namespace)
    result, err := c.Client.AppsV1().Deployments(namespace).Get(context.TODO(), name, metav1.GetOptions{})

    if err != nil {
        fmt.Printf("Failed to getting Deployment: %v\n", err)
        return nil, err
    }
    return result, nil
}

{% endhighlight %}

The `ListDeployment()` receives one argument, the `namespace`, and a pointer to the Kubernetes `client` is passed in the method set. The function returns two parameters `*appsv1.DeploymentList` and `error`.

We can call the `GetDeployment()` function from the `main()` and get the `*appsv1.Deployment` using the following code.

{% highlight golang %}
...
    // Get a deployment
    deployment, err := client.GetDeployment(deploymentName, namespace)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("%v\n", deployment)
...
{% endhighlight %}

## Listing Deployment

Now that we can create a Deployment using the SDK, let's try to list them for a given namespace. This section will use the Kubernetes client to list Deployment running in a namespace. So first, let's go through the function `ListDeployment()`.

{% highlight golang %}

func (c *K8sClient) ListDeployment(namespace string) (*appsv1.DeploymentList, error) {
    fmt.Println("List Deployments")
    deployments, err := c.Client.AppsV1().Deployments(namespace).List(context.Background(), metav1.ListOptions{})
    if err != nil {
        fmt.Printf("error listing deployments: %v\n", err)
        return nil, err
    }
    return deployments, nil
}

{% endhighlight %}

The `ListDeployment()` receives one argument, the `namespace`, and a pointer to the Kubernetes `client` is passed in the method set. The function returns two parameters `*appsv1.DeploymentList` and `error`.

We can call the `ListDeployment()` function from the `main()` and iterate over the `*appsv1.DeploymentList` array using the following code.

{% highlight golang %}
...
    // Listing Deployment
    deployment, err := client.ListDeployment(namespace)
    if err != nil {
        log.Fatal(err)
    }
    for _, d := range deployment.Items {
        fmt.Printf("%s\n", d.ObjectMeta.Name)
    }
...
{% endhighlight %}

Using a `for` loop, we can iterate over the `deployment` variable returned from the `ListDeployment()` function. In the above example, we are printing out the Deployment name using the `d.ObjectMeta.Name`. The item has all the information related to Deployment.

## Updating the Image of a Container in Deployment

We saw that using the Kubernetes SDK; we can easily create and list Deployment. Next up, we will update the image of a container in Deployment. Previously we created a Deployment with the image `docker.io/httpd:latest`. We will change that to `docker.io/nginx:latest`, an open-source web server. Finally, we will update the image with the `UpdateDeployment()` function. Let's dive right into the code.

{% highlight golang %}
func (c *K8sClient) UpdateDeployment(name, namespace, image string) {
    fmt.Printf("Updating Deployment `%s` in namespace `%s`\n", name, namespace)
    payload := []stringPatch{
        Op:    "replace",
        Path:  "/spec/template/spec/containers/0/image",
        Value: image,
    }
    payloadBytes, _ := json.Marshal(payload)

    _, err := c.Client.AppsV1().Deployments(namespace).Patch(context.TODO(), name, types.JSONPatchType, payloadBytes, metav1.PatchOptions{})
    if err != nil {
        err := fmt.Errorf("[x] Error Update Deployment Image: %v\n", err)
        panic(err)
    }

    fmt.Printf("Successfully update image for Deployment to %s\n", name)
}
{% endhighlight %}

The `UpdateDeployment()` function receives the Deployment `name`, `namespace`, and `image` to be updated. The `stringPatch` struct defines the `payload`. It consists of an `Op` referring to the `Operation`, which in this case is `replace`. The `Path` in the JSON body is where we need to perform the replace operation. The `Value` is the image name the `image` variable provides.

The `payload` is then converted into an array of bytes `payloadBytes` using the `json.Marshall()` function. Finally, the `Patch()` function uses the patch payload `payloadBytes` along with the `types.JSONPatchType`, which signifies our patch operation. The `UpdateDeployment()` is a simple function call without any return value. We can call the above function from the `main()`.

{% highlight golang %}
...
    // Updating the image for the Deployment
    client.UpdateDeployment(deploymentName, namespace, "docker.io/nginx:latest")
...
{% endhighlight %}

## Scaling Deployment

Scaling the Deployment is done through a `Patch()` function call. In addition, the SDK has a `GetScale()` and `UpdateScale()` function for getting and updating the scale of the Deployment. So let's walk through the `ScaleDeployment()` function.

{% highlight golang %}
func (c *K8sClient) ScaleDeployment(name, namespace string, replica int32) {
    scaleObj, err := c.Client.AppsV1().Deployments(namespace).GetScale(context.Background(), name, metav1.GetOptions{})
    if err != nil {
        fmt.Printf("error getting scale object: %v\n", err)
        os.Exit(1)
    }
    sd := *scaleObj
    if sd.Spec.Replicas == replica || replica < 0 {
        fmt.Printf("Deployment %s replicas %d, no changes applied\n", name, replica)
        return
    } else if sd.Spec.Replicas > replica {
        fmt.Printf("Scale down Deployment %s from %d to %d replicas\n", name, sd.Spec.Replicas, replica)
    } else {
        fmt.Printf("Scale Up Deployment %s from %d to %d replicas\n", name, sd.Spec.Replicas, replica)
    }
    sd.Spec.Replicas = replica
    scaleDeployment, err := c.Client.AppsV1().Deployments(namespace).UpdateScale(context.Background(), name, &sd, metav1.UpdateOptions{})
    if err != nil {
        fmt.Printf("error updating scale object: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("Successfully scaled deployment %s to %d replicas", name, scaleDeployment.Spec.Replicas)
}
{% endhighlight %}

This function receives a Deployment `name`, `namespace` and the replica count denoted by the variable of `replicas`. Here the `GetScale()` function provides us with the scale object. The scale object is updated to scale the Deployment using the `sd.Spec.Replicas`. Finally, we call the `UpdateScale()` function with the revised scale object. The procedure does not return any value. We can call the above function from the `main()`.

{% highlight golang %}
...
    // Scaling Deployment
    client.ScaleDeployment(deploymentName, namespace, 1)
...
{% endhighlight %}

## Deleting Deployment

Now that we have performed all the operations in the scope of this article, we can go ahead and delete the Deployment from using the Kubernetes SDK. We have created a function `DeleteDeployment()` to perform the cleanup task. Let's review the code for this function.

{% highlight golang %}
func (c *K8sClient) DeleteDeployment(name, namespace string) error {
    fmt.Printf("Deleting Deployment `%s` in namespace `%s`\n", name, namespace)
    err := c.Client.AppsV1().Deployments(namespace).Delete(context.Background(), name, metav1.DeleteOptions{})
    if err != nil {
        err := fmt.Errorf("[x] error deleting Deployment: %v\n", err)
        return err
    }
    fmt.Printf("Successfully deleted Deployment %s\n", name)
    return nil
}
{% endhighlight %}

The `DeleteDeployment()` function receives a Deployment `name` and `namespace` and returns an `error`. The `Delete()` function call of the Kubernetes SDK does the work of deleting the Deployment. We can call the `DeleteDeployment()` function from the `main()`.

{% highlight golang %}
...
    // Deleting Deployment
    err := client.DeleteDeployment(deploymentName, namespace)
    if err != nil {
        log.Fatal(err)
    }
...
{% endhighlight %}

## Assembling the Pieces

After putting all the pieces together, we have a `main.go` file containing all the code we discussed previously. Secondly, we have a `go.mod` file containing the dependencies.

{% gist 087bfb757f2ff51e475c936bda85f131 %}

## Installing the Dependencies and Testing

We are using the go version `1.19`. To install the dependencies, we need to run the following command:

{% highlight shell %}
$ go mod tidy
{% endhighlight %}

We can run the code using the below command:

{% highlight shell %}
$ go run ./main.go
{% endhighlight %}

Before running the code, ensure you can access the target Kubernetes cluster using `kubectl`. The `kubeconfig` file should be in the user's home `.kube` folder for the setup to work as expected.

## Conclusion

The Kubernetes SDK allows us to extend Kubernetes based on our use case. We can leverage the power of the Kubernetes SDK by in-cluster client communication. This way, the code is executed inside the Kubernetes cluster in a Pod where we can provide a granular level of access using a service account with proper permissions. The level of automation we can create using the Kubernetes SDK is limited only by our imagination.