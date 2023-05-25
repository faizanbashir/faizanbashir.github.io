---
layout: post
comments: true
current: post
cover: assets/images/posts/sina-rezakhani-6Pce32oZYuc-unsplash_resized.webp
navigation: True
title: "Creating Kubernetes Custom Resource Definitions using the Kubernetes Python SDK"
date: 2023-04-02 10:00:00
tags: [Kubernetes, Python]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: This comprehensive guide covers a range of Kubernetes best practices, from designing and configuring applications to monitoring and securing the cluster.
---

# Introduction

Kubernetes is a widely-used container orchestration platform that automates the deployment, scaling, and management of containerized applications. To interact with Kubernetes clusters programmatically, developers can use the Kubernetes Python client library, which provides a dynamic client for working with custom resources and the Kubernetes API.

In this tutorial, we will demonstrate how to use the Kubernetes dynamic client library in Python to interact with Kubernetes clusters, covering topics such as authentication, listing resources, creating and deleting custom resources, and more.

# Prerequisites

Before starting, make sure you have the following installed:

1. Python `3.6` or higher
2. The Kubernetes Python client library: `pip install kubernetes`

***

# Table of Contents

* [Setting up the Kubernetes Dynamic Client](#setting-up-the-kubernetes-dynamic-client)
* [Listing Resources using the Dynamic Client](#listing-resources-using-the-dynamic-client)
* [Creating Custom Resource Definitions and Resources](#creating-custom-resource-definitions-and-resources)
* [Deleting Custom Resources](#deleting-custom-resources)
* [Deleting Custom Resource Definitions](#deleting-custom-resource-definitions)
* [Conclusion](#conclusion)

***

# Setting up the Kubernetes Dynamic Client
First, import the necessary modules and create an API client:

{% highlight python %}
from kubernetes import config, client
from kubernetes.dynamic import DynamicClient

# Load the kubeconfig file from the default location (~/.kube/config)
config.load_kube_config()

# Create a dynamic client
dyn_client = DynamicClient(client.ApiClient())
{% endhighlight %}

# Listing Resources using the Dynamic Client
To list resources, you will need to create a `Resource` instance for the desired resource type. In this example, we will list all Pods in the `default` namespace:

{% highlight python %}
from kubernetes.client import V1PodList

# Define the API resource for Pods
pod_resource = dyn_client.resources.get(api_version='v1', kind='Pod')

# List Pods in the "default" namespace
pods: V1PodList = pod_resource.get(namespace='default')

for pod in pods.items:
    print(f"Name: {pod.metadata.name}, Namespace: {pod.metadata.namespace}")
{% endhighlight %}

# Creating Custom Resource Definitions and Resources

To create custom resources, you will need to define the Custom Resource Definition (CRD) and create an instance of the custom resource. In this example, we will create a custom resource for a sample CRD:

{% highlight python %}
# Define the custom resource definition
crd = {
    'apiVersion': 'apiextensions.k8s.io/v1',
    'kind': 'CustomResourceDefinition',
    'metadata': {
        'name': 'apps.faizanbashir.me'  # Adjusted according to rule 1
    },
    'spec': {
        'group': 'faizanbashir.me',
        'versions': [  # Added this to satisfy rule 2
            {
                'name': 'v1alpha1',
                'served': True,
                'storage': True,
                'schema': {
                    'openAPIV3Schema': {
                        'type': 'object',
                        'properties': {
                            'spec': {
                                'type': 'object',
                                'properties': {
                                    'message': {
                                        'type': 'string'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ],
        'names': {
            'kind': 'App',
            'plural': 'apps',  # Adjusted according to rule 3
            'singular': 'app',
            'shortNames': [
                "fba"
            ]
        },
        'scope': 'Namespaced'
    },
    'status': {  # Added this to satisfy rule 4
        'storedVersions': ['v1alpha1']
    }
}

# Create the CRD using the dynamic client
crd_resource = dyn_client.resources.get(api_version='apiextensions.k8s.io/v1' kind='CustomResourceDefinition')
created_crd = crd_resource.create(body=crd)
print(f"Created CRD {created_crd.metadata.name}")

# Define the custom resource
crd_spec = {
    'apiVersion': 'faizanbashir.me/v1alpha1',
    'kind': 'App',
    'metadata': {
        'name': 'my-crd',
        'namespace': 'default'
    },
    'spec': {
        'message': 'Hello, Kubernetes!'
    }
}

# Create the custom resource using the dynamic client
my_resource = dyn_client.resources.get(api_version='faizanbashir.me/v1alpha1', kind='App')
created_resource = my_resource.create(body=crd_spec, namespace='default')
print(f"Created resource mycrd")
{% endhighlight %}

# Deleting Custom Resources
To delete a custom resource, use the `delete` method on the `Resource` instance:

{% highlight python %}
# Delete the custom resource
my_resource = dyn_client.resources.get(api_version='faizanbashir.me/v1alpha1', kind='App')
my_resource.delete(name='my-crd', namespace='default')
print(f"Deleted resource my-crd")
{% endhighlight %}

# Deleting Custom Resource Definitions
To delete a custom resource, use the `delete` method on the `CRD` instance:

{% highlight python %}
# Delete the custom Definition
crd_client = dyn_client.resources.get(api_version="apiextensions.k8s.io/v1", kind="CustomResourceDefinition")
deleted_crd = crd_client.delete(name="apps.faizanbashir.me")
print(f"Deleted CRD apps.faizanbashir.me")
{% endhighlight %}

# Conclusion
The Kubernetes dynamic client library for Python provides a powerful and flexible way to interact with Kubernetes clusters, making it easy to manage resources and perform various operations on them. In this tutorial, we demonstrated how to set up the dynamic client, list resources, create and delete custom resources, and more.

By leveraging the Kubernetes dynamic client library in your Python projects, you can automate tasks and build powerful tools to manage your Kubernetes clusters. As you become more familiar with the library, you can explore other operations and resources, adapting the examples provided here to suit your specific needs.