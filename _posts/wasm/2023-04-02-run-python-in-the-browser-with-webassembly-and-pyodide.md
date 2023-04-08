---
layout: post
comments: true
current: post
cover:  assets/images/posts/thibaut-marquis-LMqHSv8v5IU-unsplash_resized.jpg
navigation: True
title: "Run Python in the Browser with WebAssembly and Pyodide"
date: 2023-03-16 03:13:00
tags: [Wasm]
class: post-template
subclass: 'post tag-writings'
author: faizan
excerpt:  Discover how to run Python code directly in your web browser using WebAssembly and the Pyodide library. In this tutorial, you'll learn how to calculate the square of a number using Python and display the result in the browser.
---

# Run Python in WebAssembly with Pyodide
In recent years, WebAssembly (Wasm) has emerged as a powerful tool for running languages like Python in the browser. Pyodide, an open-source project, allows developers to execute Python code in WebAssembly, opening up new possibilities for web development. In this tutorial, we will guide you on using Pyodide to run Python code in WebAssembly and create a simple application to calculate the square of a number.

# Prerequisites
Before starting, ensure you have a modern web browser supporting WebAssembly. Most modern browsers like Google Chrome, Mozilla Firefox, and Microsoft Edge support WebAssembly.

***
# Table of Contents

* [Setting Up Pyodide](#setting-up-pyodide)
* [Creating the User Interface](#creating-the-user-interface)
* [Loading and Running Python Code](#loading-and-running-python-code)
* [Calling the Python Function from JavaScript](#calling-the-python-function-from-javascript)
* [Assembling the Pieces](#assembling-the-pieces)
* [Conclusion](#conclusion)

***

# Setting Up Pyodide
To begin, create a new HTML file named `index.html` and add the following content:

{% highlight html %}
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Run Python in WebAssembly with Pyodide</title>
  <script type="text/javascript" src="https://cdn.jsdelivr.net/pyodide/v0.23.0/full/pyodide.js"></script>
</head>
<body>
  <!-- Rest of the code goes here -->
</body>
</html>
{% endhighlight %}

This code sets up the necessary HTML structure and imports the Pyodide library.

# Creating the User Interface

Next, add a user interface to the `body` of the HTML file for user input and displaying the result:

{% highlight html %}
  <h1>Calculate the square of a number using Python in WebAssembly</h1>
  <input type="number" id="number" placeholder="Enter a number">
  <button id="calculate">Calculate</button>
  <p id="result"></p>
{% endhighlight %}

# Loading and Running Python Code
Now, let's define a Python function for calculating the square of a number using Pyodide:

{% highlight javascript %}
async function main() {
  let pyodide = await loadPyodide();
  console.log('Pyodide is ready to use!');

  // Load and run the Python code
  pyodide.globals.set("square", x => x*x)
  return pyodide
}
pyodide = main();
{% endhighlight %}

This code initializes Pyodide and defines a Python function named `square`.

# Calling the Python Function from JavaScript
With the Python function defined, we can now call it from JavaScript:

{% highlight javascript %}
const calculateButton = document.getElementById('calculate');
const numberInput = document.getElementById('number');
const resultElement = document.getElementById('result');

calculateButton.addEventListener('click', () => {
  const number = parseInt(numberInput.value);
  const result = pyodide.runPython(`square(${number})`);
  resultElement.textContent = `The square of ${number} is ${result}.`;
});
{% endhighlight %}

This above code attaches an event listener to the "Calculate" button, gets the number from the input field, and calls the `square` function from Python. The result is then displayed in a paragraph element.

# Assembling the Pieces

After putting all the pieces together, we have an `index.html` file containing all the code we discussed previously.

{% gist 2da33013c6ecc9220cf26076e42f3a75 %}

# Conclusion
In this tutorial, we demonstrated how to run Python code in WebAssembly using Pyodide and created a simple application for calculating the square of a number. By integrating Python and JavaScript, developers can leverage the power of Python alongside JavaScript in the browser, unlocking new possibilities for web development.

Experiment with Pyodide and WebAssembly to explore new ways of building web applications, and consider how these technologies can enhance your development process.

If you're interested in further exploring the world of web development and cloud technologies, I invite you to read our previous articles. Start with our "[Friendly Introduction to WebAssembly](/webassembly-a-friendly-introduction)", which provides an easy-to-understand overview of this powerful technology. For those looking to dive deeper into specific WASM technologies, check out our hands-on tutorial on [Golang WebAssembly](/running-golang-webassembly-in-the-browser-a-step-by-step-guide). These articles cover the basics and provide practical code examples to enhance your understanding and help you start your journey toward mastering web development and cloud technologies.