---
layout: post
comments: true
current: post
cover:  assets/images/posts/ishan-seefromthesky-qE1Y8GQKhEk-unsplash_resized.jpg
navigation: True
title: "Building an Nginx webserver on AWS using Terraform"
date: 2022-04-08 12:07:19
tags: [Terraform, AWS]
class: post-template
subclass: 'post tag-terraform'
author: faizan
excerpt: This article will walk you through automating the creation of an Nginx web server on AWS using Terraform as an Infrastructure as Code (IaC) tool.
---
This article will walk you through automating the creation of an Nginx web server on AWS using Terraform as an Infrastructure as Code (IaC) tool.

I assume that you have installed terraform. If not, download the Terraform binary executable for your platform and follow the steps to install since I will be using AWS as a provider so ensure that AWS CLI is installed and configured correctly.

Create one project in your desired location and name it whatever you like. `cd` into the project and follow the following steps:

# Variable Declaration
Create a file called `variables.tf` where you would declare some important variables as follows:

{% highlight hcl %}
variable "aws_region" {
   description = "AWS Region to launch servers"
   default = "eu-west-2"
}

variable "aws_access_key" {
   description = "AWS User Access Key"
   default = "XXXXXXXXXXXXXXXXXX"
}

variable "aws_secret_key" {
   description = "AWS User Secret Key"
   default = "XXXXXXXXXXXXXXXXXX"
}
{% endhighlight %}

Variables or Input Variables or Terraform Variables serve as parameters for a Terraform module. Some important terms used while declaring variables:

1. `variable`: You can declare the variables within a variable block followed by a unique name.
2. `description`: You can set a brief description for the variable.
3. `default`: Requires a literal value. If present, the default value will be used to set the value for the variable when calling the module or running Terraform.

Here, you declare three variables for the `aws_region`, `aws_access_key`, and `aws_secret_key`. You need to provide your region and credentials for your AWS user against the default key.

# Provider
Create another file called `main.tf` and describe the cloud provider, AWS, in this case.

{% highlight hcl %}
provider "aws" {
   access_key = var.aws_access_key
   secret_key = var.aws_secret_key
   region = var.aws_region
   skip_credentials_validation = true
}
{% endhighlight %}

In `main.tf`, you use provider block to describe the provider you want to use. The AWS provider offers a flexible means of providing credentials for authentication. There are multiple ways of authenticating, and you can learn more about those here.

The method of authenticating used in this example is known as the static credentials method wherein `region`, `access_key` and `secret_key` are added in-line in the AWS provider block.

The interpolation syntax is used as a reference to call the above variables. The `${}` is used to wrap an interpolation, such as `${var.aws_access_key}`.

Interpolation is robust and allows you to reference variables, attributes of resources, call functions, etc. Terraform released a major version wherein the interpolation method became a little simpler. You can use the `var.aws_access_key` to access the variable that you accessed using the previous ways.

To initialize Terraform, `init`, you can see that Terraform will download the provider plugin for AWS.

{% highlight hcl %}
$ terraform init
{% endhighlight %}

# AWS VPC Resources
Create a file called `vpc.tf`, wherein you would describe the VPC resources.

The AWS VPC Terraform module will create the VPC resources in this example. A module is a container for multiple resources used together. You can also explore the Terraform Module Registry to learn about various modules provided by Terraform. For example, put the following lines of code in your `vpc.tf` file.

{% highlight hcl %}
module "vpc" {
   source               = "terraform-aws-modules/vpc/aws"
   name                 = "vpc-main"
   cidr                 = "10.0.0.0/16"
   azs                  = ["${var.aws_region}a", "${var.aws_region}b"]
   private_subnets      = ["10.0.0.0/24", "10.0.1.0/24"]
   public_subnets       = ["10.0.100.0/24", "10.0.101.0/24"]
   enable_dns_hostnames = true
   enable_dns_support   = true
   enable_nat_gateway   = false
   enable_vpn_gateway   = false
   tags = {
       Terraform   = "true"
       Environment = "dev"
   }
}
{% endhighlight %}

Modules are declared using module blocks. The label immediately after the module keyword is a local name, which the calling module can use to refer to this instance of the module. Within the block body (between `{` and `}`) are the arguments for the module.

`source`: All modules require a source argument, a meta-argument defined by Terraform CLI. Its value is either the path to a local directory of the module's configuration files or a remote module source that Terraform should download and use. Other arguments mentioned above are self-understood and depend upon one's desired values.

*Note: You can specify source addresses to be used in multiple module blocks to create multiple copies of the resources defined within, possibly with different variable values.*

*Note: Every time a module gets added, modified, or deleted, the `terraform init` command should be re-run so that Terraform can adjust the installed modules.*

# Security Group
Add the below lines of code in the `main.tf` file:

{% highlight hcl %}
resource "aws_security_group" "allow_ports" {
   name        = "allow_ssh_http"
   description = "Allow inbound SSH traffic and http from any IP"
   vpc_id      = "${module.vpc.vpc_id}"

   #ssh access
   ingress {
       from_port   = 22
       to_port     = 22
       protocol    = "tcp"
       # Restrict ingress to necessary IPs/ports.
       cidr_blocks = ["0.0.0.0/0"]
   }

   # HTTP access
   ingress {
       from_port   = 80
       to_port     = 80
       protocol    = "tcp"
       # Restrict ingress to necessary IPs/ports.
       cidr_blocks = ["0.0.0.0/0"]
   }

   egress {
       from_port   = 0
       to_port     = 0
       protocol    = "-1"
       cidr_blocks = ["0.0.0.0/0"]
   }
  
   tags {
       Name = "Allow SSH and HTTP"
   }
}
{% endhighlight %}

Terraform's resource block is used to describe infrastructure objects, for example, instances, security groups, etc. In this example, you define an aws resource of `aws_security_group` with `allow_ports`. Resource type and local name together serve as identifiers of the resource. Within the block body (between `{` and `}`) are the configuration arguments for the resource.

The egress and ingress blocks containing the inbound SSH and HTTP traffic are permitted using a security group. You can specify the ingress/egress blocks multiple times for each rule. The interpolation syntax `${module.vpc.vpc_id}` is used to refer to VPC id's as the VPC a module.

You have set up a VPC with two public and private subnets in two availability zones and one security group. You are good to create an instance now where you would install the nginx web server in a docker container!

# AWS EC2 Instance#
Before you create an EC2 instance, the `variables.tf` file needs to have the essential variables mentioned below:

{% highlight hcl %}
variable "aws_amis" {
   default = {
       us-east-1 = "ami-0f9cf087c1f27d9b1"
       eu-west-2 = "ami-095ed825090131933"
   }
}

variable "instance_type" {
   description = "Type of AWS EC2 instance."
   default     = "t2.micro"
}

variable "public_key_path" {
   description = "Enter the path to the SSH Public Key to add to AWS."
   default     = "~/.ssh/yourkey.pem"
}

variable "key_name" {
   description = "AWS key name"
   default     = "name of keypair"
}

variable "instance_count" {
   default = 1
}
{% endhighlight %}

* `aws_amis`: specifies the type of AMI we will use for our instance based upon a region.

* `instance_type`: specifies the type of instance, e.g. General Purpose Instance(T2, M3, M4), Compute Optimized(C5, C4, C3), Memory Optimized(X1, R4, R3), etc. based upon the requirement.

* `public_key_path`: specifies the location of the public key (PEM file) on your machine used to login to the instance.

* `key_name`: specifies the aws key pair name.

* `instance_count`: specifies the number of instances to create, one in this case.

Create one `outputs.tf` file to display some important information regarding the resources on their successful completion. Let's paste the below lines of code:

{% highlight hcl %}
output "vpc_id" {
   value = ["${module.vpc.vpc_id}"]
}

output "vpc_public_subnets" {
   value = ["${module.vpc.public_subnets}"]
}

output "webserver_ids" {
   value = ["${aws_instance.webserver.*.id}"]
}

output "ip_addresses" {
   value = ["${aws_instance.webserver.*.id}"]
}
{% endhighlight %}

Okay, all set. Now let's create the instance.

Add below lines of code to the `main.tf` file:

{% highlight hcl %}
resource "aws_instance" "webserver" {
   instance_type          = "${var.instance_type}"
   ami                    = "${lookup(var.aws_amis, var.aws_region)}"
   count                  = "${var.instance_count}"
   key_name               = "${var.key_name}"
   vpc_security_group_ids = ["${aws_security_group.allow_ports.id}"]
   subnet_id              = "${element(module.vpc.public_subnets,count.index)}"
   user_data              = "${file("scripts/init.sh")}"
  
   tags {
       Name = "Webserver"
   }
}
{% endhighlight %}

Again ec2 instance is created with a resource block followed by a type of resource `aws_instance` and a unique local name web server to identify the resource within other modules. The arguments used are explained as follows:

* `instance_type`:  The EC2 instance type.

* `ami`: Type of AMI. Notice the lookup, which fetches the value from the `variables.tf` file based on the specified region.

* `count`: Number of instances to be created.

* `key_name`: Name of the key pair.

* `vpc_security_group_ids`: The array of ids of the security groups.

* `subnet_id`: The id of the subnet used to launch the EC2 instance. Here, `count.index` is passed as a parameter to the element function for creating multiple instances in each subnet.

* `user_data`: You need to install docker and run nginx in a container once our instance launches. The `user_data` argument achieves this. You can embed the commands in our `main.tf` itself or more conveniently create one sh file and pass that to the `user_data` argument. Lets create one `scripts/init.sh` file and paste the below code:

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

* `tags`: A mapping of tags assigned to the resource.

# Executing Plan and Applying the Changes
You can now generate the execution plan by running the plan command and checking if everything is as expected.

{% highlight hcl %}
$ terraform plan
{% endhighlight %}

You can use the `validate` command to check if the terraform configuration is correct using the following command:

{% highlight hcl %}
$ terraform validate
{% endhighlight %}

Once confirmed, you can proceed with the apply command to provision a new or apply the changes to existing infrastructure.

{% highlight hcl %}
$ terraform apply
{% endhighlight %}

On successful applications, you will get the IP addresses of the instance(s) created by Terraform that you can use to log in using SSH.

You can also explore the `terraform show` command to see the detailed information on the provisioned infrastructure.

After logging in, run `docker ps` and see the running nginx container. Next, run the command `curl http://localhost`, and you should visit the default nginx webpage.

# Cleanup, Destroying the Infrastructure
If you want to delete the whole infrastructure, you can run the `destroy` command, like so.

{% highlight hcl %}
$ terraform destroy
{% endhighlight %}

However, you can delete a specific resource also using the target flag. For example, you can destroy the above instance using the following command:

{% highlight hcl %}
$ terraform destroy -target=aws_instance.webserver
{% endhighlight %}