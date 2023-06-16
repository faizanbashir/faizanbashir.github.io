---
layout: post
comments: true
current: post
cover: assets/images/posts/luke-richardson-ONPD_ZgSedE-unsplash_resized.webp
navigation: True
title: "Deploying an Azure Kubernetes Service (AKS) Cluster with Terraform"
date: 2023-04-16 03:13:02
tags: [Terraform, Azure]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: Learn to create an Azure Kubernetes Service (AKS) cluster with Terraform, a popular Infrastructure as Code tool, using a step-by-step guide with code examples.
---

# Deploying an Azure Kubernetes Service (AKS) Cluster with Terraform

Azure Kubernetes Service (AKS) is a fully managed Kubernetes service offered by Microsoft Azure. It simplifies deploying and managing containerized applications using Kubernetes. This article will demonstrate creating an AKS cluster using Terraform, a widespread Infrastructure as Code (IaC) tool.

# Prerequisites
1. Install Terraform on your local machine.
2. Install Azure CLI and sign in to your Azure account with az login.
3. Make sure you have an active Azure subscription.

***
# Table of Contents:

* [Create Terraform Configuration Files](#create-terraform-configuration-files)
* [Initialize Terraform](#initialize-terraform)
* [Connect to the AKS Cluster](#connect-to-the-aks-cluster)
* [Clean Up Resources](#clean-up-resources)
* [Conclusion](#conclusion)
* [Dive Deeper: Recommended Reads](#dive-deeper-recommended-reads)

***

# Create Terraform Configuration Files

First, create a new directory for your Terraform configuration files:

{% highlight shell %}
$ mkdir aks-terraform
$ cd aks-terraform
{% endhighlight %}

Next, create the main Terraform configuration file `main.tf` and the variables file `variables.tf`.

The `main.tf` file:
{% highlight hcl %}
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_kubernetes_cluster" "example" {
  name                = var.cluster_name
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  dns_prefix          = var.dns_prefix

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.vm_size
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Terraform = "true"
    Environment = "dev"
  }
}

output "kubeconfig" {
  value = azurerm_kubernetes_cluster.example.kube_config_raw
  sensitive = true
}
{% endhighlight %}

The `variables.tf` file:

{% highlight hcl %}
variable "resource_group_name" {
  description = "Name of the resource group"
  default     = "my-aks-rg"
}

variable "location" {
  description = "Azure region for the resources"
  default     = "East US"
}

variable "cluster_name" {
  description = "Name of the AKS cluster"
  default     = "my-aks-cluster"
}

variable "dns_prefix" {
  description = "DNS prefix for the AKS cluster"
  default     = "myaks"
}

variable "node_count" {
  description = "Number of nodes in the AKS cluster"
  default     = 2
}

variable "vm_size" {
  description = "Size of the VMs in the AKS cluster"
  default     = "Standard_DS2_v2"
}
{% endhighlight %}

# Initialize Terraform

Run the `terraform init` command to initialize your Terraform project and download the necessary provider plugins:

{% highlight shell %}
$ terraform init
{% endhighlight %}

# Apply the Terraform Configuration

Run the `terraform apply` to create the resources defined in your configuration:

{% highlight shell %}
$ terraform apply
{% endhighlight %}

Review the changes and type "yes" when prompted to apply them. This step might take a few minutes to complete. Once done, Terraform will output the kubeconfig information.

# Connect to the AKS Cluster
Save the kubeconfig output from the previous step to a file, and set the `KUBECONFIG` environment variable to use it:

{% highlight shell %}
$ echo "$(terraform output kubeconfig)" > kubeconfig.yaml
$ export KUBECONFIG=kubeconfig.yaml
{% endhighlight %}

Now, you can use kubectl to interact with your AKS cluster:

{% highlight shell %}
$ kubectl get nodes
{% endhighlight %}

This command will show the nodes in your AKS cluster.

# Clean Up Resources

When you no longer need the AKS cluster, you can destroy the resources using Terraform:

{% highlight shell %}
$ terraform destroy
{% endhighlight %}

Type "yes" when prompted to confirm that you want to destroy the resources.

# Conclusion

This tutorial taught you how to create an Azure Kubernetes Service (AKS) cluster using Terraform. By leveraging Infrastructure as Code, you can maintain consistent environments, collaborate more effectively, and ensure repeatability across deployments. In addition, you can further enhance your Terraform configuration by adding more resources and customizing your AKS cluster to suit your application requirements.

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
* [Building an EKS Cluster on AWS with Terraform: A Step-by-Step Guide](/building-an-eks-cluster-on-aws-with-terraform): Spin an Amazon EKS cluster effortlessly using Terraform, following our detailed step-by-step guide.
* [Create a GKE Cluster on Google Cloud Platform using Terraform](/create-a-gke-cluster-on-google-cloud-platform-using-terraform): Create and manage a GKE cluster on Google Cloud Platform with ease using Terraform's automation features.

Embrace the power of Terraform and Infrastructure as Code with this comprehensive collection of articles, and enhance your skills in deploying, managing, and maintaining your infrastructure.