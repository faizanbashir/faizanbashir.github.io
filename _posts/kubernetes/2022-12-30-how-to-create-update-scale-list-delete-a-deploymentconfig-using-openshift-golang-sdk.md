---
layout: post
comments: true
current: post
cover: assets/images/posts/john-rodenn-castillo-rQqWOHZ96OM-unsplash.jpg
navigation: True
title: "How to Create/Update/Scale/List/Delete a DeploymentConfig using Openshift Golang SDK"
date: 2022-12-30 10:00:00
tags: [Kubernetes]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: This article will walk the user through the process of Creating, Updating, Scaling, Listing, and Deleting Openshift DeploymetConfig in an Openshift cluster with the help of Openshift golang client sdk.
---

This article will walk the user through the process of Creating, Updating, Scaling, Listing, and Deleting Openshift DeploymetConfig in an Openshift cluster with the help of [Openshift golang client sdk](https://github.com/openshift/client-go).

[Red Hat OpenShift](https://www.redhat.com/en/technologies/cloud-computing/openshift) is an enterprise-ready Kubernetes container platform. Openshift is built on top of Kubernetes and has a user-friendly UI to interact with the cluster. It has all the features of Kubernetes, along with a few elements of its own.

Openshift provides us with a deployment object called the [DeploymentConfig(DC)](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.1/html/applications/deployments), which enables us to manage the desired state for a group of Pods/ReplicationControllers. The [DeploymentConfig is similar in functionality to the Kubernetes Deployment](https://docs.openshift.com/container-platform/4.6/applications/deployments/what-deployments-are.html) object. The only difference is that DeploymentConfig is available only in Openshift. 

***
# Table of Contents:

* [Creating a client to communicate with the Openshift API Server](#creating-a-client-to-communicate-with-the-openshift-api-server)
* [Creating DeploymentConfigs](#creating-deploymentconfigs)
	* [Walk through the DeploymentConfig object](#walk-through-the-deploymentconfig-object)
	* [Using the DeploymentConfig object to create a Deployment](#using-the-deploymentconfig-object-to-create-a-deployment)
* [Listing DeploymentConfigs](#listing-deploymentconfigs)
* [Updating the Image of a Container in DeploymentConfig](#updating-the-image-of-a-container-in-deploymentconfig)
* [Scaling DeploymentConfigs](#scaling-deploymentconfigs)
* [Deleting DeploymentConfigs](#deleting-deploymentconfigs)
* [Assembling the Pieces](#assembling-the-pieces)
* [Installing the Dependencies and Testing](#installing-the-dependencies-and-testing)
* [Conclusion](#conclusion)

***

## Creating a client to communicate with the Openshift API Server

The Openshift container platform is built on top of Kubernetes and uses much of the underlying functionality. We can learn more about communicating with the Kubernetes API Server using go-client SDK [in this article](https://faizanbashir.me/how-to-list-kubernetes-pods-using-golang-sdk#communicating-with-the-kubernetes-api-server).

To perform the operations on Openshift DeploymentConfigs, we need to create a client that will interact with the API Server. Openshift uses the Kubernetes SDK to interact with the `kubeconfig` file and exposes functionality to create a client. Let's dive right into the code. We will explain the stuff as we go ahead.

{% highlight golang %}
package main

import (
    "fmt"
    "os"
    "log"
    "path/filepath"
    v1 "github.com/openshift/client-go/apps/clientset/versioned/typed/apps/v1"
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
        err := fmt.Errorf("Error getting kubernetes config: %v\n", err)
        log.Fatal(err.Error)
    }
    client, err := v1.NewForConfig(kubeConfig)
    fmt.Printf("%T\n", client)

    if err != nil {
        err := fmt.Errorf("error getting kubernetes config: %v\n", err)
        log.Fatal(err.Error)
    }
}
{% endhighlight %}

In the code snippet, we get the user's home directory using the function `os.UserHomeDir()` and then acquire the path to the `~/.kube/config` file. We then pass the `kubeConfigPath` to the `clientcmd.BuildConfigFromFlags()` function, which returns a `kubeconfig` object. Finally, to get the openshift `appsv1` client, we invoke the `v1.NewForConfig()` function of the Openshift client-go SDK, passing it to the `kubeConfig` object. 

**Note:** The `v1` in the `v1.NewForConfig()` returns a `*v1.AppsV1Client`; this is part of the `appsv1`, but since we are using the DeploymentConfig object further in this tutorial which is also a part of the `appsv1` group, we ended up using the `appsv1` for the later. While both the `v1` and `appsv1` referred to in this code fall under the Openshift `appsv1`.

## Creating DeploymentConfigs

In the previous section, we created an Openshift client. Now we will be using it to perform actions on the Openshift resources. For example, this section will use the client to create Openshift DeploymentConfig. But first, let's review the DeploymentConfig object.

### Walk through the DeploymentConfig object

The Openshift go client SDK provides a `Create` function to create DeploymentConfigs. The procedure takes multiple parameters, one of which we will explain in this section: the DeploymentConfig object. First, let's walk through the DeploymentConfig object.

{% highlight golang %}
...
    dc := &appsv1.DeploymentConfig{
        ObjectMeta: metav1.ObjectMeta{
            Name: name,
        },
        Spec: appsv1.DeploymentConfigSpec{
            Replicas: replicas,
            Selector: map[string]string{
                "app": name,
            },
            Template: &corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: map[string]string{
                        "app": name,
                    },
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{
                        {
                            Name:  name,
                            Image: image,
                            Ports: []corev1.ContainerPort{
                                {
                                    ContainerPort: 8080,
                                    Protocol:      corev1.ProtocolTCP,
                                },
                            },
                        },
                    },
                },
            },
            Triggers: []appsv1.DeploymentTriggerPolicy{
                {
                    Type: appsv1.DeploymentTriggerOnConfigChange,
                },
            },
        },
    }
..
{% endhighlight %}

Here in the `&appsv1.DeploymentConfig{...}` struct, we pass the intended name of the DeploymentConfig in the `metav1.ObjectMeta` struct. Under the `appsv1.DeploymentConfigSpec` struct, we provide the `Replicas` count and `Selector` map. The `Template` uses the `&corev1.PodTemplateSpec` struct  defined in the Kubernetes `k8s.io/api/core/v1`. It has a Label map which should be the same as the `Selector` mentioned earlier. The `corev1.PodSpec` struct contains the `[]corev1.Container` struct which is an array as we can have multiple containers running inside a Pod. Further, we have the `Name`, `Image` and `Ports` related to a container. The `[]corev1.ContainerPort` struct is an array as we can expose multiple ports in our Pod.  

We can define multiple `Triggers` using the `[]appsv1.DeploymentTriggerPolicy` struct. In this case, we are using the trigger type `appsv1.DeploymentTriggerOnConfigChange`, which refers to the [ConfigChange trigger](https://docs.openshift.com/container-platform/3.11/dev_guide/deployments/basic_deployment_operations.html#config-change-trigger). The ConfigChange trigger creates a new replication controller whenever the control loop detects changes in the pod template of the deployment configuration.

### Using the DeploymentConfig object to create a Deployment

Now that we have deconstructed the DeploymentConfig struct let's go through the `CreateDeploymentConfig()` function.

{% highlight go %}

func CreateDeploymentConfig(name, namespace, image string, replicas int32, client *v1.AppsV1Client) error {
    fmt.Printf("Creating new DeploymentConfig `%s` in namespace `%s`\n", name, namespace)
    dc := &appsv1.DeploymentConfig{
        ObjectMeta: metav1.ObjectMeta{
            Name: name,
        },
        Spec: appsv1.DeploymentConfigSpec{
            Replicas: replicas,
            Selector: map[string]string{
                "app": name,
            },
            Template: &corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: map[string]string{
                        "app": name,
                    },
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{
                        {
                            Name:  name,
                            Image: image,
                            Ports: []corev1.ContainerPort{
                                {
                                    ContainerPort: 8080,
                                    Protocol:      corev1.ProtocolTCP,
                                },
                            },
                        },
                    },
                },
            },
            Triggers: []appsv1.DeploymentTriggerPolicy{
                {
                    Type: appsv1.DeploymentTriggerOnConfigChange,
                },
            },
        },
    }
    dcObj, err := client.DeploymentConfigs(namespace).Create(context.Background(), dc, metav1.CreateOptions{})
    if err != nil {
        err := fmt.Errorf("[x] Error creating DC: %v\n", err)
        return err
    }
    fmt.Printf("Successfully created deploymentconfig to `%s` in namespace `%s`\n", dcObj.ObjectMeta.Name, namespace)
    return nil
}

{% endhighlight %}

The `CreateDeploymentConfig()` function receives parameters like the `name` of the DeploymentConfig, and the `namespace` we need to create the DeploymentConfig. The container `image` to be used for the Container, the number of `replicas` that the DeploymentConfig should create and finally, the Openshift `client` for interacting with the Openshift cluster. The function returns an `error` which is `nil` in case the DeploymentConfig gets created.

The `Create()` function takes in a `context`, the `*v1.DeploymentConfig` struct and the `metav1.CreateOptions{}`. It returns an error and a `*v1.DeploymentConfig` struct for the created DeploymentConfig. We will return with an `error` if there is any error while creating the DeploymentConfig. Else, we return with a `nil`.

Using the code below, we can call the `CreateDeploymentConfig()` function from the `main()`.

{% highlight golang %}
...
    deploymentName := "my-deployment"
    namespace := "my-namespace"

    // Creating a new DeploymentConfig
    image := "docker.io/httpd:latest"
    err = CreateDeploymentConfig(deploymentName, namespace, image, 1, client)
    if err != nil {
        log.Fatal(err)
    }
...
{% endhighlight %}

## Listing DeploymentConfigs

Now that we can create a DeploymentConfig using the SDK let's try to list them for a given namespace. This section will use the Openshift client to list DeploymentConfigs running in a namespace. So first, let's go through the function `ListDeploymentConfigs()`.

{% highlight golang %}

func ListDeploymentConfigs(namespace string, client *v1.AppsV1Client) (*appsv1.DeploymentConfigList, error) {
    fmt.Printf("Listing DeploymentConifgs in namespace `%s`\n", namespace)
    deploymentConfigs, err := client.DeploymentConfigs(namespace).List(context.Background(), metav1.ListOptions{})
    if err != nil {
        err := fmt.Errorf("[x] error listing DeploymentConfig: %v\n", err)
        return nil, err
    }
    return deploymentConfigs, nil
}

{% endhighlight %}

The `ListDeploymentConfigs()` receives two arguments, the `namespace` and the Openshift `client`. The function returns two parameters `*appsv1.DeploymentConfigList` and `error`.

We can call the `ListDeploymentConfigs()` function from the `main()` and iterate over the `*appsv1.DeploymentConfigList` array using the following code.

{% highlight golang %}
...
    // Listing deployment Configs
    deploymentConfigs, err := ListDeploymentConfigs(namespace, client)
    if err != nil {
        log.Fatal(err)
    }
    for _, d := range deploymentConfigs.Items {
        fmt.Printf("%s\n", d.ObjectMeta.Name)
    }
...
{% endhighlight %}

Using a `for` loop, we can iterate over the `deploymentConfigs` variable returned from the `ListDeploymentCofigs()` function. In the above example, we are printing out the name of the DeploymentConfig using the `d.ObjectMeta.Name`. The item has all the information related to DeploymentConfig.

## Updating the Image of a Container in DeploymentConfig 

We saw that using the Openshift SDK; we can easily create and list DeploymentConfigs. Next up, we will update the image of a container in DeploymentConfig. Previously we created a DeploymentConfig with the image `docker.io/httpd:latest`. We will change that to `docker.io/nginx:latest`, an open-source web server. Finally, we will update the image with the `UpdateDeploymentConfigImage()` function. Let's dive right into the code.

{% highlight golang %}
func UpdateDeploymentConfigImage(name, namespace, image string, client *v1.AppsV1Client) {
    fmt.Printf("Updating DeploymentConfig `%s` in namespace `%s`\n", name, namespace)
    payload := []stringPatch{
        Op:    "replace",
        Path:  "/spec/template/spec/containers/0/image",
        Value: image,
    }
    payloadBytes, _ := json.Marshal(payload)

    _, err := client.DeploymentConfigs(namespace).Patch(context.TODO(), name, types.JSONPatchType, payloadBytes, metav1.PatchOptions{})
    if err != nil {
        err := fmt.Errorf("[x] Error Update DC Image: %v\n", err)
        panic(err)
    }

    fmt.Printf("Successfully update image for deploymentconfig to %s\n", name)
}
{% endhighlight %}

The `UpdateDeploymentConfigImage()` function receives the DeploymentConfig `name`, `namespace`, and `image` to be updated and the `client`. The `integerPatch` struct defines the `payload`. It consists of an `Op` referring to the `Operation`, which in this case is `replace`. The `Path` in the JSON body is where we need to perform the replace operation. The `Value` is the image name the `image` variable provides.

The `payload` is then converted into an array of bytes `payloadBytes` using the `json.Marshall()` function. Finally, the `Patch()` function uses the patch payload `payloadBytes` along with the `types.JSONPatchType`, which signifies our patch operation. The `UpdateDeploymentConfigImage()` is a simple function call without any return value. We can call the above function from the `main()`.

{% highlight golang %}
...
    // Updating the image for DeploymentConfig
    UpdateDeploymentConfigImage(deploymentName, namespace, "docker.io/nginx:latest", client)
...
{% endhighlight %}

## Scaling DeploymentConfigs

Scaling the DeploymentConfig is done through a `Patch()` function call. Although the SDK has a `GetScale()` and `UpdateScale()` function supposedly for getting and updating the scale of the DeploymentConfig. Unfortunately, the `UpdateScale()` function returned errors and did not work for me. So let's walk through the `ScaleDeploymentConfig()` function.

{% highlight golang %}
func ScaleDeploymentConfig(name, namespace string, scale int, client *v1.AppsV1Client) {
    fmt.Printf("Scaling DeploymentConfig `%s` in namespace `%s`\n", name, namespace)
    replicas := uint32(scale)

    payload := []integerPatch{
        Op:    "replace",
        Path:  "/spec/replicas",
        Value: replicas,
    }
    payloadBytes, _ := json.Marshal(payload)

    _, err := client.DeploymentConfigs(namespace).Patch(context.TODO(), name, types.JSONPatchType, payloadBytes, metav1.PatchOptions{})
    if err != nil {
        err := fmt.Errorf("[x] Error Scaling DC Image: %v\n", err)
        panic(err)
    }

    fmt.Printf("Successfully scaled deploymentconfig to %d replicas\n", replicas)
}
{% endhighlight %}

This function receives a DeploymentConfig `name`, `namespace`, number of `scale` and the Openshift `client`. Similar to the `UpdateDeploymentConfigImage()` function, we create a `payload` to replace the `/spec/replicas` value in the DeploymentConfig. The function does not return any value. We can call the above function from the `main()`.

{% highlight golang %}
...
    // Scaling DeploymentConfig
    ScaleDeploymentConfig(deploymentName, namespace, 1, client)
...
{% endhighlight %}

## Deleting DeploymentConfigs

Now that we have performed all the operations in the scope of this article, we can go ahead and delete the DeploymentConfig from using the Openshift SDK. We have created a function `DeleteDeploymentConfig()` to perform the cleanup task. Let's review the code for this function.

{% highlight golang %}
func DeleteDeploymentConfig(name, namespace string, client *v1.AppsV1Client) error {
    fmt.Printf("Deleting DeploymentConfig `%s` in namespace `%s`\n", name, namespace)
    err := client.DeploymentConfigs(namespace).Delete(context.Background(), name, metav1.DeleteOptions{})
    if err != nil {
        err := fmt.Errorf("[x] error deleting DC: %v\n", err)
        return err
    }
    fmt.Printf("Successfully deleted deploymentconfig %s\n", name)
    return nil
}
{% endhighlight %}

The `DeleteDeploymentConfig()` function receives a DeploymentConfig `name`, `namespace` and Openshift `client` and returns an `error`. The `Delete()` function call of the Openshift SDK does the work of deleting the DeploymentConfig. We can call the `DeleteDeploymentConfig()` function from the `main()`.

{% highlight golang %}
...
    // Deleting DeploymentConfig
    err = DeleteDeploymentConfig(deploymentName, namespace, client)
    if err != nil {
        log.Fatal(err)
    }
...
{% endhighlight %}

## Assembling the Pieces

After putting all the pieces together, we have a `main.go` file containing all the code we discussed previously. Secondly, we have a `go.mod` file containing the dependencies.

{% gist 48e9e65e7c8a455318ea7b7343fa86b6 %}

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

**Note:** Instead of using the Openshift golang SDK, which pulls an outdated version, uses the code in the `master` branch, which has the latest code. There is a [GitHub issue](https://github.com/openshift/client-go/issues/134) in the Openshift client-go repo with more information on this issue.

## Conclusion

The Openshift golang SDK is similar in structure and nomenclature to the Kubernetes golang SDK. The code is open-source on [GitHub](https://github.com/openshift/client-go/). Therefore, we can go through the code and check out the functionality available in the SDK.