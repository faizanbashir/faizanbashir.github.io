---
layout: post
comments: true
current: post
cover:  ./assets/images/posts/artturi-jalli-g5_rxRjvKmg-unsplash_resized.webp
navigation: True
title: "Building OpenFaaS Serverless function to detect weather using OpenWeatherMap and Python"
date: 2023-04-02 03:13:00
tags: [Serverless]
class: post-template
subclass: 'post tag-writings'
author: faizan
excerpt:  Explore how to create an OpenFaaS serverless function using Python to detect the current weather with the OpenWeatherMap API, and learn how to deploy and test your function.
---

# Building OpenFaaS Serverless Python Function

Serverless computing is rapidly becoming famous for deploying applications and functions without the hassle of managing the underlying infrastructure. OpenFaaS is an open-source serverless framework for building functions with Docker and Kubernetes. This article will walk you through creating an OpenFaaS serverless function using Python to detect the current weather using the OpenWeatherMap API.

***
# Table of Contents:

* [Prerequisites](#prerequisites)
* [Setting Up Your OpenFaaS Environment](#setting-up-your-openfaas-environment)
* [Creating the Function](#creating-the-function)
* [Deploying the Function](#deploying-the-function)
* [Testing the Function](#testing-the-function)
* [Conclusion](#conclusion)
* [Keep Learning: More on Serverless](#keep-learning-more-on-serverless)

***

# Prerequisites

1. OpenFaaS CLI installed
2. Docker installed
3. Python 3 installed
4. An OpenWeatherMap API key

# Setting Up Your OpenFaaS Environment

First, you need to set up an OpenFaaS environment. Then, follow the OpenFaaS documentation on deploying OpenFaaS on Kubernetes or Docker Swarm.

# Creating the Function

Create a new directory for your function:

{% highlight shell %}
mkdir weather-function && cd weather-function
{% endhighlight %}

Generate a new Python function using the OpenFaaS CLI:

{% highlight shell %}
faas-cli new --lang python3 weather-function
{% endhighlight %}

This command will create a `weather-function.yml` file and a weather-function directory containing the function's source code.

Update the `requirements.txt` file inside the weather-function directory to include the requests library:

{% highlight python %}
requests
{% endhighlight %}

Replace the content of the `handler.py` file inside the weather-function directory with the following code:

{% highlight python %}
import json
import os
import requests

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

def handle(req):
    try:
        data = json.loads(req)
        location = data['query']['location']
    except (KeyError, ValueError):
        return json.dumps({"error": "Invalid request payload"})

    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return json.dumps({"error": "Error fetching weather data"})

    weather_data = response.json()
    weather = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']

    return json.dumps({
        "location": location,
        "weather": weather,
        "temperature": temperature
    })
{% endhighlight %}

This function uses the `requests` library to fetch the current weather data from the OpenWeatherMap API based on the provided location.

Update the `weather-function.yml` file to include the `OPENWEATHERMAP_API_KEY` environment variable:

{% highlight yaml %}
environment:
  OPENWEATHERMAP_API_KEY: YOUR_API_KEY
{% endhighlight %}

Replace `YOUR_API_KEY` with your actual OpenWeatherMap API key.

# Deploying the Function

Build the function Docker image:

{% highlight shell %}
faas-cli build -f weather-function.yml
{% endhighlight %}

Push the function Docker image to a Docker registry (optional):

{% highlight shell %}
faas-cli push -f weather-function.yml
{% endhighlight %}

Deploy the function to your OpenFaaS environment:

{% highlight shell %}
faas-cli deploy -f weather-function.yml
{% endhighlight %}

# Testing the Function

After deploying your function, you can test it by invoking it using the OpenFaaS CLI or sending an HTTP request to the function's endpoint.

Using the OpenFaaS CLI:

{% highlight shell %}
echo -n '{"query": {"location": "San Francisco"}}' | faas-cli invoke weather-function
{% endhighlight %}

Using curl:

{% highlight shell %}
curl -X POST -d '{"query": {"location": "San Francisco"}}' http://127.0.0.1:8080/function
{% endhighlight %}

You should receive a JSON response containing the current weather data for the specified location:

{% highlight json %}
{
  "location": "San Francisco",
  "weather": "clear sky",
  "temperature": 20
}
{% endhighlight %}

You can replace "San Francisco" with any location of your choice.

# Conclusion

In this article, we demonstrated how to build an OpenFaaS serverless function that detects the current weather using the OpenWeatherMap API. By leveraging the flexibility and power of OpenFaaS and the simplicity of the OpenWeatherMap API, you can quickly develop and deploy serverless functions to address a wide variety of use cases. In addition, you can extend this example to include more features, such as fetching forecast data or integrating with other APIs to create a more comprehensive weather application.

# Keep Learning: More on Serverless

Discover the world of serverless architecture in our comprehensive collection of articles! Equip yourself with valuable knowledge and skills in the exciting realm of serverless computing by exploring the following topics:

* [What is serverless architecture and what are its pros and cons](/building-serverless-contact-form-for-static-websites): Understand the ins and outs of serverless architecture, its advantages, and its drawbacks.
* [Building serverless contact form for static websites](/building-serverless-contact-form-for-static-websites): Learn how to create a serverless contact form for your static website.
* [Serverless Technology: Exploring Cloud Providers, Benefits, Challenges, and Kubernetes Integration](/serverless-technology-exploring-cloud-providers-benefits-challenges-and-kubernetes-integration): Dive deeper into the serverless landscape and grasp the fundamentals of how it operates.
* [Building Serverless Knative function to detect weather using OpenWeatherMap and Python](/building-knative-serverless-function-to-detect-weather-using-openweathermap-and-python): Explore a practical example of creating a serverless function with Knative, OpenWeatherMap API, and Python.

Don't just stop there; continue your journey and delve even further into the fascinating and expansive world of serverless technologies and their endless possibilities.