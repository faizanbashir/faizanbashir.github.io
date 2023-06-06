---
layout: post
comments: true
current: post
cover: assets/images/posts/jaredd-craig-N2rRN9qW56A-unsplash_resized.webp
navigation: True
title: "Go for Data Processing: Working with CSV and JSON Files"
date: 2023-06-06 11:11:11
tags: [Golang]
class: post-template
subclass: 'post tag-golang'
author: faizan
excerpt: Dive into data processing with Go in this comprehensive guide. Learn how to read and write CSV and JSON files with complete code samples. Enhance your data processing skills and make your tasks simple and efficient with Go.
social_excrpt: "Enhance your data processing skills with our latest article on how to work with CSV and JSON files in Go. This comprehensive guide provides complete code samples to help you every step of the way."
---

# Go for Data Processing: Working with CSV and JSON Files

The Go language is known for its simplicity, efficiency, and powerful standard library, making it a great choice for data processing tasks. This article will provide a comprehensive guide to working with CSV and JSON files in Go.

# Prerequisites
- Go installed (version `1.16` or later)
- Basic knowledge of Go programming language

***

# Table of Contents:

* [Processing CSV Files in Go](#processing-csv-files-in-go)
  * [Reading CSV Files](#reading-csv-files)
  * [Writing CSV Files](#writing-csv-files)
* [Processing JSON Files in Go](#processing-json-files-in-go)
  * [Reading JSON Files](#reading-json-files)
  * [Writing JSON Files](#writing-json-files)
* [Conclusion](#conclusion)

***

# Processing CSV Files in Go

## Reading CSV Files

Let's start by reading a CSV file. Go has an in-built encoding/csv package for dealing with CSV data.

Create a new file `read_csv.go` and add the following code:

{% highlight go %}
package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
)

func main() {
	f, err := os.Open("data.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	r := csv.NewReader(f)

	records, err := r.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	for _, record := range records {
		fmt.Println(record)
	}
}
{% endhighlight %}

This code opens a file named `data.csv`, reads it as a CSV file, and prints each record (row).

## Writing CSV Files

Similarly, we can write CSV data with the `encoding/csv` package. The following code writes some data to a CSV file:

{% highlight go %}
package main

import (
	"encoding/csv"
	"log"
	"os"
)

func main() {
	f, err := os.Create("output.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	w := csv.NewWriter(f)
	defer w.Flush()

	data := [][]string{
		{"Name", "Age", "City"},
		{"Alice", "23", "New York"},
		{"Bob", "27", "San Francisco"},
	}

	for _, record := range data {
		if err := w.Write(record); err != nil {
			log.Fatal(err)
		}
	}
}
{% endhighlight %}

This code writes the data array to a file named `output.csv`.

# Processing JSON Files in Go

## Reading JSON Files

Go has an in-built `encoding/json` package for dealing with JSON data. The following code reads a JSON file:

{% highlight go %}
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
)

type Person struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
	City string `json:"city"`
}

func main() {
	f, err := os.Open("data.json")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	bytes, err := ioutil.ReadAll(f)
	if err != nil {
		log.Fatal(err)
	}

	var people []Person
	if err := json.Unmarshal(bytes, &people); err != nil {
		log.Fatal(err)
	}

	fmt.Println(people)
}
{% endhighlight %}

This code opens a file named `data.json`, reads it as a JSON file, and prints each object.

## Writing JSON Files

We can also write JSON data with the `encoding/json` package. Here is how to write some data to a JSON file:

{% highlight go %}
package main

import (
	"encoding/json"
	"log"
	"os"
)

type Person struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
	City string `json:"city"`
}

func main() {
	f, err := os.Create("output.json")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	people := []Person{
		{Name: "Alice", Age: 23, City: "New York"},
		{Name: "Bob", Age: 27, City: "San Francisco"},
	}

	bytes, err := json.Marshal(people)
	if err != nil {
		log.Fatal(err)
	}

	if _, err := f.Write(bytes); err != nil {
		log.Fatal(err)
	}
}
{% endhighlight %}

This code writes the people slice to a file named `output.json`.

# Conclusion

In this article, we explored how to use Go to read and write CSV and JSON files. With its powerful standard library, Go makes these common data processing tasks simple and efficient. Whether you're dealing with small data files or large datasets, Go is an excellent tool for your data processing needs.