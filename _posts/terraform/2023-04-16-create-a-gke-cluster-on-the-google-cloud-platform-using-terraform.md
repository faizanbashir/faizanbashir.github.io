---
layout: post
comments: true
current: post
cover: assets/images/posts/jasper-boer-LJD6U920zVo-unsplash_resized.webp
navigation: True
title: "Create a GKE Cluster on the Google Cloud Platform using Terraform"
date: 2023-04-16 03:13:02
tags: [Terraform, GCP]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: Learn how to create a Google Kubernetes Engine (GKE) cluster on Google Cloud Platform using Terraform, the popular Infrastructure as Code tool.
---

# Create a GKE Cluster on the Google Cloud Platform using Terraform

Google Kubernetes Engine (GKE) is a managed Kubernetes service offered by Google Cloud Platform (GCP), simplifying containerized applications' management and deployment. This tutorial will guide you through creating a GKE cluster using Terraform, a widespread Infrastructure as Code (IaC) tool.

# Prerequisites
1. A Google Cloud Platform account
2. The Google Cloud SDK installed and configured
3. Terraform installed

***
# Table of Contents:

* [Set up the Terraform Configuration](#set-up-the-terraform-configuration)
* [Initialize Terraform](#initialize-terraform)
* [Connect to the GKE Cluster](#connect-to-the-gke-cluster)
* [Clean Up Resources](#clean-up-resources)
* [Conclusion](#conclusion)
* [Dive Deeper: Recommended Reads](#dive-deeper-recommended-reads)

***

# Set up the Terraform Configuration

First, create a new directory for your Terraform configuration:

{% highlight shell %}
$ mkdir gke-terraform
$ cd gke-terraform
{% endhighlight %}

Create a `main.tf` file in the `gke-terraform` directory and add the following code:

{% highlight hcl %}
provider "google" {
  credentials = file("<PATH_TO_YOUR_SERVICE_ACCOUNT_KEY_JSON>")
  project     = "<YOUR_PROJECT_ID>"
  region      = "<YOUR_REGION>"
}

resource "google_container_cluster" "gke_cluster" {
  name               = "gke-cluster"
  location           = "<YOUR_REGION>"
  initial_node_count = 1

  node_config {
    machine_type = "n1-standard-1"
  }
}

output "cluster_endpoint" {
  value = google_container_cluster.gke_cluster.endpoint
}

output "cluster_ca_certificate" {
  value     = google_container_cluster.gke_cluster.master_auth.0.cluster_ca_certificate
  sensitive = true
}
{% endhighlight %}

Replace `<PATH_TO_YOUR_SERVICE_ACCOUNT_KEY_JSON>` with the path to your GCP service account key JSON file, `<YOUR_PROJECT_ID>` with your GCP project ID, and `<YOUR_REGION>` with your desired GCP region.

# Initialize Terraform

In the `gke-terraform` directory, run the following command to initialize Terraform:

{% highlight shell %}
$ terraform init
{% endhighlight %}

This command downloads the required provider plugins and sets up the backend for storing your Terraform state.

# Create the GKE Cluster

Run the following command to create the GKE cluster:

{% highlight shell %}
$ terraform apply
{% endhighlight %}

Type "yes" when prompted to confirm that you want to create the resources. The resource creation process may take several minutes to complete. Once done, Terraform will output the cluster endpoint and cluster CA certificate.

# Connect to the GKE Cluster
Save the kubeconfig output from the previous step to a file, and set the `KUBECONFIG` environment variable to use it:

{% highlight shell %}
$ gcloud container clusters get-credentials gke-cluster --region <YOUR_REGION>
{% endhighlight %}

Now, you can use kubectl to interact with your GKE cluster:

{% highlight shell %}
$ kubectl get nodes
{% endhighlight %}

This command will show the nodes in your GKE cluster.

# Clean Up Resources
When you no longer need the GKE cluster, you can destroy the resources using Terraform:

{% highlight shell %}
$ terraform destroy
{% endhighlight %}

Type "yes" when prompted to confirm that you want to destroy the resources.

# Conclusion
This tutorial taught you how to create a Google Kubernetes Engine (GKE) cluster using Terraform on the Google Cloud Platform. By leveraging Infrastructure as Code, you can maintain consistent environments, collaborate with your team more effectively, and automate the provisioning and management of your Kubernetes clusters.

With your GKE cluster up and running, you can now deploy containerized applications, scale your infrastructure, and take advantage of the many features offered by GCP and Kubernetes. To dive deeper into GKE and Terraform, explore the official GKE documentation and the Terraform Google provider documentation.

# Dive Deeper: Recommended Reads

Expand your knowledge of Infrastructure as Code and Terraform with our insightful collection of articles! Dive into a range of topics that will help you master the art of managing infrastructure:

* [Terraform Best Practices](/terraform-best-practices): Learn the most effective ways to use Terraform in your projects.
* [Managing environments through Terraform Workspaces](/managing-environments-through-terraform-workspaces): Discover how to manage multiple environments with ease.
* [Building highly available VMSS on Azure using Terraform Modules](/building-highly-available-vmss-on-azure-using-terraform-modules): Create scalable and highly available virtual machine scale sets on Azure.
* [Building an Elasticache cluster on AWS using Terraform Modules](/building-an-elasticache-cluster-on-aws-using-terraform-modules): Harness the power of AWS Elasticache with Terraform.
* [Demystifying Terraform Modules](/demystifying-terraform-modules): Understand the ins and outs of Terraform modules.
* [Building an Nginx web server on Azure using Terraform](/building-an-nginx-webserver-on-azure-using-terraform): Deploy a reliable Nginx web server on Azure.
* [Building an Nginx web server on AWS using Terraform](/building-an-nginx-webserver-on-aws-using-terraform): Set up an Nginx web server on AWS with Terraform.
* [Introduction to Infrastructure as Code (IaC)](/introduction-to-infrastructure-as-code): Get started with Infrastructure as Code and grasp the fundamentals.
* [Deploying an Azure Kubernetes Service (AKS) Cluster with Terraform](/deploying-an-azure-kubernetes-service-aks-cluster-with-terraform): Deploy an Azure Kubernetes Service (AKS) cluster seamlessly with Terraform's infrastructure management capabilities.
* [Building an EKS Cluster on AWS with Terraform: A Step-by-Step Guide](/building-an-eks-cluster-on-aws-with-terraform): Spin an Amazon EKS cluster effortlessly using Terraform, following our detailed step-by-step guide.

Embrace the power of Terraform and Infrastructure as Code with this comprehensive collection of articles, and enhance your skills in deploying, managing, and maintaining your infrastructure.