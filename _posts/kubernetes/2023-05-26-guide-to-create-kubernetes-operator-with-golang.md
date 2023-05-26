---
layout: post
comments: true
current: post
cover: assets/images/posts/jack-church-EG0U9_VvER4-unsplash_resized.webp
navigation: True
title: "A Guide to Creating Kubernetes Operators with Go"
date: 2023-05-26 10:00:00
tags: [Kubernetes, Golang]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: Get hands-on with our comprehensive guide on creating Kubernetes Operators using Go. This article takes you through the journey of developing Kubernetes Operators, helping you manage complex Kubernetes applications with ease and efficiency. Unlock the full potential of Kubernetes with Go now!"
social_excerpt: "Dive into the world of Kubernetes Operators with our latest guide! Learn how to leverage Go, the popular programming language loved by cloud developers, to create powerful Kubernetes Operators. Streamline and automate your Kubernetes clusters like never before. Don't miss out! #Kubernetes #Golang #containers #operatorSDK #operator"
---

# A Guide to Creating Kubernetes Operators with Go

Kubernetes operators are custom software extensions that manage and automate tasks for applications running on Kubernetes clusters. This article demonstrates creating a Kubernetes operator using the Go programming language and the Kubernetes Operator SDK.

# Prerequisites
To follow this guide, you need:

* A basic understanding of Kubernetes and Go programming language
* A Kubernetes cluster (e.g., Minikube, kind, or any cloud-based Kubernetes service)
* The `kubectl` command-line tool installed
* The Go programming language (version 1.16+) installed
* The Operator SDK installed

***

# Table of Contents
* [What are Kubernetes Operators?](#what-are-kubernetes-operators)
* [Setting Up the Development Environment](#setting-up-the-development-environment)
* [Creating a Custom Resource Definition (CRD)](#creating-a-custom-resource-definition-crd)
* [Implementing the Operator](#implementing-the-operator)
* [Deploying the Operator](#deploying-the-operator)
* [Testing the Operator](#testing-the-operator)
* [Conclusion](#conclusion)

***

# What are Kubernetes Operators?
Kubernetes operators are custom controllers that extend the Kubernetes API to manage complex applications. They allow you to define custom resources and provide the necessary automation to handle them.

# Setting Up the Development Environment
First, create a new directory for your operator:

{% highlight shell %}
$ mkdir my-operator && cd my-operator
{% endhighlight %}

Initialize the project with the `operator-sdk`:

{% highlight shell %}
$ operator-sdk init --domain example.com --repo github.com/example/my-operator
{% endhighlight %}

This command creates your operator's necessary files and directories, including the `Dockerfile`, `Makefile`, and the Go module.

# Creating a Custom Resource Definition (CRD)

Now, create a custom resource definition (CRD) for your operator:

{% highlight shell %}
$ operator-sdk create api --group apps --version v1alpha1 --kind MyApp --resource --controller
{% endhighlight %}

This command generates the following files:

* `api/v1alpha1/myapp_types.go`: Defines the MyApp custom resource (CR)
* `controllers/myapp_controller.go`: Implements the MyApp controller

`Edit api/v1alpha1/myapp_types.go` to define the MyApp CR spec and status:

{% highlight golang %}
package v1alpha1

import (
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// MyAppSpec defines the desired state of MyApp
type MyAppSpec struct {
    // INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
    // Important: Run "make" to regenerate code after modifying this file

    // Replicas is the number of replicas for the application
    Replicas int32 `json:"replicas"`
}

// MyAppStatus defines the observed state of MyApp
type MyAppStatus struct {
    // INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
    // Important: Run "make" to regenerate code after modifying this file

    // ReadyReplicas is the number of ready replicas for the application
    ReadyReplicas int32 `json:"readyReplicas"`
}

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status

// MyApp is the Schema for the myapps API
type MyApp struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   MyAppSpec   `json:"spec,omitempty"`
    Status MyAppStatus `json:"status,omitempty"`
}

//+kubebuilder:object:
//+root=true

// MyAppList contains a list of MyApp
type MyAppList struct {
    metav1.TypeMeta `json:",inline"`
    metav1.ListMeta `json:"metadata,omitempty"`
    Items           []MyApp `json:"items"`
}

func init() {
    SchemeBuilder.Register(&MyApp{}, &MyAppList{})
}
{% endhighlight %}

After defining the CRD, run the following command to update the generated code:

{% highlight shell %}
$ make generate
{% endhighlight %}

# Implementing the Operator
Next, open the `controllers/myapp_controller.go` file to implement the `MyApp` controller. Start by importing the necessary packages at the top of the file:

{% highlight golang %}
import (
    "context"
    "fmt"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    "k8s.io/apimachinery/pkg/api/errors"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"

    appsv1alpha1 "github.com/example/my-operator/api/v1alpha1"
)
{% endhighlight %}

Implement the `Reconcile` method in the `MyAppReconciler` struct:

{% highlight golang %}
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    _ = r.Log.WithValues("myapp", req.NamespacedName)

    // Fetch the MyApp instance
    myApp := &appsv1alpha1.MyApp{}
    err := r.Get(ctx, req.NamespacedName, myApp)
    if err != nil {
        if errors.IsNotFound(err) {
            // Request object not found, could have been deleted after reconcile request.
            return ctrl.Result{}, nil
        }
        // Error reading the object - requeue the request.
        return ctrl.Result{}, err
    }

    // Implement your logic here
    // ...m
}
{% endhighlight %}

Now, implement the logic to create and manage your application's `Deployment` and a `Service`. You can find examples in the official [Kubernetes client-go example repository](https://github.com/kubernetes/client-go/tree/master/examples).

# Deploying the Operator

Build and push the operator image:

{% highlight shell %}
$ make docker-build docker-push IMG=my-operator:latest
{% endhighlight %}

Deploy the operator to your cluster:

{% highlight shell %}
$ make deploy IMG=my-operator:latest
{% endhighlight %}

# Testing the Operator
Create a sample `MyApp` custom resource:

{% highlight yaml %}
apiVersion: apps.example.com/v1alpha1
kind: MyApp
metadata:
  name: my-app
spec:
  replicas: 3
{% endhighlight %}

Save this as `myapp-sample.yaml`, then apply it to your cluster:

{% highlight shell %}
$ kubectl apply -f myapp-sample.yaml
{% endhighlight %}

Check if the operator creates the `Deployment` and `Service` for your application:

{% highlight shell %}
$ kubectl get deployments
$ kubectl get services
{% endhighlight %}

# Conclusion
In this guide, you have learned how to create a Kubernetes operator using the Go programming language and the Kubernetes Operator SDK. You can now extend the Kubernetes API to manage complex applications and automate tasks on your cluster.