---
layout: post
comments: true
current: post
cover: assets/images/posts/alexander-schimmeck-Aohf8gqa7Zc-unsplash_resized.webp
navigation: True
title: "Building a Messaging System with NATS, Golang, and Azure Kubernetes Service"
date: 2023-06-07 11:11:11
tags: [Golang]
class: post-template
subclass: 'post tag-golang'
author: faizan
excerpt: Learn how to build a messaging system using NATS, Golang, and Azure Kubernetes Service in our step-by-step guide.
social_excrpt: "Dive into our latest guide, where we walk through setting up a messaging system with #NATS, #Golang, and #Azure #Kubernetes Service. Learn to deploy a NATS server, build Golang publisher and subscriber applications, package them as #Docker #containers, and run them on #AKS!"
---

# Building a Messaging System with NATS, Golang, and Azure Kubernetes Service

This article walks you through building a messaging system with NATS (an acronym for Neural Autonomic Transport System) and Golang deployed in Azure Kubernetes Service (AKS). NATS is an open-source messaging system. Written in the Go programming language. NATS has a core publish-subscribe server designed for performance, scalability, and ease of use.

## Prerequisites

- Go (version `1.16` or later): We'll use Go to write our publisher and subscriber applications.
- Docker: We'll use Docker to build and package our Go applications.
- Kubernetes CLI (`kubectl`): We'll use kubectl to interact with our Kubernetes cluster.
- Helm: We'll use Helm to deploy NATS on our Kubernetes cluster.

You'll also need access to an Azure Kubernetes Service (AKS) cluster. If you haven't already, follow the Azure documentation to [create an AKS cluster](https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes).

***

# Table of Contents:

* [Deploying NATS on Azure Kubernetes Service](#deploying-nats-on-azure-kubernetes-service)
* [Creating a Go Publisher and Subscriber](#creating-a-go-publisher-and-subscriber)
* [Running the Go Applications in Kubernetes](#running-the-go-applications-in-kubernetes)
* [Deploying to Kubernetes and Testing](#deploying-to-kubernetes-and-testing)
* [Conclusion](#conclusion)

***


## Deploying NATS on Azure Kubernetes Service

First, we'll deploy a NATS server on our AKS cluster. We can do this easily using Helm, a package manager for Kubernetes. With Helm installed and your, AKS cluster up and running, execute the following commands to add the NATS Helm chart repo and install NATS:

{% highlight bash %}
helm repo add nats https://nats-io.github.io/k8s/helm/charts/
helm repo update
helm install my-nats nats/nats
{% endhighlight %}

Helm will deploy a NATS server on your AKS cluster.

## Creating a Go Publisher and Subscriber

Next, we'll create a publisher and a subscriber application using Go. The publisher will publish messages to a NATS subject, and the subscriber will subscribe to this subject to receive these messages. Here's a simple example of a publisher in the `publisher.go` file:

{% highlight go %}
package main

import (
  "log"
  "github.com/nats-io/nats.go"
)

func main() {
  nc, _ := nats.Connect(nats.DefaultURL)
  log.Println("Connected to " + nats.DefaultURL)
  nc.Publish("foo", []byte("Hello World"))
  log.Println("Published message on subject 'foo'")
  nc.Close()
}
{% endhighlight %}

And a subscriber in the `subscriber.go` file:

{% highlight go %}
package main

import (
  "log"
  "github.com/nats-io/nats.go"
)

func main() {
  nc, _ := nats.Connect(nats.DefaultURL)
  log.Println("Connected to " + nats.DefaultURL)
  _, _ = nc.Subscribe("foo", func(m *nats.Msg) {
    log.Printf("Received a message on %s: %s\n", m.Subject, string(m.Data))
  })

  select {}
}
{% endhighlight %}

## Running the Go Applications in Kubernetes

Now we will containerize our Go applications using Docker. Here's a basic Dockerfile for our Go applications:

{% highlight Dockerfile %}
FROM golang:1.16

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY *.go ./

RUN go build -o main .

CMD ["/app/main"]
{% endhighlight %}

Build Docker images for both applications, tag them, and push them to a Docker registry. Here's how you might do it:

{% highlight bash %}
docker build -t publisher .
docker tag publisher:latest myregistry/publisher:latest
docker push myregistry/publisher:latest
{% endhighlight %}

Remember to replace `myregistry` with the name of your Docker registry.

## Deploying to Kubernetes and Testing

With our Docker images pushed to the registry, we can now deploy our applications to Kubernetes. We'll create a deployment for each application, creating a pod for each.

{% highlight yaml %}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: publisher
spec:
  replicas: 1
  selector:
    matchLabels:
      app: publisher
  template:
    metadata:
      labels:
        app: publisher
    spec:
      containers:
        - name: publisher
          image: myregistry/publisher:latest
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: subscriber
spec:
  replicas: 1
  selector:
    matchLabels:
      app: subscriber
  template:
    metadata:
      labels:
        app: subscriber
    spec:
      containers:
        - name: subscriber
          image: myregistry/subscriber:latest
{% endhighlight %}

Finally, we can test our setup by publishing a message. We should see this message appear in the logs of our subscriber:

{% highlight bash %}
kubectl logs -l app=subscriber
{% endhighlight %}

## Conclusion

In this guide, we built a messaging system using NATS, Golang, and Azure Kubernetes Service. We deployed a NATS server onto AKS, made Golang publisher and subscriber applications, packaged them as Docker containers, and ran them on AKS. This guide is a basic introduction to NATS, Golang, and AKS. Feel free to expand upon this guide to build more complex systems tailored to your needs.