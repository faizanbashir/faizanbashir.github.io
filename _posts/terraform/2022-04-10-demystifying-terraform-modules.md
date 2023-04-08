---
layout: post
comments: true
current: post
cover:  assets/images/posts/bawah-reserve-MtHP4ydvZXA-unsplash_resized.webp
navigation: True
title: "Demystifying Terraform Modules"
date: 2022-04-10 03:13:00
tags: [Terraform]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: This article explains the usage of Terraform modules and how they make it easier to substitute repetitive tasks with Modules.
---
This article explains the usage of Terraform modules and how they make it easier to substitute repetitive tasks with Modules.

Terraform Modules provide us with a way which reuses a predefined module just like we do in any general-purpose programming language. With Terraform, we can put our code inside a Terraform module and reuse that module in multiple places throughout our code. Instead of using the same code copy-pasted in various environments like dev, staging and production. Using Terraform Modules, we can have all the environments reuse code from the same module.

Modules enable us to write DRY (Don't Repeat Yourself) code; thus, they are the key ingredient to writing reusable, maintainable, and testable Terraform code. Once we start using them, there's no going back :). We can build everything as a module, creating a library of modules to perform repetitive tasks. We can leverage modules published online in the Terraform Registry. These modules are called Published modules. After learning the use and benefits of modules, we can refactor our entire infrastructure as a collection of reusable modules.

# What is a Terraform Module?

We can think of the Terraform module is simply a set of Terraform configuration files bundled together in a folder. To see what modules are capable of, you have to use one module from another. Terraform provides modules which allow us to abstract away reusable parts, which we can configure once and use everywhere. Modules will enable us to group resources together, define input variables used to change needed resource configuration parameters, and define output variables that other resources or modules can use. Modules are like files with exposed input and output variables that facilitate reuse. If you know how to write Terraform code to deploy a Virtual Machine on AWS or Azure, the chances are that you don't need to do anything special to create a module. It is just like your terraform configuration, which runs independently. Modules can't inherit or reference parent resources. Instead, we need to pass them to the module as input variables explicitly. Modules are self-contained packages that engineers can reuse across teams for different projects.

Modules are a convenient way to package and reuse resource configurations with Terraform. Simply put, Modules are containers for multiple resources scoped together. For example, a module consists of a collection of `.tf` or`.tf.json` files in a directory for creating a set of Virtual Machines.

## Root Modules

All Terraform configurations contain at least one module, called the root module. The root module consists of the resources defined in the `.tf` files in the root working directory.

## Child Modules

A Terraform module (usually the root configuration module) can call other modules to include their resources in the configuration. A module referred to by another module is named child module.

We can call the Child modules multiple times within the same configuration, and various configurations can refer to the same child module.

## Published Modules

Terraform can load modules from a public or private registry, apart from the modules stored on the local filesystem. Since Modules can be shipped separately, this makes it possible to publish modules for public or private use, and engineers can benefit from modules that others have published.

The [Terraform Registry](https://registry.terraform.io/browse/modules) hosts a broad collection of publicly available Terraform modules for configuring many kinds of shared infrastructure on the public cloud. The modules hosted by the Terraform Registry are free to use. The Terraform CLI tool can download the module by specifying the version and source in the module configuration.

Members of an organization can create modules crafted explicitly for their own infrastructure needs. For example, [Terraform Cloud](https://www.terraform.io/docs/cloud/index.html) and [Terraform Enterprise](https://www.terraform.io/docs/enterprise/index.html) both include a private module registry for sharing modules internally within your organization.

# Terraform Modules Usage

## Blocks

All Terraform codebases have at least one module, called the root module consisting of the resources defined in the directory root of the project.

We can call a Terraform module from other modules. Calling a module from another module lets you include the child module's resources into the codebase. Modules can also be called multiple times within the same configuration or in separate configurations, allowing resource configurations to be packaged and reused.

When you add a `module`, the module's contents are added to the caller. Simply put, the resultant code would execute the configuration of the caller moduled and the child module. A Terraform Module can be called from within other modules using `module` blocks:

{% highlight hcl %}
module "servers" {
  source = "./app-cluster"

  servers = 5
}
{% endhighlight %}

The above example illustrates the use of calling a child module. In this example, the child module exists in the local filesystem in the `./app-clusters` directory.

A Module makes use of the following arguments:

* `source`: This argument is mandatory for all modules and refers to the module's location. The source can reference the local filesystem, the HTTP endpoint of the Terraform Registry, a Github repository or a self-hosted repository.
* `version`: This argument is recommended for modules from a registry and contains the module version.
* Most other arguments correspond to [input variables](https://www.terraform.io/docs/language/values/variables.html) defined by the `module`.
* A few other arguments can be used with all `modules`, including `for_each` and `depends_on`.

## Source

All modules require a `source` argument. The `source` argument can refer to the path in the local filesystem containing the module configuration files, a remote module source hosted on Terraform Registry, Github, Gitlab or a private registry. The value must not include template sequences and should be a literal string. You can refer to the Terraform documentation about the [Module Sources](https://www.terraform.io/docs/language/modules/sources.html) for more information.

A user can specify the same source address in multiple `module` blocks to create multiple copies of the resources defined in the child module.

Every time you add, update or delete a module, you must run the `terraform init` command. The `init` command gathers the required data for using the module and stores the information in the `.terraform` folder.

## Version

It's best to explicitly specify the `version` for a given Terraform module to ensure only the version which works well with the rest of the code.

The `version` argument specifies the exact module version in the `module` block:

{% highlight hcl %}
module "consul" {
  source  = "hashicorp/consul/aws"
  version = "0.0.5"

  servers = 3
}
{% endhighlight %}

The `version` argument in the module accepts a [version constraint](https://www.terraform.io/docs/language/expressions/version-constraints.html). If the module version is not explicitly specified, Terraform will use the newest installed version of the module that meets the constraint; it will download the latest version that meets the condition.

The `version` constraint argument is supported only for modules installed from a module registry, such as the public [Terraform Registry](https://registry.terraform.io/) or [Terraform Cloud's private module registry](https://www.terraform.io/docs/cloud/registry/index.html). Other module sources can provide their versioning mechanisms within the source string itself or might not support versions. The modules sourced from local file paths do not support `version`. Since the module loads from the same repository, they will always share the same version as their caller module.

## Meta-Arguments

Alongside the `source` and `version` arguments, Terraform provides a few other optional arguments. You can use these general-purpose arguments across all modules. The following arguments can be used along with modules:

* [count](https://www.terraform.io/docs/language/modules/syntax.html#count): Creates multiple instances of a module from a single module block. See [the count page](https://www.terraform.io/docs/language/meta-arguments/count.html) for details.
* [for_each](https://www.terraform.io/docs/language/modules/syntax.html#for_each) : An iterative construct, it creates multiple instances of a module from a single module block. See [the for_each page](https://www.terraform.io/docs/language/meta-arguments/for_each.html) for details.
* [providers](https://www.terraform.io/docs/language/modules/syntax.html#providers) : Passes provider configurations to a child module. See [the providers page](https://www.terraform.io/docs/language/meta-arguments/module-providers.html) for more details. If the argument is not specified, the child module will inherit the provider configuration from the calling module.
* [depends_on](https://www.terraform.io/docs/language/modules/syntax.html#depends_on): Used to create explicit dependencies between the module and the listed targets.

In addition to the above, Terraform's lifecycle argument is not currently used but reserved for planned future features.

# Terraform Modules in Practice

You can use modules to create abstractions which you can use in your infrastructure rather than the entire configuration. Modules are encapsulations for the configuration they contain. So, for instance, we can build a module for creating Virtual Machines and then call the module for our root module to make multiple Virtual Machines.

The `.tf` files in the working directory when you run `terraform plan` or `terraform apply` together form the root `module`. That module may [call other modules](https://www.terraform.io/docs/language/modules/syntax.html#calling-a-child-module) and connect them by passing output values from one to input values of another.

To learn how to use modules, see [ Modules configuration](https://www.terraform.io/docs/language/modules/index.html). This section is about creating reusable modules that other configurations can include using module blocks.

## Module Structure

Reusable modules are defined using the same configuration language concepts we use in root modules. Most commonly, modules use:

* [Input variables](https://www.terraform.io/docs/language/values/variables.html): The arguments accepted from the calling module.
* [Output values](https://www.terraform.io/docs/language/values/outputs.html): The values returned to the calling module.
* [Resources](https://www.terraform.io/docs/language/resources/index.html): Resources are the infrastructure objects managed by the module.

I will soon post a few articles on the usage of Terraform modules with code samples. IA