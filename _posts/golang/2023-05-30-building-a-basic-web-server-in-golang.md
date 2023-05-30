---
layout: post
comments: true
current: post
cover: assets/images/posts/lorenzo-herrera-p0j-mE6mGo4-unsplash_resized.webp
navigation: True
title: "Building a basic Web Server in Golang"
date: 2023-05-30 11:11:11
tags: [Golang]
class: post-template
subclass: 'post tag-golang'
author: faizan
excerpt: Discover the ease and efficiency of building a basic web server in Go. This hands-on guide will take you through setting up, running, and testing your web server. Ideal for those new to Go or those wanting to expand their back-end development skills.
social_excerpt: "Dive into #Go's versatility in #WebDevelopment as we guide you step-by-step through creating a basic web server. Learn the fundamentals of setting up web servers and leveraging Go's inbuilt packages for your #WebApplications. #Golang #BackendDevelopment"
---

# Introduction

Building a basic web server is an essential first step for anyone learning web application development. This article will guide you through creating a basic web server in Golang. 

# Prerequisites

To benefit from this article, you will need the following:

* Go installed (version `1.16` or later)
* Basic knowledge of the Go programming language

***

# Table of Contents:

* [Creating a Simple Web Server](#creating-a-simple-web-server)
* [Exploring More Web Server Features](#exploring-more-web-server-features)
* [Running and Testing](#running-and-testing)
* [Conclusion](#conclusion)

***

# Creating a Simple Web Server

Let's start by creating a basic web server using the `net/http` package from the Go standard library.

{% highlight golang %}
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", handler)
    fmt.Println("Starting server on :8080")
    http.ListenAndServe(":8080", nil)
}

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello, World!")
}
{% endhighlight %}

# Exploring More Web Server Features

While our web server is currently very basic, there are several additional features we can add:

* We can set custom routes for different webpage paths
* We can implement reading from and writing to the request and response bodies

For now, we will continue using our simple `"Hello, World!"` response handler.

{% highlight golang %}
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", handler)

    server := &http.Server{
        Addr: ":8080",
    }

    fmt.Println("Starting server on :8080")
    if err := server.ListenAndServe(); err != nil {
        fmt.Println("Error serving:", err)
    }
}

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello, World!")
}

{% endhighlight %}

# Running and Testing

To run and test our web server, we can use the following steps:

Compile and run the server:

{% highlight shell %}
go build server.go
./server
{% endhighlight %}

In a separate terminal or a web browser, navigate to `http://localhost:8080`, and you should see the `"Hello, World!"` message.

# Conclusion

We have demonstrated how to build a basic web server in Golang. This server listens for incoming connections and serves a simple `"Hello, World!"` message to the client. While this server is basic, it is a solid foundation for more complex applications built using Golang.