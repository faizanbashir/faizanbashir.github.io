---
layout: post
comments: true
current: post
cover: assets/images/posts/michael-yuan-irisojcwKaM-unsplash_resized.webp
navigation: True
title: "Event-Driven Scaling of Golang Applications in Azure Kubernetes Service (AKS) using KEDA"
date: 2023-06-08 11:11:11
tags: [Golang]
class: post-template
subclass: 'post tag-golang'
author: faizan
excerpt: Learn how to set up event-driven scaling of Golang applications in Azure Kubernetes Service using KEDA, an open-source project providing event-driven autoscaling for Kubernetes workloads.
social_excrpt: "Check out our latest guide on setting up event-driven scaling of Golang applications in Azure Kubernetes Service using KEDA. Learn to build highly scalable, responsive applications that auto-adjust resources based on demand. Dive in now! #azure #golang #aks #keda"
---

# Event-Driven Scaling of Golang Applications in Azure Kubernetes Service (AKS) using KEDA

This article will guide you through setting up event-driven scaling of a Golang application deployed in Azure Kubernetes Service (AKS) using Kubernetes Event-Driven Autoscaling (KEDA). KEDA is an open-source project that provides event-driven autoscaling for Kubernetes workloads.

## Prerequisites

- Go (version `1.16` or later): We'll use Go to write our publisher and subscriber applications.
- Docker: We'll use Docker to build and package our Go application.
- Kubernetes CLI (`kubectl`): We'll use kubectl to interact with our Kubernetes cluster.
- Helm: We'll use Helm to deploy KEDA on our Kubernetes cluster.

Additionally, you'll need an AKS cluster for deploying our application and KEDA. If you don't have an AKS cluster ready to use, you can create an AKS cluster by following this [Azure documentation](https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes).

***

# Table of Contents:

* [Deploying KEDA on AKS](#deploying-keda-on-aks)
* [Building a Golang Application for Event-Driven Scaling](#building-a-golang-application-for-event-driven-scaling)
* [Packaging and Deploying Golang Application in AKS](#packaging-and-deploying-golang-application-in-aks)
* [Testing Event-Driven Scaling](#testing-event-driven-scaling)
* [Conclusion](#conclusion)

***

## Deploying KEDA on AKS

We'll use Helm, a Kubernetes package manager, to deploy KEDA on AKS. Run the following commands to add the KEDA Helm chart repository and install KEDA:

{% highlight bash %}
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
kubectl create namespace keda
helm install keda kedacore/keda --namespace keda
{% endhighlight %}

## Building a Golang Application for Event-Driven Scaling

Let's build a simple Golang application that reads messages from an Azure Storage Queue. The number of pods in the deployment will automatically scale up or go scale down based on the number of messages in the Azure Storage Queue. Here's a simple Go script that reads messages from Azure Storage Queue:

{% highlight go %}
package main

import (
    "context"
    "fmt"
    "github.com/Azure/azure-storage-queue-go/azqueue"
    "os"
)

func main() {
    connectionString := os.Getenv("AZURE_STORAGE_CONNECTION_STRING")
    queueName := os.Getenv("QUEUE_NAME")
    queueURL := azqueue.NewServiceURLFromConnectionString(connectionString).NewQueueURL(queueName)

    for {
        messagesURL := queueURL.NewMessagesURL()
        messages, _ := messagesURL.Dequeue(context.Background(), 32, 30)

        for _, message := range messages.QueueMessages {
            fmt.Printf("Processing message: %s\n", *message.MessageText)
            messageURL := messagesURL.NewMessageIDURL(*message.MessageID)
            messageURL.Delete(context.Background(), message.PopReceipt)
        }
    }
}
{% endhighlight %}

## Packaging and Deploying Golang Application in AKS

We need to package our Go application using Docker. Create a `Dockerfile` for the same:

{% highlight Dockerfile %}
FROM golang:1.16

WORKDIR /app

COPY go.mod ./
COPY go.sum ./
RUN go mod download

COPY . .

RUN go build -o main .

CMD [ "./main" ]
{% endhighlight %}

After building the Docker image and pushing it to a Docker registry, we create a Kubernetes deployment for our application. However, to enable KEDA, we need to create a `ScaledObject` which defines the scaling parameters:

{% highlight yaml %}
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: golang-scaledobject
spec:
  scaleTargetRef:
    name: golang-deployment
  triggers:
  - type: azure-queue
    metadata:
      connectionFromEnv: AZURE_STORAGE_CONNECTION_STRING
      queueName: myqueue
      queueLength: '5'
{% endhighlight %}

## Testing Event-Driven Scaling

To test the event-driven scaling, add messages to the Azure Storage Queue and observe the number of pods of your Golang application. You should see more pods when there are more messages in the queue and fewer pods when there are fewer messages in the queue.

## Conclusion

This article walked you through setting up event-driven scaling of a Golang application in Azure Kubernetes Service using Kubernetes-based Event-Driven Autoscaling (KEDA). This capability is crucial in building highly scalable and responsive applications that automatically adjust their resources based on demand.
