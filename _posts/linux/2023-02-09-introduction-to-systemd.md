---
layout: post
comments: true
current: post
cover: assets/images/posts/evgeny-matveev-3kWh-ikNZJo-unsplash.webp
navigation: True
title: "Introduction to Systemd"
date: 2023-02-09 11:11:11
tags: [Linux]
class: post-template
subclass: 'post tag-linux'
author: faizan
excerpt: This article will discuss how to manage services in Systemd, a popular init system used in many Linux distributions.
---
This article will discuss how to manage services in Systemd, a popular init system used in many Linux distributions. The `systemctl` command is the primary tool for operating services in Systemd. With the `systemctl` command, you can start, stop, restart, enable, and disable services, among many other actions.

***
# Table of Contents

* [Enabling Services](#enabling-services)
* [Disabling Services](#disabling-services)
* [Checking Service Status](#checking-service-status)
* [Disabling Services](#disabling-services)
* [Listing Service Units](#listing-service-units)
* [Iterating Over Services](#iterating-over-services)
* [Removing Services](#removing-services)
* [Conclusion](#conclusion)

***

## Enabling Services

Let's start by enabling a service to be launched at system startup. To do this, use the following command:

{% highlight bash %}
sudo systemctl enable <servicename>.service
{% endhighlight%}

The `enable` command will configure the service to start automatically at boot time.

## Disabling Services

To disable a service, use the following command:

{% highlight bash %}
sudo systemctl disable <servicename>.service
{% endhighlight%}

The `disable` command will prevent the service from starting automatically at boot time.

## Checking Service Status

To check the status and active state of a service, use the following commands:

{% highlight bash %}
sudo systemctl status <servicename>
sudo systemctl is-active <servicename>
{% endhighlight%}

The `status` command will give you information about the service's status, including whether it is running. The `is-active` command will inform you whether a system is an "active" or "inactive" service.

## Listing Service Units

To list all active services, use the following command:

{% highlight bash %}
sudo systemctl list-units --type=service
{% endhighlight%}

The `list-units` command will give you a list of all currently active services on your system.

## Iterating over Services

To iterate over a list of services and check whether they are enabled and active services, you can use the following script:

{% highlight bash %}
for SERVICES in etcd kube-apiserver kube-controller-manager kube-scheduler;
do echo --- $SERVICES --- ; 
	systemctl is-active $SERVICES ;
	systemctl is-enabled $SERVICES ; echo "";  
done
{% endhighlight%}

This script will list the services specified in the for loop and their active and enabled state.

## Removing Services

To completely remove a service, you must stop it, disable it, remove its system files, and reload the Systemd daemon. You can use the following commands to do this:

{% highlight bash %}
sudo systemctl stop <servicename>
sudo systemctl disable <servicename>
sudo rm /etc/systemd/system/<servicename>
sudo systemctl daemon-reload
sudo systemctl reset-failed
{% endhighlight%}

Finally, to unmask a previously masked service, use the following command:

{% highlight bash %}
sudo systemctl unmask [servicename]
{% endhighlight%}

The `unmask` command will restore the ability to start and enable the service.

## Conclusion

In conclusion, Systemd provides a centralized and powerful way to manage services in Linux. With the systemctl command, you can perform many actions, including starting, stopping, restarting, enabling, disabling, and removing services. The above commands and scripts should help you begin managing services in Systemd.