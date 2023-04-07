---
layout: post
comments: true
current: post
cover:  assets/images/posts/math-PJrkLbUqMzQ-unsplash_resized.jpg
navigation: True
title: "Running Golang WebAssembly in the Browser: A Step-By-Step Guide"
date: 2023-03-15 03:13:00
tags: [Wasm]
class: post-template
subclass: 'post tag-writings'
author: faizan
excerpt:  Learn how to create a simple Go WebAssembly application in this step-by-step guide, including setting up the environment, creating the Go code, and integrating with JavaScript.
---

# Running Golang WebAssembly in the Browser

WebAssembly, often abbreviated as "wasm", is a binary instruction format designed as a portable target for compiling high-level languages like C, C++, and Rust. In addition, WebAssembly was intended as a low-level virtual machine that runs code at near-native speed in web browsers using standard hardware capabilities.


# Prerequisites
* [Go](https://golang.org/dl/) installed on your system (version `1.11` or later)
* A modern web browser that supports WebAssembly
* A basic understanding of Go and JavaScript

***

# Table of Contents:
* [Setting Up the Go Environment for WebAssembly](#setting-up-the-go-environment-for-webassembly)
* [Creating the Go Code](#creating-the-go-code)
* [Compiling the Go Code to WebAssembly](#compiling-the-go-code-to-webassembly)
* [Creating the HTML file with JavaScript](#creating-the-html-file-with-javascript)
* [Running the Application](#running-golang-webassembly-in-the-browser)
* [Conclusion](#conclusion)

***

# Setting Up the Go Environment for WebAssembly

First, make sure your Go environment is set up correctly. You should have Go installed and configured on your system. If you don't have Go installed, download it from the [official Go website](https://golang.org/dl/).

{% highlight shell %}
go version
{% endhighlight %}

You're all set if you have Go version `1.11` or later.

# Creating the Go Code

Create a new Go file named `main.go` and add the following code:

{% highlight golang %}
package main

import (
  "fmt"
  "strconv"
  "syscall/js"
)

func multiply(this js.Value, inputs []js.Value) interface{} {
  a, _ := strconv.Atoi(inputs[0].String())
  b, _ := strconv.Atoi(inputs[1].String())
  return a * b
}

func main() {
  c := make(chan struct{}, 0)
  js.Global().Set("multiply", js.FuncOf(multiply))
  <-c
}
{% endhighlight %}

This code defines a simple Go function, `multiply`, that takes two integers and returns their product. The `multiply` function is then exposed to JavaScript via the `js.Global().Set()` method.

# Compiling the Go Code to WebAssembly

Next, compile the Go code to WebAssembly with the following command:

{% highlight shell %}
GOOS=js GOARCH=wasm go build -o main.wasm main.go
{% endhighlight %}

This command will create a `main.wasm` file in the current directory.

# Creating the HTML file with JavaScript

Create a new file named `index.html` and add the following content:

{% highlight html %}
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Go WebAssembly: Multiply Two Numbers</title>
  <script src="wasm_exec.js"></script>
</head>
<body>
  <h1>Multiply Two Numbers with Go WebAssembly</h1>
  <input type="number" id="number1" placeholder="Enter the first number">
  <input type="number" id="number2" placeholder="Enter the second number">
  <button id="calculate">Multiply</button>
  <p id="result"></p>

  <script>
    const go = new Go();
    WebAssembly.instantiateStreaming(fetch("main.wasm"), go.importObject).then((result) => {
      go.run(result.instance);

      const calculateButton = document.getElementById("calculate");
      const number1Input = document.getElementById("number1");
      const number2Input = document.getElementById("number2");
      const resultElement = document.getElementById("result");

      calculateButton.addEventListener("click", () => {
        const number1 = parseInt(number1Input.value);
        const number2 = parseInt(number2Input.value);
        const result = window.multiply(number1, number2);
        resultElement.textContent = `The product of ${number1} and ${number2} is ${result}.`;
      });
    });
  </script>
</body>
</html>
{% endhighlight %}

This HTML file sets up the input fields for the user to enter two numbers and a button to trigger the calculation. Next, the JavaScript code initializes the WebAssembly instance, loads the `main.wasm` file, and runs the Go WebAssembly code.

When the user clicks the "Multiply" button, it takes the input values, calls the `multiply` function exported from Go, and displays the result in the `result` paragraph element.

# Running the Application

To run the application using a web server, you must serve the `index.html`, `main.wasm`, and `wasm_exec.js` files. You can use any web server of your choice. In this example, we'll use the Python built-in HTTP server. First, copy the `wasm_exec.js` file from your Go installation's `misc/wasm` directory to your project folder:

{% highlight shell %}
cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" .
{% endhighlight %}

Now, run the web server using the following command in the terminal:

{% highlight shell %}
python -m http.server 8080
{% endhighlight %}

This command starts an HTTP server on port `8080`. First, navigate to `http://localhost:8080` in your browser of choice. Next, you should see a button that says, "Multiply 6 and 7." Click the button, and "The result is 42." should appear below it.

# Conclusion

In this article, we demonstrated how to create a simple Go WebAssembly application and interact with it using JavaScript. We could call the Golang function directly from JavaScript by setting up the Go environment, writing a Go function, and compiling it to WebAssembly. This technique opens up new possibilities for web development, enabling developers to leverage the power of Go alongside JavaScript in the browser.

If you're interested in further exploring the world of web development and cloud technologies, I invite you to read our previous articles. Start with our "[Friendly Introduction to WebAssembly](https://faizanbashir.me/webassembly-a-friendly-introduction)", which provides an easy-to-understand overview of this powerful technology. For those looking to dive deeper into specific WASM technologies, check out our guide on [Python in WebAssembly with Pyodide](https://faizanbashir.me/run-python-in-the-browser-with-webassembly-and-pyodide). These articles cover the basics and provide practical code examples to enhance your understanding and help you start your journey toward mastering web development and cloud technologies.