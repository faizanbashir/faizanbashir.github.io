---
layout: post
comments: true
current: post
cover:  assets/images/posts/chris-hardy-XF-ZLS5G0QU-unsplash.webp
navigation: True
title: "Building an Nginx webserver on Azure using Terraform"
date: 2022-04-09 03:13:00
tags: [Terraform, Azure]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: This article will walk you through automating the creation of an Nginx web server on Microsoft Azure using Terraform as an Infrastructure as Code (IaC) tool.
---
This article will walk you through automating the creation of an Nginx web server on Azure using Terraform as an Infrastructure as Code (IaC) tool.

I assume that you have installed terraform. If not, download the Terraform binary executable for your platform and follow the steps to install since I will be using Azure as a provider so ensure that Azure CLI is installed and configured correctly.

Create one project in your desired location and name it whatever you like. `cd` into the project and follow the following steps:

# Variable Declaration

Create a file called `variables.tf` where you would declare some important variables as follows:

{% highlight hcl %}
variable "subscription_id" {
   description = "Azure subscription"
   default = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
}

variable "client_id" {
   description = "Azure Client ID"
   default = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
}

variable "client_secret" {
   description = "Azure Client Secret"
   default = "XXXXXXXXXXXXXXXXXX"
}

variable "tenant_id" {
   description = "Azure Tenant ID"
   default = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
}

variable "instance_size" {
   type = string
   description = "Azure instance size"
   default = "Standard_F2"
}

variable "location" {
   type = string
   description = "Region"
   default = "West US"
}

variable "environment" {
   type = string
   description = "Environment"
   default = "dev"
}
{% endhighlight %}

Variables or Input Variables or Terraform Variables serve as parameters for a Terraform module. Some important terms used in declaring variables:

1. `variable`: You can declare the variables within a variable block followed by a unique name.
2. `description`: It gives a brief description of the variable.
3. `default`: Requires a literal value. If present, the default value will be used to set the value for the variable when calling the module or running Terraform.

Here, you declare three variables for the `location`, `client_id`, and `client_secret`. You need to provide your region and credentials for your Azure user against the `default` key.

# Provider

Create another file called `main.tf` and describe the cloud provider,  Azure, in this case.

{% highlight hcl %}
terraform {
   required_version = ">= 0.12"
   required_providers {
      azurerm = "~>2.24.0"
   }
}

provider "azurerm" {
   subscription_id = var.subscription_id
   client_id = var.client_id
   client_secret = var.client_secret
   tenant_id = var.tenant_id
   features {}
}
{% endhighlight %}

In `main.tf`, you use provider block to describe the provider you want to use. The Azure provider offers a flexible means of providing credentials for authentication. This example uses the Azure authentication with [Service Principal and client Secret method](https://www.terraform.io/docs/providers/azurerm/auth/service_principal_client_secret.html). There are multiple ways of authenticating, and you can learn more about those [here](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs).

The method of authenticating used in this example is known as the static credentials method wherein `subscription_id`, `client_id`, `client_secret`, `tenant_id`, and `features` are added in-line in the Azurerm provider block.

The interpolation syntax is used as a reference to call the above variables. These interpolations are wrapped in `${}`, such as `${var.client_secret}`. 

Interpolation is robust and allows you to reference variables, attributes of resources, call functions, etc. Terraform released a significant version wherein the interpolation method became a little simpler. You can use the `var.client_secret` to access the variable that you accessed using the previous ways.

To initialize Terraform, `run` init, and you can see that Terraform will download the provider plugin for `Azurerm`.

{% highlight shell %}
$ terraform init
{% endhighlight %}

# Resource Group

According to the [Micorsoft azure documentation](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal):

"A resource group is a container that holds related resources for an Azure solution. The resource group can include all the resources for the solution or only those resources that you want to manage as a group. You decide how you want to allocate resources to resource groups based on what makes the most sense for your organization. Generally, add resources that share the same lifecycle to the same resource group so you can quickly deploy, update, and delete them as a group."

A resource group in Azure acts as a metadata store for the resources within the resource group. The resource group region will be the locality where the metadata is stored. For example, some applications would require you to keep the user data within a specific geographic area for compliance reasons.

We can create a resource group using the following code in the `main.tf` file:

{% highlight hcl %}
resource "azurerm_resource_group" "webserver" {
   name = "nginx-server"
   location = var.location
}
{% endhighlight %}

# Azure VNet Resources

Create a file called `vnet.tf`, wherein you would describe the vnet resources.

In this example, the Azure VNet Terraform module creates the vpc resources. A module is a container for multiple resources used together. You can also explore the [Terraform Module Registry](https://registry.terraform.io/) to learn about various modules provided by Terraform. Put the following lines of code in your `vnet.tf` file.

{% highlight hcl %}
module "network" {
   source = "Azure/vnet/azurerm"
   version = "2.4.0"
   resource_group_name = azurerm_resource_group.webserver.name
   address_space = ["10.0.0.0/16"]
   subnet_prefixes = ["10.0.1.0/24", "10.0.2.0/24"]
   subnet_names = ["subnet1", "subnet2"]

   nsg_ids = {
       subnet1 = azurerm_network_security_group.allowedports.id
   }

   tags = {
       environment = var.environment
       costcenter = "it"
   }

   depends_on = [azurerm_resource_group.webserver]
}
{% endhighlight %}

Modules are declared using `module` blocks. The label immediately after the module keyword is a local name, which the calling module can use to refer to this instance of the module. Within the block body (between `{ and }`) are the arguments for the module.

`source`: All modules require a `source` argument, a meta-argument defined by Terraform CLI. Its value is either the path to a local directory of the module's configuration files or a remote module source that Terraform should download and use. Other arguments mentioned above are self-understood and depend upon one's desired values.

***Note:** You can specify source addresses to be used in multiple module blocks to create various copies of the resources defined within, possibly with different variable values.*

***Note:** Every time a module gets added, modified, or deleted, the `terraform init` command should be re-run so that Terraform can adjust the installed modules.*

# Network Security Group

Add the following lines of code containing the Network Security Group configuration in the `main.tf` file:

{% highlight hcl %}
resource "azurerm_network_security_group" "allowedports" {
   name = "allowedports"
   resource_group_name = azurerm_resource_group.webserver.name
   location = azurerm_resource_group.webserver.location
  
   security_rule {
       name = "http"
       priority = 100
       direction = "Inbound"
       access = "Allow"
       protocol = "Tcp"
       source_port_range = "*"
       destination_port_range = "80"
       source_address_prefix = "*"
       destination_address_prefix = "*"
   }

   security_rule {
       name = "https"
       priority = 200
       direction = "Inbound"
       access = "Allow"
       protocol = "Tcp"
       source_port_range = "*"
       destination_port_range = "443"
       source_address_prefix = "*"
       destination_address_prefix = "*"
   }

   security_rule {
       name = "ssh"
       priority = 300
       direction = "Inbound"
       access = "Allow"
       protocol = "Tcp"
       source_port_range = "*"
       destination_port_range = "22"
       source_address_prefix = "*"
       destination_address_prefix = "*"
   }
}
{% endhighlight %}

Terraform's resource block is used to describe infrastructure objects, for example, instances, security groups, etc. In this example, you define an `azurerm` resource of type `azurerm_network_security_group` with a given name `allowedports`. Resource type and local name together serve as identifiers of the resource. Within the block body (between `{ and }`) are the configuration arguments for the resource itself.

The egress and ingress blocks containing the inbound SSH and HTTP traffic are permitted using a security group. You can specify the ingress/egress blocks multiple times for each rule.

You have set up a vnet with two subnets in one region and three security groups. You are good to create an instance now where you would install an nginx web server in a docker container!

# Creating Public IP and Network Interface

To expose our Nginx web server to the outside world, we need to create a public IP address using the `azurerm_public_ip` and network interface resources azurerm_network_interface`. The network interface resides in `subnet1` and will be attached to the virtual machine exposing a web server to the outside world.

{% highlight hcl %}
resource "azurerm_public_ip" "webserver_public_ip" {
   name = "webserver_public_ip"
   location = var.location
   resource_group_name = azurerm_resource_group.webserver.name
   allocation_method = "Dynamic"

   tags = {
       environment = var.environment
       costcenter = "it"
   }

   depends_on = [azurerm_resource_group.webserver]
}

resource "azurerm_network_interface" "webserver" {
   name = "nginx-interface"
   location = azurerm_resource_group.webserver.location
   resource_group_name = azurerm_resource_group.webserver.name

   ip_configuration {
       name = "internal"
       private_ip_address_allocation = "Dynamic"
       subnet_id = module.network.vnet_subnets[0]
       public_ip_address_id = azurerm_public_ip.webserver_public_ip.id
   }

   depends_on = [azurerm_resource_group.webserver]
}
{% endhighlight %}

# Azure Virtual Machine Instance

Before creating an instance, we will add some essential variables to the `variables.tf` file.

{% highlight hcl %}
variable "instance_size" {
   type = string
   description = "Standard_F2"
}
{% endhighlight %}

`instance_size`: specifies the type of instances to create.

Create one `outputs.tf` file to output desirable information regarding the resources on their successful completion. For example, let's paste the below lines of code:

{% highlight hcl %}
output "vnet_subnets" {
 value = module.network.vnet_subnets
}

output "vnet_id" {
 value = module.network.vnet_id
}

output "nginx_private_ip" {
   value = azurerm_linux_virtual_machine.nginx.private_ip_address
}

output "nginx_public_ip" {
   value = azurerm_linux_virtual_machine.nginx.public_ip_address
}
{% endhighlight %}

Okay, all set. Now let's create the instance.

Add below lines of code to the `main.tf` file:

{% highlight hcl %}
resource "azurerm_linux_virtual_machine" "nginx" {
   size = var.instance_size
   name = "nginx-webserver"
   resource_group_name = azurerm_resource_group.webserver.name
   location = azurerm_resource_group.webserver.location
   custom_data = base64encode(file("scripts/init.sh"))
   network_interface_ids = [
       azurerm_network_interface.webserver.id,
   ]

   source_image_reference {
       publisher = "Canonical"
       offer = "UbuntuServer"
       sku = "18.04-LTS"
       version = "latest"
   }

   computer_name = "nginx"
   admin_username = "adminuser"
   admin_password = "Faizan@bashir.123"
   disable_password_authentication = false

   os_disk {
       name = "nginxdisk01"
       caching = "ReadWrite"
       create_option = "FromImage"
       storage_account_type = "Standard_LRS"
   }

   tags = {
       environment = var.environment
       costcenter = "it"
   }

   depends_on = [azurerm_resource_group.webserver]
}
{% endhighlight %}

Again a virtual machine instance is created with a resource block followed by a type of resource `azurerm_linux_virtual_machine` and a unique local name `nginx-webserver` to identify the resource within other modules. The arguments used are explained as follows:

`size`: Type of instance.

`source_image_reference`: Defines the details about the image to be used for creating the Virtual Machine. It uses keys such as `publisher`, `offer`, `sku`, and `version` to define the Virtual Machine image.

`custom_data`: You need to install docker and run nginx in a container once our instance launches. The `custom_data` argument achieves this. You can embed the commands in our `main.tf` itself or more conveniently create one sh file and pass that to the `custom_data` argument. The custom data should be base64 encoded that is why we use a function called `base64encode` to encode the data in the script. Let's create one `scripts/init.sh` file and paste the below code:

{% highlight shell %}
#!/bin/bash
#Installing Docker
sudo apt-get remove docker docker-engine docker.io
sudo apt-get update
sudo apt-get install -y \
apt-transport-https \
ca-certificates \
curl \
software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"
sudo apt-get update
sudo apt-get install docker-ce -y
sudo usermod -a -G docker $USER
sudo systemctl enable docker
sudo systemctl restart docker
sudo docker run --name docker-nginx -p 80:80 nginx:latest
{% endhighlight %}

`tags`: A mapping of tags to assign to the resource.

# Execution Plan and Applying the Changes

You can now generate the execution plan by running the `plan` command and checking if everything is as expected.

{% highlight shell %}
$ terraform plan
{% endhighlight %}

You can also use the `terraform validate` command to check if the configuration is correct using the following command:

{% highlight shell %}
$ terraform validate
{% endhighlight %}

Once confirmed, you can proceed with the `apply` command to provision a new or apply the changes to the existing infrastructure.

{% highlight shell %}
$ terraform apply
{% endhighlight %}

Once successfully applied, you will get the Virtual Machines IP addresses created by Terraform. You can use the IP addresses to log in to them using SSH.

You can also explore the `terraform show` command to see the provisioned infrastructure's detailed information.

Once logged in, run `docker ps` and see the running nginx container. Next, `curl localhost`, and you should visit the default nginx webpage.

# Cleanup, Destroying the Infrastructure

If you want to delete the whole infrastructure, you can run the `destroy` command, like so.

{% highlight shell %}
$ terraform destroy
{% endhighlight %}

However, you can delete a specific resource also using the `target` flag. For example, you can destroy the above instance using the following command:

{% highlight shell %}
$ terraform destroy -target=azurerm_linux_virtual_machine.nginx-webserver
{% endhighlight %}