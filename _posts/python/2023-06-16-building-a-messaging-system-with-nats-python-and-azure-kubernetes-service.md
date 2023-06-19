---
layout: post
comments: true
current: post
cover: assets/images/posts/leo-castro-VcCHO0atmtw-unsplash_resized.webp
navigation: True
title: "Building a Messaging System with NATS, Python, and Azure Kubernetes Service"
date: 2023-06-16 10:00:00
tags: [Python, Kubernetes, Azure]
class: post-template
subclass: 'post tag-python'
author: faizan
excerpt: Learn how to build a messaging system using NATS, Python, and Azure Kubernetes Service in our step-by-step guide.
social_excerpt: "Dive into our latest guide where we walk through setting up a distributed messaging system with NATS, Python, and Azure Kubernetes Service. Learn to deploy a NATS server, build Python publisher and subscriber applications, package them as Docker containers, and run them on AKS! Get started today! #python #nats #azure #kubernetes #aks"
---

# Building a Messaging System with NATS, Python, and Azure Kubernetes Service

This article walks you through building a messaging system with NATS (an acronym for Neural Autonomic Transport System) and Python deployed in Azure Kubernetes Service (AKS). NATS is an open-source messaging system. NATS has a core publish-subscribe server designed for performance, scalability, and ease of use.

# Prerequisites

Before we start, make sure you have the following:

- An active Azure subscription.
- The Azure CLI `az` installed and configured.
- Python 3 and pip installed.
- Docker installed.
- Kubernetes CLI `kubectl` installed and configured.
- Helm: We'll use Helm to deploy NATS on our Kubernetes cluster.

***

# Table of Contents
* [Deploying NATS on Azure Kubernetes Service](#deploying-nats-on-azure-kubernetes-service)
* [Creating a Python Publisher and Subscriber](#creating-a-python-publisher-and-subscriber)
* [Running the Python Applications in Kubernetes](#running-the-python-applications-in-kubernetes)
* [Deploying to Kubernetes and Testing](#deploying-to-kubernetes-and-testing)
* [Conclusion](#conclusion)

***

## Deploying NATS on Azure Kubernetes Service

First, we need to create a Kubernetes cluster on AKS. Use the following `az` CLI commands:

{% highlight bash %}
az group create --name myResourceGroup --location eastus
az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
{% endhighlight %}

Next, we'll deploy a NATS server on our AKS cluster. We can do this easily using Helm, a package manager for Kubernetes. With Helm installed and your, AKS cluster up and running, execute the following commands to add the NATS Helm chart repo and install NATS:

{% highlight bash %}
helm repo add nats https://nats-io.github.io/k8s/helm/charts/
helm repo update
helm install my-nats nats/nats
{% endhighlight %}

The above command deploys a single server NATS setup onto your cluster.

## Creating a Python Publisher and Subscriber

Next, we'll create a publisher and a subscriber application using Python. The publisher will publish messages to a NATS subject, and the subscriber will subscribe to this subject to receive these messages. Here's a simple example of a publisher in the `publisher.py` file:

{% highlight python %}
from nats import NATS, Msg

async def main():
    nc = NATS()
    await nc.connect("nats://localhost:4222")
    await nc.publish("foo", b'Hello World')
    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
{% endhighlight %}

And here's a Python subscriber `subscriber.py`:

{% highlight python %}
from nats import NATS, Msg

async def message_handler(msg: Msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print(f'Received a message on {subject}: {data}')

async def main():
    nc = NATS()
    await nc.connect("nats://localhost:4222")
    sid = await nc.subscribe("foo", cb=message_handler)
    await nc.auto_unsubscribe(sid, max=1)
    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
{% endhighlight %}

These scripts will send and receive a "Hello World" message through NATS.

## Running the Python Applications in Kubernetes

Package your Python applications as Docker containers and deploy them onto your AKS cluster. Here are basic `Dockerfile` examples for both applications:

Dockefile for Publisher:

{% highlight Dockerfile %}
FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN pip install nats.py
CMD [ "python", "./publisher.py" ]
{% endhighlight %}

Dockerfile for Subscriber:

{% highlight Dockerfile %}
FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN pip install nats.py
CMD [ "python", "./subscriber.py" ]
{% endhighlight %}

Then, build and push these Docker images to a Docker registry accessible by your AKS cluster.

## Deploying to Kubernetes and Testing

After preparing the Docker images, we can deploy our Python applications to our AKS cluster. We'll use Kubernetes Deployments and Services to manage our applications. Here are basic examples for the publisher and subscriber:

Kubernetes Publisher Deployment Spec:

{% highlight yaml %}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: publisher-deployment
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
        image: <your-docker-registry>/publisher:latest
        ports:
        - containerPort: 8080
{% endhighlight %}

Kubernetes Subscriber Deployment Spec:

{% highlight yaml %}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: subscriber-deployment
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
        image: <your-docker-registry>/subscriber:latest
        ports:
        - containerPort: 8080
{% endhighlight %}

Deploy these Kubernetes objects using `kubectl apply -f <file-name>`. Once the Deployments and Services are active, the publisher will send messages, and the subscriber will receive them.

To verify that our system is working correctly, we can check the logs of our subscriber:

{% highlight bash %}
kubectl logs -l app=subscriber
{% endhighlight %}

If everything is set up correctly, you should see `"Received a message on foo: Hello World"` in the logs.

## Conclusion

In this guide, we built a distributed messaging system using NATS, Python, and Azure Kubernetes Service. We deployed a NATS server onto AKS, made Python publisher and subscriber applications, packaged them as Docker containers, and ran them on AKS.

This guide is a basic introduction to NATS, Python, and AKS. Feel free to expand upon this guide to build more complex systems tailored to your needs.
