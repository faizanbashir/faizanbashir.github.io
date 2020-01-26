---
layout: post
current: post
cover:  assets/images/posts/1*oYWC2Wnc4Nf_mH0WL3ep_w1.jpeg
navigation: True
title: "Adding limited access IAM user to your EKS Cluster"
date: 2020-01-19 15:07:19
tags: [Kubernetes]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
---

### Creating an IAM User
Go to your [AWS Console](https://console.aws.amazon.com/), you will find the [IAM service](https://console.aws.amazon.com/iam/home) listed below the “Security, Identity & Compliance” group. Inside the IAM dashboard click on the Users tab and click “Add User” button.
![AWS IAM Dashboard User Tab](assets/images/posts/1*VtA7fGzE2a_h6yMTl69lBw.png)

Create a new user and allow the user **programmatic access** by clicking on the Programmatic access checkbox. Next, in the permissions section, you need to add a set of permissions to the user. From the list of available options under the “Attach existing policies directly” check the **AdministratorAccess**.

![Attach Policy](assets/images/posts/1*d_6PWCnAeK25k7P7CaL1uA.png)

After the user is created, you will have access to the users **Access Key ID** and **Secret Access Key**. You will be required to use these keys in the next step.

![Access Keys](assets/images/posts/1*7FqyvVFoRxZClqC16SevXw.png)

**Word of Caution**: These are the kind of credentials you don’t want to lose even by mistake, remember you have provided **AdministratorAccess** to this user. The user with **AdministratorAccess** can do pretty much everything with your AWS account.

### Configure AWS CLI

### Creating a role and role binding for the user

### Configuring permissions for the user

### Test, test test!

### Wrapup!