---
layout: post
comments: true
current: post
cover:  assets/images/posts/shahadat-rahman-BfrQnKBulYQ-unsplash_resized.webp
navigation: True
title: "Building Knative Serverless function to detect weather using OpenWeatherMap and Python"
date: 2023-04-02 03:13:00
tags: [Serverless]
class: post-template
subclass: 'post tag-writings'
author: faizan
excerpt:  Learn how to create and deploy a Knative serverless function using Python to detect the current weather using the OpenWeatherMap API on a Kubernetes cluster.
---

# Building Knative Serverless Python Function

Knative is a Kubernetes-based platform designed to deploy, run, and manage serverless workloads. This article will walk you through creating a Knative serverless function using Python to detect the current weather using the OpenWeatherMap API.

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

1. A Kubernetes cluster with Knative Serving installed
2. `kubectl` CLI installed and configured to interact with your cluster
3. Python 3 installed
4. An OpenWeatherMap API key

# Creating the Function

Create a new directory for your function:

{% highlight shell %}
mkdir weather-function && cd weather-function
{% endhighlight %}

Create a `requirements.txt` file inside the `weather-function` directory to include the `requests` library:

{% highlight text %}
requests
{% endhighlight %}

Create a `main.py` file inside the `weather-function` directory with the following code:

{% highlight python %}
import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

@app.route('/', methods=['POST'])
def weather():
    try:
        data = request.json
        location = data['query']['location']
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid request payload"})

    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Error fetching weather data"})

    weather_data = response.json()
    weather = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']

    return jsonify({
        "location": location,
        "weather": weather,
        "temperature": temperature
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
{% endhighlight %}

This function uses the `requests` library to fetch the current weather data from the OpenWeatherMap API based on the provided location.

Create a `Dockerfile` inside the `weather-function` directory with the following content:


{% highlight Dockerfile %}
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV PORT 8080
CMD ["python", "main.py"]
{% endhighlight %}

This Dockerfile sets up a Python environment, installs the required libraries, and runs the Flask application.

# Deploying the Function

Build the function Docker image:

{% highlight shell %}
docker build -t your-docker-username/weather-function .
{% endhighlight %}

Push the function Docker image to a Docker registry:

{% highlight shell %}
docker push your-docker-username/weather-function
{% endhighlight %}

Create a `weather-function.yaml` file with the following content:

{% highlight yaml %}
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: weather-function
spec:
  template:
    spec:
      containers:
        - image: your-docker-username/weather-function
          env:
            - name: OPENWEATHERMAP_API_KEY
              value: YOUR_API_KEY
{% endhighlight %}

Replace `your-docker-username` with your actual Docker `username` and `YOUR_API_KEY` with your existing OpenWeatherMap API key.

Deploy the function to your Knative environment:

{% highlight shell %}
kubectl apply -f weather-function.yaml
{% endhighlight %}

# Testing the Function

After deploying your function, you can test it by sending an HTTP request to its endpoint.

Get the domain name for your function:

{% highlight shell %}
kubectl get ksvc weather-function -o jsonpath='{.status.url}'
{% endhighlight %}

This command will return the domain name of your function.

Send a POST request to the function using curl:
{% highlight shell %}
curl -X POST -H "Content-Type: application/json" -d '{"query": {"location": "San Francisco"}}' http://weather-function.default.example.com
{% endhighlight %}

Replace `http://weather-function.default.example.com` with the domain name you obtained in the previous step.

You should receive a JSON response containing the weather information:

{% highlight json %}
{
  "location": "San Francisco",
  "weather": "clear sky",
  "temperature": 20.8
}
{% endhighlight %}

# Conclusion

In this article, we demonstrated how to create and deploy a Knative serverless function using Python to detect the current weather using the OpenWeatherMap API. Knative enables you to build serverless applications on Kubernetes, providing a powerful platform for deploying and scaling your functions as needed.

# Keep Learning: More on Serverless

Discover the world of serverless architecture in our comprehensive collection of articles! Equip yourself with valuable knowledge and skills in the exciting realm of serverless computing by exploring the following topics:

* [What is serverless architecture and what are its pros and cons](/building-serverless-contact-form-for-static-websites): Understand the ins and outs of serverless architecture, its advantages, and its drawbacks.
* [Building serverless contact form for static websites](/building-serverless-contact-form-for-static-websites): Learn how to create a serverless contact form for your static website.
* [Serverless Technology: Exploring Cloud Providers, Benefits, Challenges, and Kubernetes Integration](/serverless-technology-exploring-cloud-providers-benefits-challenges-and-kubernetes-integration): Dive deeper into the serverless landscape and grasp the fundamentals of how it operates.
* [Building Serverless OpenFaaS function to detect weather using OpenWeatherMap and Python](/building-openfaas-serverless-function-to-detect-weather-using-openweathermap-and-python): Discover another approach to building a serverless function using OpenFaaS, OpenWeatherMap API, and Python.

Don't just stop there; continue your journey and delve even further into the fascinating and expansive world of serverless technologies and their endless possibilities.