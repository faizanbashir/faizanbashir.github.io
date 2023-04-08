---
layout: post
comments: true
current: post
cover:  assets/images/posts/chris-paul-fXa3v3Vco4o-unsplash_resized.webp
navigation: True
title: "Building an Elasticache cluster on AWS using Terraform Modules"
date: 2022-04-11 03:13:01
tags: [Terraform]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: This article is a practical implementation of Terraform Modules for building an ElastiCache cluster on AWS.
---
This article is a practical implementation of Terraform Modules for building an ElastiCache cluster on AWS. Building on the previous article, I had written as an introduction to Terraform Modules.

To demonstrate how modules work in real life, we'll be building an ElastiCache cluster for multiple environments like dev, staging and production. To create the same using modules, we would have to write a separate dev, stage and production configuration in Terraform. Although this would be a laborious activity with a likelihood of discrepancies in the configurations of the three environments, using Terraform modules would ensure that the base configuration for the cluster would always be the same, thereby enabling us to maintain dev-prod parity.

# Defining the Folder Structure

In building the ElastiCache module, we need to define the folder and file structure where we will store our module files. For instance, the folder structure would look something like the one given below:

{% highlight shell %}
.
+-- elasticache
¦   +-- main.tf
¦   +-- variables.tf
+-- environments
¦   +-- dev
¦   ¦ +-- main.tf
¦   +-- production
¦   ¦ +-- main.tf
¦   +-- staging
¦       +-- main.tf
+-- main.tf
+-- provider.tf
{% endhighlight %}

The folder named `elasticache` will be the place we'll use to store the `main.tf` and `variables.tf` files comprising the configuration for the `elasticache` cluster. The `environments` folder has the folders corresponding to the environment names. The `main.tf` file will use the `elasticache` module and update the properties based on the need of the environment in question. The environments will be used as environments in the root `main.tf` file. Finally, the cloud provider for our project is defined using the `provider.tf`, which happens to be `aws` in our case.

# Writing the Reusable Module

To use a module between multiple environments, first, we need to write a reusable terraform `elasticache` module.

Before we define the elasticache module, we need to write the variables that will be used by the `elasticache` module, using the following configuration in the `elasticache/variables.tf` file:

{% highlight hcl %}
variable "environment" {}
variable "node_count" {}
variable "node_type" {}
variable "availability_zones" { type = "list" }
{% endhighlight %}

The `elasticache/main.tf` file contains the configuration for the elasticache module as defined below:

{% highlight hcl %}
resource "aws_elasticache_replication_group" "elasticache-cluster" {
  availability_zones            		= ["${var.availability_zones}"]
  replication_group_id          		= "tf-${var.environment}-rep-group"
  replication_group_description 	= "${var.environment} replication group"
  node_type                     		= "${var.node_type}"
  number_cache_clusters         	= "${var.node_count}"
  parameter_group_name          	= "default.redis3.2"
  port                          			= 6379
}
{% endhighlight %}

# Writing the Modules for Environments

Now that we have defined our elasticache module, we can create the modules for the dev, stage and production environments. We have previously described a folder environment for the same, and under the folder, we have created folders with the names of the environments. In each of the folders, we'll have a `main.tf` file that uses the `elasticache` module and later, we will use these modules in the `main.tf` file present in the root.

First, we will define the dev `elasticache` cluster in the `environment/dev` folder in a `main.tf` file, with the following configuration:

{% highlight hcl %}
module "dev-elasticache" {
  source             	= "../../elasticache"
  environment        	= "dev"
  node_count         	= 1
  node_type          	= "cache.m3.medium"
  availability_zones = ["us-east-1a", "us-east-1b"]
}
{% endhighlight %}

We have named the module `dev-elasticache`, the `source` points to the `elasticache` folder, and we set the values for the `environment`, `node_count`, `node_type`, and `avaiability_zones` as per the requirements of the dev environment.

Next up, we'll define the staging `elasticache` cluster in the `environment/staging` folder in a `main.tf` file, with the following configuration:

{% highlight hcl %}
module "staging-elasticache" {
  source             	= "../../elasticache"
  environment        	= "dev"
  node_count         	= 2
  node_type          	= "cache.m3.medium"
  availability_zones = ["us-east-1a", "us-east-1b"]
}
{% endhighlight %}

We have named the module staging-elasticache. The source points to the elasticache folder. The `environment`, `node_count`, `node_type`, and `avaiability_zones` are values set at the staging environment's requirements.

Next up, we'll define the production `elasticache` cluster in the `environment/production` folder in a `main.tf` file, with the following configuration:

{% highlight hcl %}
module "production-elasticache" {
  source             	= "../../elasticache"
  environment        	= "dev"
  node_count         	= 3
  node_type          	= "cache.m3.large"
  availability_zones = ["us-east-1a", "us-east-1b"]
}
{% endhighlight %}

We have named the module `production-elasticache`, the source points to the `elasticache` folder, and we set the values of the `environment`, `node_count`, `node_type`, and `avaiability_zones` as per the requirements of the production environment.

# Using the Modules in the root `main.tf`

We have defined the modules, and now we can use the modules in our `main.tf` file located at the directory's root. We can define the `main.tf` file as given below:

{% highlight hcl %}
module "dev" {
  source = "environments/dev"
}

module "staging" {
  source = "environments/staging"
}

module "production" {
  source = "environments/production"
}
{% endhighlight %}

Finally, we need to define the provider in our `providers.tf` file with the following configuration:

{% highlight hcl %}
provider "aws" {
  profile   = "${var.aws_cred_profile}"
  region    = "${var.aws_region}"
}
{% endhighlight %}

With a little effort, we can restructure Terraform code from the beginning so that a growing code base won't bring growing pains. Writing reusable and configurable modules are one of the basic building blocks of clean, readable and scalable Terraform code. Writing modules would help us better manage a growing code base and reduce useless repetition in code.

You can find the codebase supporting this article on Github [AWS ElastiCache Terraform Module](https://github.com/faizanbashir/aws-elasticache-terraform-module).
