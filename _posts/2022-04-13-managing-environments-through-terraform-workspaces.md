---
layout: post
comments: true
current: post
cover:  assets/images/posts/enrapture-captivating-media-AFqhe5VAXt0-unsplash.jpg
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

Workspaces each have state files, and as such, they provide isolation between them. When working in one workspace, changes will not affect resources in another workspace. This separation is critical for peace of mind when managing separate environments and large deployments.

# What is a Terraform Workspace?

We can think of workspaces as a layer of isolation for Terraform state files. Every workspace has its state file. All modifications applied in a particular workspace will never affect resources managed by another workspace. Workspaces are the key to manage multiple independent environments using a single Terraform project.

When using workspaces in Terraform, we can use the current workflow’s name in our configuration files, by using the terraform.workspace variable.

A fairly common use case is to create scoped names for resources. Consider using Terraform to provision an Azure Resource Group. Azure enforces a unique name constraint on Resource Groups in the context of your Azure subscription. (We can have only one Resource Group with the name cool-product). By adding the name of the current workspace (e.g. dev, test, or prod), we enforce the unique name constraint.

# Terraform Workspaces in Practice

## Creating Workspaces for environments
Every Terraform project comes with a workspace out of the box. When we execute the terraform init, Terraform implicitly creates a new workspace. The name of this workspace is always default. However, we can quickly create a custom workspace using the terraform workspace new command:

{% highlight hcl %}
# create three new workspace
terraform workspace new dev
terraform workspace new test
terraform workspace new prod
{% endhighlight %}

## Create a workspace from an existing state file
You can bring in workspaces also for existing Terraform projects. If we already have a state file, use the state option to copy the existing state into the new workspace.

{% highlight hcl %}
# create a new workspace and pass existing state file
terraform workspace new -state=terraform.tfstate dev
{% endhighlight %}

## Display the current workspace
To know which workspace we are currently interacting with, execute terraform workspace show. Terraform will quickly print the name of the current workspace.

{% highlight hcl %}
# get the name of the current workspace
terraform workspace show
prod
{% endhighlight %}

## List all available workspaces
We can list the available workspaces using the list sub-command:

{% highlight hcl %}
# list all workspaces
terraform workspace list

default
dev
test
prod
{% endhighlight %}

## How to switch workspace
Switching to a different namespace is super easy in Terraform. Just execute the terraform workspace select command, followed by the name of the desired workspace.

{% highlight hcl %}
# switch to the dev workspace
terraform workspace select dev

terraform workspace show
dev
{% endhighlight %}

## Remove a workspace
Sometimes, we want to remove a specific workspace. The sub-command delete is responsible for that. Delete the staging environment and check the list of remaining workspaces. There is only one exception; we can not delete the default namespace.

{% highlight hcl %}
# delete the staging workspace
terraform workspace delete test

terraform workspace list

default
dev
prod
{% endhighlight %}

## Creating the Infrastructure
Finally let's get hands on and create the infrastructure from the code that we wrote so far. Initially we need to initialize the project using the init sub-command, like so:

{% highlight hcl %}
terraform init
{% endhighlight %}

The init command will install the required dependencies for our project like the cloud provider, plugins, etc.

Next up we need to switch to the correct environment for example let’s switch to the dev environment for illustration:

{% highlight hcl %}
terraform workspace select dev
{% endhighlight %}

Next let’s run a plan of our infrastructure to see what resources will be created once we apply the code, there however is an extra variable we need to pass in called the -var-file, this argument takes the tfvars file based on the environment we selected:

{% highlight hcl %}
terraform plan -var-file environments/dev/dev.tfvars
{% endhighlight %}

Finally let’s apply the infrastructure using the apply sub-command:

{% highlight hcl %}
terraform apply -var-file environments/dev/dev.tfvars
{% endhighlight %}