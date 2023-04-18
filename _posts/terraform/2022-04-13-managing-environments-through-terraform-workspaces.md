---
layout: post
comments: true
current: post
cover:  assets/images/posts/enrapture-captivating-media-AFqhe5VAXt0-unsplash_resized.webp
navigation: True
title: "Managing environments through Terraform Workspaces"
date: 2022-04-13 03:13:02
tags: [Terraform]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: This article explains the usage of Terraform modules and how they make it easier to substitute repetitive tasks with Modules.
---
# Terraform Workspaces

Terraform Workspaces provide the ability to have separate state files for environments. Separating the state files provides isolation between multiple environments. While working in one workspace, changes are committed to the state file of a single environment. Therefore, they do not affect resources in another workspace. When managing separate environments and large deployments, this separation is critical for peace of mind.

# What is a Terraform Workspace?

We can think of workspaces as a layer of isolation for Terraform state files. Every workspace has its state file. All modifications applied in a particular workspace will never affect resources managed by another. Workspaces are the key to managing multiple independent environments using a single Terraform project.

We can use the current workflow's name in our configuration files by using the `terraform.workspace` variable when using workspaces in Terraform.

A fairly common use case is to create scoped names for resources. For example, consider using Terraform to provision an Azure Resource Group. Azure enforces a unique name constraint on Resource Groups in the context of your Azure subscription. (We can have only one Resource Group with the name cool-product). By adding the name of the current workspace (e.g. dev, test, or prod), we enforce the unique name constraint.

# Terraform Workspaces in Practice

## Creating Workspaces for environments

Every Terraform project comes with a workspace out of the box. When we execute the `terraform init`, Terraform implicitly creates a new workspace. The name of this workspace is always `default`. However, we can quickly create a custom workspace using the `terraform workspace new` command:

{% highlight hcl %}
# create three new workspace
terraform workspace new dev
terraform workspace new test
terraform workspace new prod
{% endhighlight %}

## Create a workspace from an existing state file

You can bring in workspaces also for existing Terraform projects. For example, if we already have a state file, use the state option to copy the existing state into the new workspace.

{% highlight hcl %}
# create a new workspace and pass existing state file
terraform workspace new -state=terraform.tfstate dev
{% endhighlight %}

## Display the current workspace

To know which workspace we are currently interacting with, execute `terraform workspace show`. Terraform will quickly print the name of the current workspace.

{% highlight hcl %}
# get the name of the current workspace
terraform workspace show
prod
{% endhighlight %}

## List all available workspaces

We can list the available workspaces using the `list` sub-command:

{% highlight hcl %}
# list all workspaces
terraform workspace list

default
dev
test
prod
{% endhighlight %}

## How to switch workspace
Switching to a different namespace is super easy in Terraform. Just execute the `terraform workspace select` command, followed by the name of the desired workspace.

{% highlight hcl %}
# switch to the dev workspace
terraform workspace select dev

terraform workspace show
dev
{% endhighlight %}

## Remove a workspace

Sometimes, we want to remove a specific workspace. The sub-command `delete` is responsible for that. But, first, delete the `staging` environment and check the list of remaining workspaces. There is only one exception; we can not delete the `default` namespace.

{% highlight hcl %}
# delete the staging workspace
terraform workspace delete test

terraform workspace list

default
dev
prod
{% endhighlight %}

## Creating the Infrastructure

Finally, let's get hands-on and create the infrastructure from our written code. Initially, we need to initialize the project using the `init` subcommand, like so:

{% highlight hcl %}
terraform init
{% endhighlight %}

The init command will install the required dependencies for our project like the cloud provider, plugins, etc.

Next up, we need to switch to the correct environment. For example, let's change the `dev` environment for illustration:

{% highlight hcl %}
terraform workspace select dev
{% endhighlight %}

Next, let's run a plan of our infrastructure to see what resources will be created once we apply the code, there however is an extra variable we need to pass in called the `-var-file`. This argument takes the `tfvars` file based on the environment we selected:

{% highlight hcl %}
terraform plan -var-file environments/dev/dev.tfvars
{% endhighlight %}

Finally, let's apply the infrastructure using the `apply` sub-command:

{% highlight hcl %}
terraform apply -var-file environments/dev/dev.tfvars
{% endhighlight %}

# Dive Deeper: Recommended Reads

Expand your knowledge of Infrastructure as Code and Terraform with our insightful collection of articles! Dive into a range of topics that will help you master the art of managing infrastructure:

* [Terraform Best Practices](/terraform-best-practices): Learn the most effective ways to use Terraform in your projects.
* [Building highly available VMSS on Azure using Terraform Modules](/building-highly-available-vmss-on-azure-using-terraform-modules): Create scalable and highly available virtual machine scale sets on Azure.
* [Building an Elasticache cluster on AWS using Terraform Modules](/building-an-elasticache-cluster-on-aws-using-terraform-modules): Harness the power of AWS Elasticache with Terraform.
* [Demystifying Terraform Modules](/demystifying-terraform-modules): Understand the ins and outs of Terraform modules.
* [Building an Nginx web server on Azure using Terraform](/building-an-nginx-webserver-on-azure-using-terraform): Deploy a reliable Nginx web server on Azure.
* [Building an Nginx web server on AWS using Terraform](/building-an-nginx-webserver-on-aws-using-terraform): Set up an Nginx web server on AWS with Terraform.
* [Introduction to Infrastructure as Code (IaC)](/introduction-to-infrastructure-as-code): Get started with Infrastructure as Code and grasp the fundamentals.
* [Deploying an Azure Kubernetes Service (AKS) Cluster with Terraform](/deploying-an-azure-kubernetes-service-aks-cluster-with-terraform): Deploy an Azure Kubernetes Service (AKS) cluster seamlessly with Terraform's infrastructure management capabilities.
* [Building an EKS Cluster on AWS with Terraform: A Step-by-Step Guide](/building-an-eks-cluster-on-aws-with-terraform): Spin an Amazon EKS cluster effortlessly using Terraform, following our detailed step-by-step guide.
* [Create a GKE Cluster on Google Cloud Platform using Terraform](/create-a-gke-cluster-on-google-cloud-platform-using-terraform): Create and manage a GKE cluster on Google Cloud Platform with ease using Terraform's automation features.

Embrace the power of Terraform and Infrastructure as Code with this comprehensive collection of articles, and enhance your skills in deploying, managing, and maintaining your infrastructure.