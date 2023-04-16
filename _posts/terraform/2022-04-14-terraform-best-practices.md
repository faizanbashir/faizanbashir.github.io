---
layout: post
comments: true
current: post
cover:  assets/images/posts/florian-giorgio-KdbeXNzZhB0-unsplash_resized.webp
navigation: True
title: "Terraform Best Practices"
date: 2022-04-14 03:13:02
tags: [Terraform]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: In this article, I have attempted to gather the Best Practices that an engineer can adhere to while writing Terraform code.
---
There are many ways to build infrastructure in public using Terraform. In this article, I have attempted to gather the Best Practices that an engineer can adhere to while writing Terraform code. By following these best practices, the resultant codebase can be easily manageable, reusable, and modular.

***
# Table of Contents:

* [Defining the folder structure](#defining-the-folder-structure)
* [Isolate Environments](#isolate-environments)
* [Using Terraform Workspaces](#using-terraform-workspaces)
  * [What is a Terraform Workspace?](#what-is-a-terraform-workspace)
  * [Terraform Workspaces in Practice](#terraform-workspaces-in-practice)
    * [Creating Workspaces for environments](#creating-workspaces-for-environments)
    * [Creating a workspace from an existing state file](#creating-a-workspace-from-an-existing-state-file)
    * [Display the current workspace](#display-the-current-workspace)
    * [List all available workspaces](#list-all-available-workspaces)
    * [How to switch workspaces](#how-to-switch-workspaces)
    * [Remove a workspace](#remove-a-workspace)
* [Proper Naming Convention](#proper-naming-convention)
* [Using Shared Modules](#using-shared-modules)
* [Upgrading to the Latest Version of Terraform](#upgrading-to-the-latest-version-of-terraform)
* [Backup System State](#backup-system-state)
* [Validate and Format Terraform Code](#validate-and-format-terraform-code)
* [Lock State File](#lock-state-file)
* [Generate documentation with terraform-docs](#generate-documentation-with-terraform-docs)
* [Using the self Variable](#using-the-self-variable)
* [Minimize Blast Radius](#minimize-blast-radius)
* [Using -var-file flag](#using-the--var-file-flag)
* [Dive Deeper: Recommended Reads](#dive-deeper-recommended-reads)

***

# Defining the folder structure

It is important to lay down a proper folder structure for our terraform code to get the most out of it. Here we will look at the folder structure we followed in the article [Building highly available VMSS on Azure using Terraform Modules](https://faizanbashir.me/building-highly-available-vmss-on-azure-using-terraform-modules). The `modules` folder contains the modules within each sub folder named after the name of the `module/function` that it would perform. Each module would have a `main.tf`, `outputs.tf` and `variables.tf` files. The environments folder stores the environment-specific configuration. In this example, we have a dev, stage and prod environment, each with a `<environment-name>.tfvars` file to store the override values. Finally, in the root module, we have the `main.tf`, `backend.tf`, `terraform.tfvars`, `outputs.tf` and `variables.tf` files. The folder structure would look something like the one given below:

{% highlight shell %}
.
+-- modules
¦   +-- subnet
¦   ¦ +-- main.tf
¦   ¦ +-- outputs.tf
¦   ¦ +-- variables.tf
¦   +-- vmss
¦   ¦ +-- main.tf
¦   ¦ +-- outputs.tf
¦   ¦ +-- variables.tf
¦   +-- vnet
¦   ¦ +-- main.tf
¦   ¦ +-- outputs.tf
¦   ¦ +-- variables.tf
+-- environments
¦   +-- dev
¦   ¦ +-- dev.tfvars
¦   +-- prod
¦   ¦ +-- prod.tfvars
¦   +-- stage
¦   ¦ +-- test.tfvars
+-- scripts
¦   +-- init.sh
+-- main.tf
+-- outputs.tf
+-- variables.tf
+-- terraform.tfvars
{% endhighlight %}

For this example, we will use the folder called `modules` as a container for all the separate modules we will use throughout this article. The folder named `vnet` will be the place we'll use to store the `main.tf`, `output.tf`, and `variables.tf` files which hold the configuration for the `vnet` that the rest of the resources will use. Likewise, a `subnet` folder will be hosting similar files to our `vnet` folder. The `subnet` module will create the subnet(s) that the resources will use. Finally, we have the `vmss` folder that holds the configuration for the Azure Virtual Machine Scale Set. Within it, we create the required resources like public IP, load balancers, an address pool, lb health check probe and rules to expose the ports on the load balancer. The environments folder has the folders corresponding to the environment names; we will use the `<environment-name>.tfvars` files to create the resources based on the environment in question. The environment configuration in the `tfvars` files in the `environment` folders will be used in the commands like `plan` and `apply` to override the `terraform.tfvars` stored in the root module. The `backend.tf` defines our cloud provider for the project. Since we are using Microsoft Azure for this illustration, our provider name will be `azurerm`. We will be using the `required_version` and `required_providers` to define the proper versions.

# Isolate Environments

Sometimes, developers like to create a security group and share it with all non-prod (dev/QA) environments. It is better to create resources with different names for each environment and each resource.

{% highlight hcl %}
variable "application" {
  description = "application name"
  default = "<replace_with_your_project_or_application_name, use short name if possible, because some resources have length limit on its name>"
}

variable "environment" {
  description = "environment name"
  default = "<replace_with_environment_name, such as dev, svt, prod,etc. Use short name if possible, because some resources have length limit on its name>"
}

locals {
  name_prefix    = "${var.application}-${var.environment}"
}

resource "<any_resource>" "custom_resource_name" {
  name = "${local.name_prefix}-<resource_name>"
  ...
}
{% endhighlight %}

With that, we will quickly define the resource with a meaningful and unique name, and we can build more of the same application stack for different developers without changing a lot. For example, we update the environment to dev, staging, QA, prod, etc.

Some cloud providers have resource names with length limits, such as less than 24 characters, so it is better to use a short name when defining variables for our application and environment name.

# Using Terraform Workspaces

Workspaces each have state files, and as such, they provide isolation between them. When working in one workspace, changes will not affect resources in another workspace. When managing separate environments and large deployments, this separation is critical for peace of mind.

## What is a Terraform Workspace?

We can think of workspaces as a layer of isolation for Terraform state files. Every workspace has its state file. All modifications applied in a particular workspace will never affect resources managed by another. Workspaces are the key to managing multiple independent environments using a single Terraform project.

We can use the current workflow's name in our configuration files by using the `terraform.workspace` variable when using workspaces in Terraform.

A fairly common use case is to create scoped names for resources. For example, consider using Terraform to provision an Azure Resource Group. Azure enforces a unique name constraint on Resource Groups in the context of your Azure subscription. (We can have only one Resource Group with the name cool-product). By appending the name of the current workspace (e.g. dev, test, or prod), we enforce the unique name constraint.

## Terraform Workspaces in Practice

### Creating Workspaces for environments

Every Terraform project comes with a workspace out of the box. When we execute the `terraform init`, Terraform implicitly creates a new workspace. The name of this workspace is always `default`. However, we can quickly create a custom workspace using the terraform workspace the `new` command:

{% highlight shell %}
# create three new workspace
terraform workspace new dev
terraform workspace new stage
terraform workspace new prod
{% endhighlight %}

### Creating a workspace from an existing state file

You can bring in workspaces also for existing Terraform projects. For example, if we already have a state file, use the state option to copy the existing state into the new workspace.

{% highlight shell %}
# create a new workspace and pass existing state file
terraform workspace new -state=terraform.tfstate dev
{% endhighlight %}

### Display the current workspace

To know which workspace we are currently interacting with, execute `terraform workspace show`. Terraform will quickly print the name of the current workspace.

{% highlight shell %}
# get the name of the current workspace
terraform workspace show
prod
{% endhighlight %}

### List all available workspaces
We can list the available workspaces using the `list` sub-command:

{% highlight shell %}
# list all workspaces
terraform workspace list

default
dev
stage
prod
{% endhighlight %}

### How to switch workspaces

Switching to a different namespace is super easy in Terraform. Just execute the `terraform workspace select` command, followed by the name of the desired workspace.

{% highlight shell %}
# switch to the dev workspace
terraform workspace select dev

terraform workspace show
dev
{% endhighlight %}

### Remove a workspace

Sometimes, we want to remove a specific workspace. The sub-command `delete` is responsible for that. But, first, delete the staging environment and check the list of remaining workspaces. There is only one exception; we can not delete the `default` namespace.

{% highlight shell %}
# delete the staging workspace
terraform workspace delete stage

terraform workspace list

default
dev
prod
{% endhighlight %}

# Proper Naming Convention

Naming conventions are used in Terraform to make things easily understandable.

For example, let's say we want to make three different workspaces for different environments in a project. So, rather than naming them env1, en2, or env3, we should call them a dev, stage, or prod. From the name, it becomes clear that three different workspaces exist for each environment.

A proper naming convention should be followed for resources, variables, modules, etc. For example, the resource name in Terraform should start with a provider name followed by an underscore and other details.

For example, the resource name for creating a terraform object for a Public IP in Azure would be `azurerm_public_ip`.

So, if we follow the naming conventions right, it will be easier to understand even complex codes.

# Using Shared Modules

Using the official Terraform modules available is strongly suggested. No need to reinvent a module that already exists. It saves a lot of time and pain. Terraform registry has plenty of modules readily available. Make changes to the existing modules as per the need.

Also, each module should concentrate on only one aspect of the infrastructure, such as creating an Azure Virtual Machine instance, setting MySQL database, etc.

For example, if you want to use Azure VNet in your terraform code, we can use:

{% highlight hcl %}
module "vnet_example" {
  source = "Azure/vnet/azurerm" 
  version = "2.4.0"
}
{% endhighlight %}

# Upgrading to the Latest Version of Terraform

The Terraform development community is active, and new functionalities are released frequently. Therefore, staying on the latest version of Terraform is recommended when a new major release happens. You can easily upgrade to the latest version.

If you skip multiple major releases, upgrading will become very complex.

Execute the `terraform -v` command to check for a new update.

{% highlight shell %}
terraform -v 
Terraform v0.11.14
{% endhighlight %}

Your version of Terraform is out of date! The latest version is 0.12.0. You can update by [downloading Terraform](www.terraform.io/downloads.html)

# Backup System State

Always backup the state files of Terraform.

These files keep track of the metadata and resources of the infrastructure. By default, these files called `terraform.tfstate` are stored locally inside the workspace directory.

Terraform cannot determine the resources deployed on the infrastructure without these files. So, it is essential to have a backup of the state file. So, the `terraform.tfstate.backup` will be created to keep a backup of the state file.

{% highlight shell %}
tree terraform_demo/
terraform_demo/
├── main.tf 
├── terraform.tfstate 
└── terraform.tfstate.backup 0 directories, 3 files
{% endhighlight %}

If you want to store a backup state file in another location, use the `-backup` flag in the terraform command and give the location path.

Most of the time, multiple developers will work on a project. So, to give them access to the state file, it should be stored at a remote location using a `terraform_remote_state` data source.

The following example will take a backup to the Storage Account.

{% highlight hcl %}
data "terraform_remote_state" "foo" {
  backend = "azurerm"
  config = {
    storage_account_name = "remote_state_store"
    container_name       = "terraform-state"
    key                  = "prod.terraform.tfstate"
  }
}
{% endhighlight %}

# Validate and Format Terraform Code

Consistently execute the `terraform fmt` command to format Terraform configuration files and make them neat.

We can use the code below in a Travis CI pipeline (you can re-use it in any pipelines) to validate and format check the code before we can merge it with the `master` branch.

{% highlight yaml %}
script:
  - terraform validate
  - terraform fmt -check=true -write=false -diff=true
  terraform
{% endhighlight %}

# Lock State File

There can be multiple scenarios where more than one developer tries to run the terraform configuration simultaneously. Such a scenario can lead to the corruption of the terraform state file or even data loss. The locking mechanism helps to prevent such scenarios. It makes sure that at a time, only one person is running the terraform configurations, and there is no conflict.

Here is an example of locking the state file at a remote location in Azure.

{% highlight hcl %}
terraform {
  backend "azurerm" {
    resource_group_name   = "tstate"
    storage_account_name  = "tstate09762"
    container_name        = "tstate"
    key                   = "terraform.tfstate"
  }
}
{% endhighlight %}

When multiple users try to access the state file, Azure Storage Account will be used for state locking and maintaining consistency.

*Note: not all backend support locking.*

# Generate documentation with terraform-docs

We need not manually manage the usage of input variables and outputs. Instead, a tool named terraform-docs can do the job for us.

Currently, the original terraform-docs don't support Terraform `0.12+`. Follow this [Github issue for updating](https://github.com/segmentio/terraform-docs/issues/62).

Now we have a workaround.

{% highlight shell %}
# [Terraform >= 0.12]
docker run --rm \
  -v $(pwd):/data \
  cytopia/terraform-docs \
  terraform-docs-012 --sort-inputs-by-required --with-aggregate-type-defaults md . > README.md
{% endhighlight %}

For details on how to run terraform-docs, check this [repository](https://github.com/cytopia/docker-terraform-docs).

# Using the `self` Variable

The `self` variable is a special variable used when you don't know the variable's value before deploying an infrastructure.

Let's say you want to use the IP address of an instance which will be deployed only after the `terraform apply` command, so you don't know the IP address until it is up and running.

In such cases, you use self variables, and the syntax to use it is `self.ATTRIBUTE`. So, in this case, you will use `self.ipv4_address` as a self variable to get the IP address of the instance. 

These variables are only allowed on connection and provisioner blocks of terraform configuration.

{% highlight hcl %}
connection {
  host = self.ipv4_address
  type = "ssh" user = var.users[2]
  private_key = file(var.private_key_path)
}
{% endhighlight %}

# Minimize Blast Radius

The blast radius is nothing but the measure of damage that can happen if things do not go as planned.

For example, what will be the amount of damage to the infrastructure if you are deploying some terraform configurations on the infrastructure and the configuration does not get applied correctly.

To minimize the blast radius, I suggest pushing a few configurations on the infrastructure at a time. So, if something goes wrong, the damage to the infrastructure will be minimal and can be corrected quickly. However, deploying plenty of configurations at once is very risky.

# Using the `-var-file` flag

Next, let's run a `plan` of our infrastructure to see the final Terraform plan once we apply the code. There, however, is an extra variable we need to pass in called the `-var-file`. This argument takes the tfvars file based on the environment we selected:

{% highlight shell %}
terraform plan -var-file environments/dev/dev.tfvars
{% endhighlight %}

Finally, let's apply the infrastructure using the apply sub-command:

{% highlight shell %}
terraform apply -var-file environments/dev/dev.tfvars
{% endhighlight %}

# Dive Deeper: Recommended Reads

Expand your knowledge of Infrastructure as Code and Terraform with our insightful collection of articles! Dive into a range of topics that will help you master the art of managing infrastructure:

* [Managing environments through Terraform Workspaces](/managing-environments-through-terraform-workspaces): Discover how to manage multiple environments with ease.
* [Building highly available VMSS on Azure using Terraform Modules](/building-highly-available-vmss-on-azure-using-terraform-modules): Create scalable and highly available virtual machine scale sets on Azure.
* [Building an Elasticache cluster on AWS using Terraform Modules](/building-an-elasticache-cluster-on-aws-using-terraform-modules): Harness the power of AWS Elasticache with Terraform.
* [Demystifying Terraform Modules](/demystifying-terraform-modules): Understand the ins and outs of Terraform modules.
* [Building an Nginx webserver on Azure using Terraform](/building-an-nginx-webserver-on-azure-using-terraform): Deploy a reliable Nginx webserver on Azure.
* [Building an Nginx webserver on AWS using Terraform](/building-an-nginx-webserver-on-aws-using-terraform): Set up an Nginx webserver on AWS with Terraform.
* [Introduction to Infrastructure as Code (IaC)](/introduction-to-infrastructure-as-code): Get started with Infrastructure as Code and grasp the fundamentals.
* [Deploying an Azure Kubernetes Service (AKS) Cluster with Terraform](/deploying-an-azure-kubernetes-service-aks-cluster-with-terraform): Deploy an Azure Kubernetes Service (AKS) cluster seamlessly with Terraform's infrastructure management capabilities.
* [Effortlessly Spin Up an EKS Cluster on AWS with Terraform: A Step-by-Step Guide](/effortlessly-spin-up-an-eks-cluster-on-aws-with-terraform): Spin up an Amazon EKS cluster effortlessly using Terraform, following our detailed step-by-step guide.
* [Create a GKE Cluster on Google Cloud Platform using Terraform](/create-a-gke-cluster-on-google-cloud-platform-using-terraform): Create and manage a GKE cluster on Google Cloud Platform with ease using Terraform's automation features.

Embrace the power of Terraform and Infrastructure as Code with this comprehensive collection of articles, and enhance your skills in deploying, managing, and maintaining your infrastructure.