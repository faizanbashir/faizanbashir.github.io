---
layout: post
comments: true
current: post
cover: ./assets/images/posts/sharad-bhat--fVs_61OaAA-unsplash_resized.webp
navigation: True
title: "Interacting with Kubernetes Deployments and Services using Python SDK"
date: 2023-05-29 10:00:00
tags: [Kubernetes, Python]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: Explore the seamless integration of Kubernetes and Python in our comprehensive guide. Learn how to interact with Kubernetes deployments and services using Python SDK, making your cloud-native journey more efficient and pythonic. Begin your Kubernetes automation with Python today!
social_excerpt: "Discover the power of Kubernetes combined with Python! In our newest guide, we delve into using the Python SDK for interacting with Kubernetes deployments and services. Harness the versatility of Python and the robustness of Kubernetes in one place. Check it out now! #Kubernetes #PythonSDK #Python #containers"

---

# Interacting with Kubernetes Deployments and Services using Python SDK

Kubernetes has become the de facto choice for a container orchestration platform that automates containerized applications' deployment, scaling, and management. This article will demonstrate how to interact with Kubernetes Deployments and Services using Python and the official Kubernetes Python client.

# Prerequisites
To follow this guide, you will need:

1. A Kubernetes cluster is up and running.
2. `kubectl` is installed and configured to access your cluster.
3. Python `3.x` installed.
4. Kubernetes Python client. 

You can install the Kubernetes Python client library using `pip`:

{% highlight shell %}
pip install kubernetes
{% endhighlight %}

We will cover the following topics:

***

# Table of Contents

* [Listing Kubernetes Deployments](#listing-kubernetes-deployments)
* [Listing Kubernetes Services](#listing-kubernetes-services)
* [Updating a Kubernetes Deployment](#updating-a-kubernetes-deployment)
* [Updating a Kubernetes Service](#updating-a-kubernetes-service)
* [Deleting a Kubernetes Deployment](#deleting-a-kubernetes-deployment)
* [Deleting a Kubernetes Service](#deleting-a-kubernetes-service)
* [Conclusion](#conclusion)

***

# Listing Kubernetes Deployments

Let's create a script to list all existing Deployments in the `default` namespace:

{% highlight python %}
from kubernetes import client, config

def list_deployments(api_instance, namespace):
    # List Deployments
    deployments = api_instance.list_namespaced_deployment(namespace)
    for deployment in deployments.items:
        print("Name: %s, Replicas: %s" % (deployment.metadata.name, deployment.spec.replicas))

def main():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    namespace = "default"
    list_deployments(apps_v1, namespace)

if __name__ == '__main__':
    main()
{% endhighlight %}

Run the script using the following:

{% highlight shell %}
python list_deployments.py
{% endhighlight %}

# Listing Kubernetes Services

Now, let's create a script to list all existing Services in the `default` namespace:

{% highlight python %}
from kubernetes import client, config

def list_services(api_instance, namespace):
    # List Services
    services = api_instance.list_namespaced_service(namespace)
    for service in services.items:
        print("Name: %s, Cluster IP: %s" % (service.metadata.name, service.spec.cluster_ip))

def main():
    config.load_kube_config()
    namespace = "default"
    core_v1 = client.CoreV1Api()
    list_services(core_v1, namespace)

if __name__ == '__main__':
    main()
{% endhighlight %}

Run the script using the following:

{% highlight shell %}
python list_services.py
{% endhighlight %}

# Updating a Kubernetes Deployment

To update a Deployment, you can patch it with the desired changes. In this example, we will update the number of replicas for an existing Deployment:

{% highlight python %}
from kubernetes import client, config

def update_deployment_replicas(api_instance, deployment_name, new_replicas, namespace):
    # Update Deployment replicas
    body = {
        "spec": {
            "replicas": new_replicas
        }
    }
    api_response = api_instance.patch_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body=body
    )
    print("Deployment updated")

def main():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    namespace = "default"
    deployment_name = "nginx-deployment"
    new_replicas = 5
    update_deployment_replicas(apps_v1, deployment_name, new_replicas, namespace)

if __name__ == '__main__':
    main()
{% endhighlight %}

Run the script using the following:

{% highlight shell %}
python update_deployment.py
{% endhighlight %}

Verify updates to the Deployment using the following command:

{% highlight shell %}
kubectl get deployments
{% endhighlight %}

# Updating a Kubernetes Service

To update a Service, you can patch it with the desired changes. In this example, we will update the type of an existing Service:

{% highlight python %}
from kubernetes import client, config

def update_service_type(api_instance, service_name, new_type, namespace):
    # Update Service type
    body = {
        "spec": {
            "type": new_type
        }
    }
    api_response = api_instance.patch_namespaced_service(
        name=service_name,
        namespace=namespace,
        body=body
    )
    print("Service updated")

def main():
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    namespace = "default"
    service_name = "nginx-service"
    new_type = "NodePort"
    update_service_type(core_v1, service_name, new_type, namespace)

if __name__ == '__main__':
    main()
{% endhighlight %}

Run the script using the following:

{% highlight shell %}
python update_service.py
{% endhighlight %}

Verify updates to the Service using the following command:

{% highlight shell %}
kubectl get services
{% endhighlight %}

# Deleting a Kubernetes Deployment

To delete a Deployment, use the following script:

{% highlight python %}
from kubernetes import client, config

def delete_deployment(api_instance, deployment_name, namespace):
    # Delete Deployment
    api_response = api_instance.delete_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body=client.V1DeleteOptions(propagation_policy="Foreground", grace_period_seconds=5)
    )
    print("Deployment deleted")

def main():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()

    namespace = "default"
    deployment_name = "nginx-deployment"
    delete_deployment(apps_v1, deployment_name, namespace)

if __name__ == '__main__':
    main()
{% endhighlight %}

Run the script using the following:

{% highlight shell %}
python delete_deployment.py
{% endhighlight %}

# Deleting a Kubernetes Service
To delete a Service, use the following script:

{% highlight python %}
from kubernetes import client, config

def delete_service(api_instance, service_name, namespace):
    # Delete Service
    api_response = api_instance.delete_namespaced_service(
        name=service_name,
        namespace=namespace,
        body=client.V1DeleteOptions()
    )
    print("Service deleted")

def main():
    config.load_kube_config()
    core_v1 = client.CoreV1Api()

    namespace = "default"
    service_name = "nginx-service"
    delete_service(core_v1, service_name, namespace)

if __name__ == '__main__':
    main()
{% endhighlight %}

Run the script using the following:

{% highlight shell %}
python delete_service.py
{% endhighlight %}

# Conclusion

To summarise, we demonstrated how to interact with Kubernetes Deployments and Services using Python and the official Kubernetes Python client. You can now use these examples as a starting point to build more complex interactions and automation for your Kubernetes workloads.