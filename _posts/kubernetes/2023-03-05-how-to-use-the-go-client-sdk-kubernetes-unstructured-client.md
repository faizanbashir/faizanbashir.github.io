---
layout: post
comments: true
current: post
cover: assets/images/posts/rodrigo-abreu-lq9PxpwDZUk-unsplash_resized.webp
navigation: True
title: "How to Create and Delete deployment and service using the Unstructured Dynamic Client in Go"
date: 2023-03-05 10:00:00
tags: [Kubernetes, Golang]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: This article will walk the user through the process of creating and managing Kubernetes deployments and services in an Kubernetes cluster with the help of Kubernetes golang client sdk.
---

# Introduction

In this article, we will explore how to use the Go dynamic client to create and manage Kubernetes deployments and services. The unstructured client allows us to work with Kubernetes resources without having to define strong types for each resource. This can be useful when dealing with custom resources or when you want to write generic code that can handle multiple resource types.

***
# Table of Contents:

* [Set Up the Kubernetes Dynamic Client](#set-up-the-kubernetes-dynamic-client)
* [Create a deployment and service using the unstructured client](#create-a-deployment-and-service-using-the-unstructured-client)
* [Delete the created deployment and service](#delete-the-created-deployment-and-service)
* [The Main Function](#the-main-function)
* [Assembling the pieces](#assembling-the-pieces)
* [Conclusion](#conclusion)

***

# Set Up the Kubernetes Dynamic Client

The first step in working with the unstructured client is to set up a dynamic Kubernetes client. In the code snippet, we define a `K8sDynamicClient` struct with a `dynamic.Interface` field. The `dynamic.Interface` is part of the Go Kubernetes client library and allows us to work with third-party and unstructured resources.

{% highlight golang %}
type K8sDynamicClient struct {
	Client dynamic.Interface
}

func getK8sClient() *K8sDynamicClient {
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
	client, err := dynamic.NewForConfig(kubeConfig)
	if err != nil {
		err := fmt.Errorf("error getting kubernetes config: %v\n", err)
		log.Fatal(err.Error)
	}

	fmt.Printf("%T\n", client)
	return &K8sDynamicClient{
		Client: client,
	}
}
{% endhighlight %}

In the `getK8sClient` function, we build a dynamic client using the `clientcmd` package and the user's `kubeconfig` file. The `kubeconfig` file is typically found in the user's home directory under the `.kube` folder. We create an instance of the `K8sDynamicClient` struct and return it.

# Create a deployment and service using the unstructured client

To create a deployment using the unstructured client, we define the `CreateDeployment` function. This function accepts the name, namespace, image, port, and replicas for the deployment. Using the provided parameters, we create a `unstructured.Unstructured` object with the required fields and use the dynamic client to create the deployment in the specified namespace.

{% highlight golang %}
func (c *K8sDynamicClient) CreateDeployment(name, namespace, image string, port, replicas int32) {
	deploymentRes := schema.GroupVersionResource{
		Group:    "apps",
		Version:  "v1",
		Resource: "deployments",
	}

	deploymentObject := &unstructured.Unstructured{
		Object: map[string]interface{}{
			"apiVersion": "apps/v1",
			"kind":       "Deployment",
			"metadata": map[string]interface{}{
				"name": name,
			},
			"spec": map[string]interface{}{
				"replicas": replicas,
				"selector": map[string]interface{}{
					"matchLabels": map[string]interface{}{
						"app": name,
					},
				},
				"template": map[string]interface{}{
					"metadata": map[string]interface{}{
						"labels": map[string]interface{}{
							"app": name,
						},
					},
					"spec": map[string]interface{}{
						"containers": []map[string]interface{}{
							{
								"name":  name,
								"image": image,
								"ports": []map[string]interface{}{
									{
										"name":          "http",
										"protocol":      "TCP",
										"containerPort": port,
									},
								},
							},
						},
					},
				},
			},
		},
	}

	fmt.Println("Creating deployment using the unstructured object")
	deployment, err := c.Client.Resource(deploymentRes).Namespace(namespace).Create(context.TODO(), deploymentObject, metav1.CreateOptions{})
	if err != nil {
		log.Fatalf("Failed to create deploymetn: %v\n", err)
	}
	fmt.Printf("Created deployment: %s", deployment.GetName())
}

func (c *K8sDynamicClient) CreateService(name, selector, namespace string, port, targetPort int32) {
	serviceRes := schema.GroupVersionResource{
		Group:    "",
		Version:  "v1",
		Resource: "services",
	}

	serviceObject := &unstructured.Unstructured{
		Object: map[string]interface{}{
			"apiVersion": "v1",
			"kind":       "Service",
			"metadata": map[string]interface{}{
				"name": name,
			},
			"spec": map[string]interface{}{
				"selector": map[string]interface{}{
					"app": selector,
				},
				"ports": []map[string]interface{}{
					{
						"name":       "http",
						"protocol":   "TCP",
						"port":       port,
						"targetPort": targetPort,
					},
				},
				"type": "ClusterIP",
			},
		},
	}

	service, err := c.Client.Resource(serviceRes).Namespace(namespace).Create(context.TODO(), serviceObject, metav1.CreateOptions{})
	if err != nil {
		log.Fatalf("Failed to create service: %v\n", err)
	}
	fmt.Printf("Service created: %v\n", service.GetName())
}
{% endhighlight %}

Similarly, we define the `CreateService` function to create a service using the unstructured client. This function accepts the name, selector, namespace, port, and target port for the service. We create a `unstructured.Unstructured` object with the required fields and use the dynamic client to create the service in the specified namespace.

# Delete the created deployment and service

The `DeleteDeployment` and `DeleteService` functions demonstrate how to delete a deployment and service using the unstructured client. We create a `unstructured.Unstructured` object with the required metadata and use the dynamic client to delete the deployment or service in the specified namespace.

{% highlight golang %}
func (c *K8sDynamicClient) DeleteDeployment(name, namespace string) {
	deploymentRes := schema.GroupVersionResource{
		Group:    "apps",
		Version:  "v1",
		Resource: "deployments",
	}

	deploymentObject := &unstructured.Unstructured{
		Object: map[string]interface{}{
			"apiVersion": "apps/v1",
			"kind":       "Deployment",
			"metadata": map[string]interface{}{
				"name": name,
			},
		},
	}

	err := c.Client.Resource(deploymentRes).Namespace(namespace).Delete(context.TODO(), deploymentObject.GetName(), metav1.DeleteOptions{})
	if err != nil {
		log.Fatalf("Failed to delete deployment: %v\n", err)
	}
	fmt.Printf("Deployment deleted: %v\n", deploymentObject.GetName())
}

func (c *K8sDynamicClient) DeleteService(name, namespace string) {
	serviceRes := schema.GroupVersionResource{
		Group:    "",
		Version:  "v1",
		Resource: "services",
	}

	serviceObject := &unstructured.Unstructured{
		Object: map[string]interface{}{
			"apiVersion": "v1",
			"kind":       "Service",
			"metadata": map[string]interface{}{
				"name": name,
			},
		},
	}

	err := c.Client.Resource(serviceRes).Namespace(namespace).Delete(context.TODO(), serviceObject.GetName(), metav1.DeleteOptions{})
	if err != nil {
		log.Fatalf("Failed to delete service: %v\n", err)
	}
	fmt.Printf("Service deleted: %v\n", serviceObject.GetName())
}
{% endhighlight %}

# The Main Function
In the main function, we initialize the dynamic client and create a deployment and service using the `CreateDeployment` and `CreateService` functions. We then delete the created deployment and service using the `DeleteDeployment` and `DeleteService` functions.

{% highlight golang %}
func main() {
	fmt.Println("How to use the unstructred client to create a Kubernetes Deployment")
	client := getK8sClient()

	deploymentName := "korn"
	serviceName := "korn"
	namespace := "podkiller"
	image := "docker.io/nginx:latest"
	// Create a deployment
	client.CreateDeployment(deploymentName, namespace, image, 80, 1)
	// Create a service
	client.CreateService(serviceName, deploymentName, namespace, 80, 80)

	// Cleanup resource
	client.DeleteDeployment(deploymentName, namespace)
	client.DeleteService(serviceName, namespace)
}
{% endhighlight %}

# Assembling the Pieces

After putting all the pieces together, we have a `main.go` file containing all the code we discussed previously. Secondly, we have a `go.mod` file containing the dependencies.

{% gist fdd8278b9250a0f0a56b3eec43b8abcb %}

# Conclusion
This article has demonstrated how to use the Go unstructured client to create and manage Kubernetes deployments and services. By using the unstructured client, you can write code that works with Kubernetes resources without having to define strong types for each resource. This can be especially helpful when dealing with custom resources or when you want to write generic code that can handle multiple resource types.