---
layout: post
comments: true
current: post
cover:  assets/images/posts/pierre-leverrier-k0Ynnf2CbKw-unsplash_resized.webp
navigation: True
title: "Building highly available VMSS on Azure using Terraform Modules"
date: 2022-04-12 03:13:02
tags: [Terraform]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: This article is a practical implementation of Terraform Modules for building highly available VMSS on Microsoft Azure.
---
To demonstrate how modules work in real life, we'll be building an Azure Virtual Machine Scale Set cluster for multiple environments like dev, test and production. 

We'll be running a cloud-init script inside all of the Virtual Machines, which are part of the Scale set to install docker and run an Nginx web server. The code contains the rest of the configuration to expose the proper ports via a load balancer to access the nginx web servers on multiple machines. To build the same with modules, we would have to write a separate dev, test and production configuration in Terraform. Building multiple codebases for different environments would be a laborious activity with a likelihood of discrepancies in the configurations of the three environments. However, using modules would ensure that the base configuration for the cluster would always be the same, enabling us to maintain dev-prod parity.

# Defining the Folder Structure

In building the Nginx VM Scale Set, we need to define the folder and file structure where we will store our module files. For example, the folder structure would look something like the one given below:

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
¦   +-- test
¦   ¦ +-- test.tfvars
+-- scripts
¦   +-- init.sh
+-- main.tf
+-- outputs.tf
+-- variables.tf
+-- terraform.tfvars
{% endhighlight %}

For this example, we will use the folder called modules as a container for all the separate modules we will use throughout this lab. The folder named vnet will be the place we'll use to store the `main.tf`, `output.tf` and `variables.tf` files which hold the configuration for the vnet that the rest of the resources will use. Likewise, a subnet folder will be hosting similar files to our vnet folder. The subnet module will create the resources required for the subnets. Finally, we have the `vmss` folder that holds the configuration for the Azure Virtual Machine Scale Set. Within it, we create the required resources like `public_ip`, load balancers, an address pool, lb health check probe and rules to expose the ports on the load balancer. The environments folder has the folders corresponding to the environment names; we will use the `<environment-name>.tfvars` files to create the resources based on the environment in question. We will use the environment configuration in the tfvars files in the environment folders in the commands like `plan` and `apply` to override the `terraform.tfvars` stored in the root module. The `backend.tf` defines the cloud provider for our project. We will use `azurerm` in our case and the terraform config like the `required_version` and `required_providers`.

# Writing the VNET Module

To use a module between multiple environments, first, we need to write a reusable terraform vnet module.

Before we define the modules, we need to write the variables that will be used by the modules, using the following configuration in the modules/vnet/variables.tf file:

{% highlight hcl %}
variable "resource_group_name" {
  type = string
  description = "Name of the resource group"
  default = ""
}
variable "location" {
  type = string
  description = "The location/region of the resources"
  default = ""
}
variable "tags" {
  type = map(any)
  description = "The tags to associate with resources"
}
variable "vnet_name" {
  type = string
  description = "Name of VNET to create"
}
variable "address_space" {
  type = string
  description = "The VNET CIDR"
}
variable "dns_servers" {
  type = list(any)
  description = "The DNS Servers to be used with the VNET"
  default = []
}
{% endhighlight %}

The `modules/vnet/main.tf` file contains the configuration for the VNET module as given below:

{% highlight hcl %}
resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  location            = var.location
  dns_servers         = var.dns_servers
  address_space       = [var.address_space]
  resource_group_name = var.resource_group_name

  tags = var.tags
}
{% endhighlight %}

The `modules/vnet/outputs.tf` file contains the output configuration for the VNET module as given below:

{% highlight hcl %}
output "vnet_id" {
  description = "The ID of the newly created VNet"
  value       = azurerm_virtual_network.vnet.id
}

output "vnet_name" {
  description = "The name of the VNet"
  value       = azurerm_virtual_network.vnet.name
}

output "vnet_location" {
  description = "The location of the VNet"
  value       = azurerm_virtual_network.vnet.location
}

output "vnet_address_space" {
  description = "The name of the VNet"
  value       = azurerm_virtual_network.vnet.address_space
}
{% endhighlight %}

The `outputs.tf` file in the root module contains the output values that Terraform will print on the console. If there are no outputs, Terraform will not print the values of the infrastructure objects after we run the `plan`, `apply`, or the `output` command.

# Writing the Subnet Module

Next, we need to write a reusable terraform subnet module. This module must create a subnet into which we can launch our VM scale sets.

Before we define the modules, we need to write the variables that will be used by the modules, using the following configuration in the `modules/subnet/variables.tf` file:

{% highlight hcl %}
variable "resource_group_name" {
  type = string
  description = "Name of the resource group"
  default = ""
}
variable "location" {
  type = string
  description = "The location/region of the resources"
  default = ""
}
variable "tags" {
  type = map(any)
  description = "The tags to associate with resources"
}
variable "vnet_name" {
  type = string
  description = "Name of VNET to create"
}
variable "subnets" {
  type = list(any)
  description = "The address prefix to use for the subnet."
  default = ["10.135.20.0/24"]
}
variable "add_endpoint" {
  type = bool
  description = "Should you be adding an endpoint, leave this as is"
  default = false
}
{% endhighlight %}

The `modules/subnet/main.tf` file contains the configuration for the subnet module as given below:

{% highlight hcl %}
resource "azurerm_subnet" "subnet" {
  count                = var.add_endpoint != true ? length(var.subnets) : 0
  resource_group_name  = var.resource_group_name
  name                 = lookup(var.subnets[count.index], "name", "")
  virtual_network_name = var.vnet_name
  address_prefixes     = [lookup(var.subnets[count.index], "prefix", "")]
}

resource "azurerm_subnet" "subnet-endpoint" {
  count                = var.add_endpoint == true ? length(var.subnets) : 0
  resource_group_name  = var.resource_group_name
  name                 = lookup(var.subnets[count.index], "name", "")
  virtual_network_name = var.vnet_name
  address_prefixes     = [lookup(var.subnets[count.index], "prefix", "")]
  service_endpoints    = [lookup(var.subnets[count.index], "service_endpoint", "")]
}
{% endhighlight %}

The `modules/subnet/main.tf` file contains the output configuration for the subnet module as given below:

{% highlight hcl %}
output "vnet_subnets" {
 description = "The ids of subnets created inside the new vNet"
 value       = azurerm_subnet.subnet.0.id
}

output "vnet_subnet_names" {
 description = "The ids of subnets created inside the new vNet"
 value       = flatten(concat(azurerm_subnet.subnet.*.name, azurerm_subnet.subnet-endpoint.*.name))
}
{% endhighlight %}

The `outputs.tf` file in the root module contains the output values that Terraform will print on the console. If there are no outputs, Terraform will not print the values of the infrastructure objects after we run the `plan`, `apply`, or the `output` command.

# Writing the VMSS Module

Next, we need to write a reusable terraform vmss module. This module is required to create  Virtual Machine Scale Sets on which we will be running the Nginx web servers.

Before we define the modules, we need to write the variables that will be used by the modules, using the following configuration in the modules/vmss/variables.tf file:

{% highlight hcl %}
variable "resource_group_name" {
  type = string
  description = "Name of the resource group"
  default = ""
}
variable "location" {
  type = string
  description = "The location/region of the resources"
  default = ""
}
variable "tags" {
  type = map(any)
  description = "The tags to associate with resources"
}
variable "subnet_id" {
  type = string
  description = "The subnet ID"
  default = ""
}
variable "saname" {
  type = string
  description = ""
  default = ""
}
variable "capacity" {
  type = string
  description = ""
  default = ""
}
{% endhighlight %}

The `modules/vmss/main.tf` file contains the configuration for the VMSS module as given below:

{% highlight hcl %}
resource "azurerm_public_ip" "lab2" {
  name                = "${var.resource_group_name}-pip"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags
  allocation_method   = "Static"
  domain_name_label   = var.resource_group_name
}

resource "azurerm_lb" "lab2" {
  name                = "${var.resource_group_name}-lb"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags

  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = azurerm_public_ip.lab2.id
  }
}

resource "azurerm_lb_backend_address_pool" "bpepool" {
  resource_group_name = var.resource_group_name
  loadbalancer_id     = azurerm_lb.lab2.id
  name                = "BackEndAddressPool"
}

resource "azurerm_lb_probe" "lab2" {
  name                = "http-probe"
  resource_group_name = var.resource_group_name
  loadbalancer_id     = azurerm_lb.lab2.id
  protocol            = "Http"
  request_path        = "/index.html"
  port                = 80
}

resource "azurerm_lb_rule" "lbrulehttp" {
  resource_group_name            = var.resource_group_name
  loadbalancer_id                = azurerm_lb.lab2.id
  name                           = "LBRuleHTTP"
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = "PublicIPAddress"
  probe_id                       = azurerm_lb_probe.lab2.id
  backend_address_pool_id        = azurerm_lb_backend_address_pool.bpepool.id
}

resource "azurerm_lb_nat_pool" "lbnatpoolssh" {
  name                           = "ssh"
  resource_group_name            = var.resource_group_name
  loadbalancer_id                = azurerm_lb.lab2.id
  protocol                       = "Tcp"
  frontend_port_start            = 50000
  frontend_port_end              = 50119
  backend_port                   = 22
  frontend_ip_configuration_name = "PublicIPAddress"
}

resource "azurerm_storage_account" "lab2" {
  name                     = var.saname
  location                 = var.location
  resource_group_name      = var.resource_group_name
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = var.tags
}

resource "azurerm_storage_container" "lab2" {
  name                  = "vhds"
  storage_account_name  = azurerm_storage_account.lab2.name
  container_access_type = "private"
}

resource "azurerm_virtual_machine_scale_set" "vmss" {
  name                = "${var.resource_group_name}-vmss"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags

  upgrade_policy_mode = "Manual"
  overprovision       = false

  sku {
    name     = "Standard_F2"
    tier     = "Standard"
    capacity = var.capacity
  }

  os_profile {
    computer_name_prefix = "${var.resource_group_name}-vm"
    admin_username       = "sshadmin"
    admin_password       = "Password1234!"
    custom_data          = base64encode(file("scripts/init.sh"))
  }

  os_profile_linux_config {
    disable_password_authentication = false
    # admin_ssh_key {
    #     username = "adminuser"
    #     public_key = file("~/.ssh/personal/fs/id_rsa.pub")
    # }
  }

  storage_profile_os_disk {
    name           = "osDiskProfile"
    caching        = "ReadWrite"
    create_option  = "FromImage"
    vhd_containers = ["${azurerm_storage_account.lab2.primary_blob_endpoint}${azurerm_storage_container.lab2.name}"]
  }

  storage_profile_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  network_profile {
    name    = "terraformnetworkprofile"
    primary = true

    ip_configuration {
      name                                   = "TestIPConfiguration"
      primary                                = true
      subnet_id                              = var.subnet_id
      load_balancer_backend_address_pool_ids = [azurerm_lb_backend_address_pool.bpepool.id]
      load_balancer_inbound_nat_rules_ids    = [azurerm_lb_nat_pool.lbnatpoolssh.id]
    }
  }
}
{% endhighlight %}

The `modules/vnet/main.tf` file contains the output configuration for the VMSS module as given below:

{% highlight hcl %}
output "frontend_ip_configuration" {
  value = azurerm_lb.lab2.frontend_ip_configuration
}

output "frontend_ip_address" {
  value = azurerm_public_ip.lab2.ip_address
}
{% endhighlight %}

The `outputs.tf` file in the root module contains the output values that Terraform will print on the console. If there are no outputs, Terraform will not print the values of the infrastructure objects after we run the `plan`, `apply`, or the `output` command.

# Writing the environment variable files

Now that we have defined our modules, we can create the environments folder to store the override `tfvars` for the dev, test and production environments. We have previously described a folder `environment` for the same, and under the folder, we have created folders with the names of the environments. In each folder, we'll have a `<environment-name>.tfvars` file with similar variables to the `terraform.tfvars` file, which is in the root module.

First, we will define the dev environment for the cluster in the `environment/dev` folder in a `dev.tfvars` file, with the following configuration:

{% highlight hcl %}
application         = "tfworkspaces"
environment         = "dev"
location            = "westeurope"
capacity            = 2

default_tags = {
   environment     = "dev"
   developed_by    = "Codification"
}

address_space = "10.135.0.0/16"
subnet        = "10.135.20.0/24"
{% endhighlight %}

We have detained the configuration which we will use to create our dev environment with variables like: 

`capacity`: defines the number of servers in the VM scale set.
`location`: the deployment region for the environment.
`address_space`: the CIDR for the VNet.
`subnet`: the CIDR for the subnet.
`environment`: the environment name.
`default_tags`: the tags for the resources.
`application`: the application name.

Similar to the above `dev.tfvars` file, we will define the override for the other environments like test and production.

Next, we will define the test environment for the cluster in the `environment/test` folder in a `test.tfvars` file, with the following configuration:

{% highlight hcl %}
application         = "tfworkspaces"
environment         = "test"
location            = "westeurope"
capacity            = 3

default_tags = {
   environment = "test"
   developed_by = "Codification"
}

address_space = "10.136.0.0/16"
subnet = "10.136.20.0/24"
{% endhighlight %}

Finally, we will define the test environment for the cluster in the `environment/prod` folder in a `prod.tfvars` file, with the following configuration:

{% highlight hcl %}
application         = "tfworkspaces"
environment         = "prod"
location            = "westeurope"
capacity            = 5

default_tags = {
   environment = "prod"
   developed_by = "Codification"
}

address_space = "10.134.0.0/16"
subnet = "10.134.20.0/24"
{% endhighlight %}

# Using the Modules in the root module

We have defined the modules, and now we can use the modules in our `main.tf` file located at the directory's root. We can define the `main.tf` file as given below:

{% highlight hcl %}
locals {
  resource_group_name = "${var.application}-${var.environment}"
  vnet_name           = "${var.application}-${var.environment}-vnet"
  subnet_name         = "${var.application}-${var.environment}-subnet"
  saname              = "${var.application}${var.environment}"
}

resource "azurerm_resource_group" "lab2" {
  name     = local.resource_group_name
  location = var.location
  tags     = merge(var.default_tags, map("type", "resource"))
}

module "vnet" {
  source              = "./modules/vnet"
  location            = var.location
  resource_group_name = local.resource_group_name
  vnet_name           = local.vnet_name
  address_space       = var.address_space

  tags = merge(var.default_tags, map("type", "network"))
}

module "subnets" {
  source              = "./modules/subnet"
  location            = var.location
  resource_group_name = local.resource_group_name
  vnet_name           = module.vnet.vnet_name

  subnets = [
    {
      name   = local.subnet_name
      prefix = var.subnet
    }
  ]

  tags = merge(var.default_tags, map("type", "network"))
}

module "vmss" {
  source              = "./modules/vmss"
  location            = var.location
  capacity            = var.capacity
  saname              = local.saname
  subnet_id           = module.subnets.vnet_subnets
  resource_group_name = local.resource_group_name

  tags = merge(var.default_tags, map("type", "vmss"))
}
{% endhighlight %}

Next, we define the outputs for the root module in the `outputs.tf` file given below:

{% highlight hcl %}
output "azurerm_resource_group_name" {
 description = "The name of the resource group"
 value       = azurerm_resource_group.lab2.name
}

output "vnet_module_location" {
 description = "The location of the VNet"
 value       = module.vnet.vnet_location
}

output "vnet_module_id" {
 description = "The ID of the VNet"
 value       = module.vnet.vnet_id
}

output "vnet_module_name" {
 description = "The name of the VNet"
 value       = module.vnet.vnet_name
}

output "vnet_module_address_space" {
 description = "The address space of the VNet"
 value       = module.vnet.vnet_address_space
}

output "vmss_frontend_ip_configuration" {
 value = module.vmss.frontend_ip_configuration
}

output "vmss_frontend_ip_address" {
 value = module.vmss.frontend_ip_address
}
{% endhighlight %}

Next, we will define the variables for our root module in the `variables.tf` file given below:

{% highlight hcl %}
variable "subscription_id" {
 type        = string
 description = "Azure subscription"
 # default = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
}

variable "client_id" {
 type        = string
 description = "Azure Client ID"
 # default = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
}

variable "client_secret" {
 type        = string
 description = "Azure Client Secret"
 # default = "XXXXXXXXXXXXXXXXXX"
}

variable "tenant_id" {
 type        = string
 description = "Azure Tenant ID"
 # default = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
}

variable "resource_group_name" {
 type        = string
 description = ""
 default     = ""
}

variable "location" {
 type        = string
 description = ""
 default     = ""
}

variable "default_tags" {
 description = ""
 type        = map(any)
 default     = {}
}

variable "address_space" {
 type        = string
 description = ""
 default     = ""
}

variable "subnet" {
 type        = string
 description = ""
 default     = ""
}

variable "subnets" {
 type        = list(any)
 description = ""
 default     = []
}

variable "application" {
 type        = string
 description = ""
 default     = ""
}

variable "environment" {
 type        = string
 description = ""
 default     = ""
}

variable "capacity" {
 type        = string
 description = ""
 default     = ""
}
{% endhighlight %}

Finally, we need to declare the variables in the `terraform.tfvars` file present in the root module:

{% highlight hcl %}
subscription_id = ""
client_id       = ""
client_secret   = ""
tenant_id       = ""

application = "tfworkspaces"
environment = "workspaces"
location    = "westeurope"
capacity    = 3

default_tags = {
 environment = "workspaces"
 deployed_by = "Codification"
}

address_space = "10.134.0.0/16"
subnet        = "10.134.20.0/24"
{% endhighlight %}

With a little effort, we can structure or restructure the codebase so that each significant infrastructure component sits within a module. Terraform modules written in a configurable and reusable manner can act as the basic building blocks of a clean, readable and scalable IaC codebase. In addition, writing modules would help us better manage a growing code base and reduce useless repetition in code.

You can find the codebase supporting this article on Github [Azure Terraform VMSS Module](https://github.com/faizanbashir/azure-terraform-vmss)