---
layout: post
comments: true
current: post
cover:  assets/images/posts/abdelrahman-ismail-9nsj6C5Vxhg-unsplash_resized.webp
navigation: True
title: "WebAssembly: A Friendly Introduction"
date: 2023-04-01 03:13:00
tags: [Wasm]
class: post-template
subclass: 'post tag-writings'
author: faizan
excerpt: Discover the power of WebAssembly in our beginner-friendly guide. Learn about its benefits, browser compatibility, and how to get started with hands-on examples. Unlock a new level of web performance today!
---

# Introduction to WebAssembly

## What is WebAssembly?
WebAssembly, often abbreviated as "wasm", is a binary instruction format designed as a portable target for compiling high-level languages like C, C++, and Rust. In addition, WebAssembly was intended as a low-level virtual machine that runs code at near-native speed in web browsers using standard hardware capabilities.

## Why WebAssembly is important
WebAssembly provides a new level of performance and flexibility for web developers. It allows for more efficient code execution than JavaScript, making it an ideal choice for computationally heavy tasks or real-time applications. Moreover, WebAssembly enables developers to use their preferred languages for web development, opening up new possibilities for code reuse and cross-platform development.

***

# Table of Contents:

* [WebAssembly: The Basics](#webassembly-the-basics)
  * [WebAssembly Concepts](#webassembly-concepts)
  * [WebAssembly vs. JavaScript](#webassembly-vs-javascript)
  * [WebAssembly Features](#webassembly-features)
* [Setting Up Your WebAssembly Development Environment](#setting-up-your-webassembly-development-environment)
  * [Required Tools and Libraries](#required-tools-and-libraries)
  * [Installing the WebAssembly Binary Toolkit (WABT)](#installing-the-webassembly-binary-toolkit-wabt)
* [Configuring Your Browser for WebAssembly](#configuring-your-browser-for-webassembly)
  * [Verifying WebAssembly Support](#verifying-webassembly-support)
  * [Enabling Experimental Features](#enabling-experimental-features)
  * [Debugging WebAssembly Issues](#debugging-webassembly-issues)
* [Creating a Simple WebAssembly Module](#creating-a-simple-webassembly-module)
  * [Writing a C Function](#writing-a-c-function)
  * [Compiling to WebAssembly](#compiling-to-webassembly)
  * [Loading and Running the WebAssembly Module](#loading-and-running-the-webassembly-module)
  * [Running the Web Server](#running-the-web-server)
* [Interacting with JavaScript and the DOM](#interacting-with-javascript-and-the-dom)
  * [Calling JavaScript Functions from WebAssembly](#calling-javascript-functions-from-webassembly)
  * [Manipulating the DOM with WebAssembly](#manipulating-the-dom-with-webassembly)
* [Working with WebAssembly Memory](#working-with-webassembly-memory)
  * [Understanding Linear Memory](#understanding-linear-memory)
  * [Sharing Memory Between WebAssembly and JavaScript](#sharing-memory-between-webassembly-and-javascript)
* [Optimizing WebAssembly Performance](#optimizing-webassembly-performance)
  * [WebAssembly Optimization Techniques](#webassembly-optimization-techniques)
  * [Debugging and Profiling WebAssembly Code](#debugging-and-profiling-webassembly-code)
* [Real-World Applications of WebAssembly](#real-world-applications-of-webassembly)
  * [Use Cases and Examples](#use-cases-and-examples)
  * [WebAssembly in Popular Frameworks and Libraries](#webassembly-in-popular-frameworks-and-libraries)
* [Conclusion](#conclusion)
  * [The Future of WebAssembly](#the-future-of-webassembly)
  * [Getting Involved in the WebAssembly Community](#getting-involved-in-the-webassembly-community)

***

# WebAssembly: The Basics

## WebAssembly Concepts
WebAssembly consists of a few core concepts:

* **Modules:** A WebAssembly module is a binary file containing compiled code and data.
* **Instances:** An instance represents a module's code, memory, and other resources loaded into a specific runtime environment.
* **Functions:** Functions are the basic building blocks of WebAssembly code, and they can be exported and called from JavaScript or other WebAssembly modules.
* **Linear Memory:** WebAssembly uses a linear memory model, where memory is represented as a contiguous array of bytes with a fixed size.

## WebAssembly vs JavaScript
While WebAssembly and JavaScript can coexist and complement each other, there are some key differences:

* **Performance:** WebAssembly code executes faster than JavaScript, making it suitable for performance-critical tasks.
* **Language Support:** WebAssembly allows developers to use languages other than JavaScript, enabling them to leverage existing codebases or use languages better suited for specific tasks.
* **Binary Format:** WebAssembly uses a compact binary format faster to decode and execute than JavaScript's text-based format.
* **Strong Typing:** WebAssembly is a strongly typed language, which can lead to more predictable performance and improved optimization by the compiler.

## WebAssembly Features
Some of the critical features of WebAssembly include:

* **Portability:** WebAssembly is designed to be a portable target for compiling high-level languages.
* **Security:** WebAssembly runs inside a sandboxed environment, providing isolation and security guarantees similar to JavaScript.
* **Integration:** WebAssembly is designed to integrate seamlessly with the existing web platform, allowing developers to leverage JavaScript APIs and interact with the DOM.
* **Compactness:** The binary format of WebAssembly is designed to be compact and efficient, both in terms of file size and execution speed.

# Setting Up Your WebAssembly Development Environment

## Required Tools and Libraries
To get started with WebAssembly development, you'll need the following tools:

* A WebAssembly-capable browser (e.g., Chrome, Firefox, Safari, or Edge)
* A integrated development environment (IDE) for writing code
* The Emscripten SDK, which includes tools for compiling C/C++ code to WebAssembly
* Use Node.js and npm, if you want additional development tools or libraries

## Installing the WebAssembly Binary Toolkit (WABT)
The WebAssembly Binary Toolkit (WABT) is a set of tools for working with WebAssembly binary files. To install WABT, follow the instructions on the [official GitHub repository](https://github.com/WebAssembly/wabt).

# Configuring Your Browser for WebAssembly

WebAssembly has been supported by all major browsers since 2017, including Chrome, Firefox, Safari, and Edge. In most cases, browsers are configured to enable WebAssembly by default, but there may be instances where you need to allow WebAssembly support manually. However, in this section, we'll discuss some steps you can take to ensure your browser is set up correctly to run WebAssembly code and to troubleshoot any issues you may encounter.



## Verifying WebAssembly Support
To check if your browser supports WebAssembly, you can visit the official [WebAssembly website](https://webassembly.org/) or use the following JavaScript code snippet:

{% highlight javascript%}
if (typeof WebAssembly === 'object') {
  console.log('WebAssembly is supported by your browser.');
} else {
  console.log('WebAssembly is not supported by your browser.');
}
{% endhighlight %}

If your browser does not support WebAssembly, consider updating it to the latest version or switching to another browser that supports WebAssembly.

## Enabling Experimental Features
Although WebAssembly is supported by default in modern browsers, some experimental features may be hidden behind feature flags. To enable these features, you can follow these steps for each browser:

* **Chrome:** Navigate to `chrome://flags`, search for "WebAssembly", and enable any relevant features.
* **Firefox:** Navigate to `about:config`, search for "WebAssembly", and toggle any relevant features.
* **Safari:** Enable the "Develop" menu in the "Advanced" tab of the "Preferences" window, and then navigate to "Develop" > "Experimental Features" to enable any relevant WebAssembly features.
* **Edge:** Navigate to `edge://flags`, search for "WebAssembly", and enable any relevant features.

Remember that enabling experimental features may cause instability or other issues in your browser. So use caution and only allow the features you need.

## Debugging WebAssembly Issues
If you encounter issues when running WebAssembly code in your browser, you can use the browser's built-in developer tools to help diagnose and fix the problem. In addition, most browsers provide debugging and profiling tools designed explicitly for WebAssembly, such as support for source maps, which allow you to debug your WebAssembly code at the source level.

To access the developer tools, right-click on the page and select "Inspect" or "Inspect Element". This will open the developer tools panel in a separate window or panel. From there, you can navigate to the "Console" tab to view any error messages or warnings related to WebAssembly, and to the "Sources" or "Debugger" tab to set breakpoints and step through your WebAssembly code.

# Creating a Simple WebAssembly Module

## Writing a C Function
To create a simple WebAssembly module, let's start by writing a C function that we'll compile to WebAssembly. First, create a file called `example.c` with the following content:

{% highlight c %}
#include <emscripten.h>

EMSCRIPTEN_KEEPALIVE
void call_showAlert() {
  EM_ASM({
    showAlert('Hello from WebAssembly!');
  });
}

int main() {
  call_showAlert();
  return 0;
}
{% endhighlight %}

## Compiling to WebAssembly
To compile the C function to WebAssembly, we'll use the Emscripten compiler. Run the following command:

{% highlight shell %}
emcc example.c -s WASM=1 -O3 -s "EXPORTED_RUNTIME_METHODS=['cwrap']" -o example.js
{% endhighlight %}

This command will generate two files: `example.wasm` (the WebAssembly binary) and `example.js` (a JavaScript loader for the WebAssembly module).

## Loading and Running the WebAssembly Module

Now, let's create an HTML file called `index.html` to load and run our WebAssembly module:

{% highlight html %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WebAssembly Example</title>
</head>
<body>
  <h1>WebAssembly: A Friendly Introduction</h1>

  <button onclick="callWebAssemblyFunction()">Call WebAssembly Function</button>

  <!-- Include the generated JavaScript file -->
  <script src="main.js"></script>
  <script>
    // showAlert function called from C code
    function showAlert(message) {
      alert(message);
    }

    // Load the WebAssembly module
    Module.onRuntimeInitialized = function() {
      console.log('WebAssembly module initialized');
    };

    // Optional: Function to call the WebAssembly function from the button
    function callWebAssemblyFunction() {
      // Get the exported function from the WebAssembly module
      const call_showAlert = Module.cwrap('call_showAlert', 'void', []);
      
      // Call the WebAssembly function
      call_showAlert();
    }
  </script>
</body>
</html>

{% endhighlight %}

## Running the Web Server

Serve the files using a local web server. For our example, we are using Python's built-in HTTP server. So, for instance, in the same directory as your `index.html`, `example.js`, and `example.wasm` files, run the following command:

{% highlight python %}
python -m http.server 8080
{% endhighlight %}

Navigate to `http://localhost:8080` in your browser. The `index.html` file should load,  executing the WebAssembly code and showing the alert dialogue with the message 'Hello from WebAssembly!'.

# Interacting with JavaScript and the DOM

## Calling JavaScript Functions from WebAssembly
To call a JavaScript function from your WebAssembly code, you can use the `EM_ASM` macro provided by Emscripten. For example, if you want to call a JavaScript function `showAlert` from your `C` code, you can do the following:

{% highlight c %}
#include <emscripten.h>

void call_showAlert() {
   EM_ASM({
     showAlert('Hello from WebAssembly!');
   });
}
{% endhighlight %}

## Calling WebAssembly Functions from JavaScript
As we saw earlier, you can use the `Module.cwrap` function provided by Emscripten to call WebAssembly functions from JavaScript. This function takes three arguments: the function's name to call, the return type, and an array of argument types.

## Manipulating the DOM with WebAssembly
Although WebAssembly does not have direct access to the DOM, you can still manipulate the DOM indirectly by calling JavaScript functions that interact with the DOM. For example, you can create a JavaScript function that updates the DOM and then call this function from your WebAssembly code using the `EM_ASM` macro.

# Working with WebAssembly Memory

## Understanding Linear Memory
WebAssembly uses a linear memory model, where memory is represented as a contiguous array of bytes with a fixed size. This memory can be accessed and modified using WebAssembly instructions or JavaScript.

## Sharing Memory Between WebAssembly and JavaScript
To share memory between WebAssembly and JavaScript, you can use the `Module.HEAP*` arrays provided by Emscripten. These arrays represent different views of the WebAssembly memory, allowing you to read and write values using different data types (e.g., `HEAP8` for 8-bit integers, `HEAP32` for 32-bit integers).

# Optimizing WebAssembly Performance

## WebAssembly Optimization Techniques
Some optimization techniques for WebAssembly include:

* Using Web Workers to run WebAssembly code off the main thread.
* Minimizing the size of the WebAssembly binary by removing unused code and compressing the binary.
* Using WebAssembly-specific optimization flags during compilation.

## Debugging and Profiling WebAssembly Code
To debug and profile WebAssembly code, you can use the browser's built-in developer tools. These tools support source maps, allowing you to debug and profile your WebAssembly code at the source level.

# Real-World Applications of WebAssembly

## Use Cases and Examples
Some use cases for WebAssembly include:

* High-performance web applications, such as games and multimedia editors.
* Running existing desktop applications in the browser.
* Implementing performance-critical parts of web frameworks and libraries.

## WebAssembly in Popular Frameworks and Libraries
Many popular web frameworks and libraries are starting to use WebAssembly to improve performance and enable new features. For example, the popular JavaScript framework Blazor uses WebAssembly to run .NET code in the browser.

# Conclusion

## The Future of WebAssembly
WebAssembly is an exciting technology that has the potential to revolutionize web development. As it continues to evolve and gain support from browser vendors and the developer community, we can expect to see more powerful and flexible web applications built using WebAssembly.

## Getting Involved in the WebAssembly Community
If you happen to be interested in learning more about WebAssembly or contributing to its development, you can join the [WebAssembly community on GitHub](https://github.com/WebAssembly), participate in [online forums and mailing lists](https://www.w3.org/community/webassembly/), and [attend conferences](https://wasmio.tech/) and [meetups](https://github.com/WebAssembly/meetings) dedicated to WebAssembly.

If you're interested in further exploring the world of web development and cloud technologies, I invite you to read our previous articles. For those looking to dive deeper into specific WASM technologies, check out our comprehensive guide on [Python in WebAssembly with Pyodide](/run-python-in-the-browser-with-webassembly-and-pyodide) or our hands-on tutorial on [Golang WebAssembly](/running-golang-webassembly-in-the-browser-a-step-by-step-guide). These articles cover the basics and provide practical code examples to enhance your understanding and help you start your journey toward mastering web development and cloud technologies.