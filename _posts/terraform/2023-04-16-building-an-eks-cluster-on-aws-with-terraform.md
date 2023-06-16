---
layout: post
comments: true
current: post
cover: assets/images/posts/mihaly-koles-FodEb_8qfdg-unsplash_resized.webp
navigation: True
title: "Building an EKS Cluster on AWS with Terraform: A Step-by-Step Guide"
date: 2023-04-16 03:13:02
tags: [Terraform, AWS]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: Learn how to create an Amazon EKS cluster using Terraform in this comprehensive, step-by-step tutorial with real-world code examples.
---

# Building an EKS Cluster on AWS with Terraform

Elastic Kubernetes Service (EKS) is a fully managed Kubernetes service provided by AWS. It helps users to deploy, manage, and scale containerized applications using Kubernetes. This article will walk you through creating an Amazon EKS cluster using Terraform, a widespread Infrastructure as Code (IaC) tool. Then, you'll learn how to define, provision, and manage your Kubernetes infrastructure in a declarative and reproducible way.

# Prerequisites

Before we start, ensure you have the following:

1. An AWS account
2. AWS CLI installed and configured
3. Terraform installed (v0.12+)

***
# Table of Contents:

* [Initialize your Terraform project](#initialize-your-terraform-project)
* [Define the EKS cluster resources](#define-the-eks-cluster-resources)
* [Provision worker nodes](#provision-worker-nodes)
* [Initialize and apply your Terraform configuration](#initialize-and-apply-your-terraform-configuration)
* [Connecting to the EKS Cluster](#connecting-to-the-eks-cluster)
* [Clean Up](#clean-up)
* [Conclusion](#conclusion)
* [Dive Deeper: Recommended Reads](#dive-deeper-recommended-reads)

***

# Initialize your Terraform project

First, create a new directory for your Terraform configuration files:

{% highlight shell %}
$ mkdir terraform-eks
$ cd terraform-eks
{% endhighlight %}

Next, create a `main.tf` file in the project directory and add the AWS provider:

{% highlight hcl %}
provider "aws" {
  region = "us-west-2"
}
{% endhighlight %}

# Define the EKS cluster resources

In your `main.tf` file, add the following resources:

{% highlight hcl %}
locals {
  cluster_name = "my-eks-cluster"
}

resource "aws_eks_cluster" "this" {
  name = local.cluster_name

  vpc_config {
    subnet_ids = aws_subnet.private.*.id
  }
}

resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Terraform = "true"
    Kubernetes = "true"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }
}

resource "aws_subnet" "private" {
  count = 2

  cidr_block = "10.0.${count.index + 1}.0/24"

  tags = {
    Terraform = "true"
    Kubernetes = "true"
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  }
}
{% endhighlight %}

This configuration creates a new VPC, subnets, and an EKS cluster within the specified VPC.

# Provision worker nodes

Create an AWS Auto Scaling group to launch worker nodes for your EKS cluster. Add the following to your `main.tf`:

{% highlight hcl %}
module "eks" {
  source = "terraform-aws-modules/eks/aws"

  cluster_name = local.cluster_name
  subnets      = aws_subnet.private.*.id

  tags = {
    Terraform = "true"
    Kubernetes = "true"
  }

  vpc_id = aws_vpc.this.id

  node_groups_defaults = {
    instance_type = "t2.small"
  }

  node_groups = {
    first_group = {
      desired_capacity = 2
      max_capacity     = 2
      min_capacity     = 1
    }
  }
}
{% endhighlight %}

This configuration defines a module that provisions worker nodes for your EKS cluster.

# Initialize and apply your Terraform configuration

Run `terraform init` to initialize your Terraform project and download the necessary provider plugins:

{% highlight shell %}
$ terraform init
{% endhighlight %}

Once the initialization is complete, run the `terraform apply` command to create the resources defined in your configuration:

{% highlight shell %}
$ terraform apply
{% endhighlight %}

Review the changes and type "yes" when prompted to apply the changes. This step might take a few minutes as Terraform creates the resources in AWS.

# Connecting to the EKS Cluster

Once the cluster is up and running, you must configure `kubectl`, the Kubernetes command-line tool, to interact with the EKS cluster. Next, use the AWS CLI to update your kubeconfig file:

{% highlight shell %}
$ aws eks update-kubeconfig --region us-west-2 --name my-eks-cluster
{% endhighlight %}

Now you can use kubectl to interact with your EKS cluster:

{% highlight shell %}
$ kubectl get nodes
{% endhighlight %}

# Clean up

When done using the EKS cluster, run `terraform destroy` to delete all the resources created by your Terraform configuration:

{% highlight shell %}
$ terraform destroy
{% endhighlight %}

Type "yes" when prompted to confirm the resource destruction. This step may take a few minutes as Terraform deletes the resources in AWS.

# Conclusion

In this article, you've learned how to create an Amazon EKS cluster using Terraform, a widespread Infrastructure as Code (IaC) tool. As a result, you can easily maintain and scale your containerized applications by defining, provisioning, and managing your Kubernetes infrastructure in a declarative and reproducible way.

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
* [Create a GKE Cluster on Google Cloud Platform using Terraform](/create-a-gke-cluster-on-google-cloud-platform-using-terraform): Create and manage a GKE cluster on Google Cloud Platform with ease using Terraform's automation features.

Embrace the power of Terraform and Infrastructure as Code with this comprehensive collection of articles, and enhance your skills in deploying, managing, and maintaining your infrastructure.