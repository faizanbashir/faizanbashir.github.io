---
layout: post
comments: true
current: post
cover: assets/images/posts/usgs-5HT7p_DVJ3c-unsplash_resized.webp
navigation: True
title: "How to create CLI Applications in Go using Cobra and Viper"
date: 2023-04-24 11:11:11
tags: [Golang]
class: post-template
subclass: 'post tag-golang'
author: faizan
excerpt: Learn to build powerful CLI applications in Golang using the Cobra and Viper libraries. Follow step-by-step examples and explore popular applications using these libraries to enhance your Golang development skills.
social_excerpt: "🚀 Master the art of building powerful CLI applications in Golang using Cobra and Viper! Explore real-world examples and dive into popular applications that leverage these libraries. Don't miss out. Read our article now! #Golang #Cobra #Viper #CLI"
---

# How to create CLI Applications in Go using Cobra and Viper"
This article will go through a basic Go program that leverages the Cobra and Viper libraries to build a simple Command-Line Interface (CLI) application. The Cobra library is primarily used for creating robust modern CLI applications, and Viper is intended to work with Cobra for configuration solution purposes.

***

# Table of Contents:

* [Real World Uses-Case and Adoption in Open Source](#real-world-uses-case-and-adoption-in-open-source)
* [Importing Cobra and Viper](#importing-cobra-and-viper)
* [Adding a Persistent Flag](#adding-a-persistent-flag)
* [Setting Default Configuration](#setting-default-configuration)
* [Root Command's Run Function](#root-commands-run-function)
* [Executing the CLI](#executing-the-cli)
* [Using the CLI tool](#using-the-cli-tool)
* [Conclusion](#conclusion)

***

# Real World Uses-Case and Adoption in Open Source

Cobra and Viper are incredibly versatile libraries in Go and have found many real-world use cases.

Cobra is widely used for creating robust modern CLI (Command Line Interface) applications. With features like command nesting, global flags, and powerful help generation, it offers a comprehensive solution for creating complex command-based applications. Real-world applications include:

* Building tools for system administration.
* Automating repetitive tasks.
* Building testing frameworks.
* Creating CLIs for controlling larger software packages or services.

Viper, on the other hand, is designed for application configuration. It offers a unified API to access configuration variables from different sources - environment variables, command-line flags, configuration files in various formats (JSON, TOML, YAML), remote config systems, or direct values. Real-world applications include any software requiring flexible configuration, such as web servers, game servers, database connectors, etc.

Many famous open-source projects use Cobra and Viper. These include:

1. [Kubernetes (k8s)](https://github.com/kubernetes/kubernetes): Kubernetes, a widely adopted container orchestration system, uses Cobra for its CLI `kubectl`.
2. [Hugo](https://github.com/gohugoio/hugo): Hugo, a popular static site generator written in Go, uses Cobra and Viper. Cobra provides the CLI interface, and Viper handles the site configuration.
3. [Docker (CLI)](https://github.com/docker/cli): Docker, a platform that automates the deployment, scaling, and management of applications, uses Cobra for its command-line interface.
4. [CockroachDB](https://github.com/cockroachdb/cockroach): CockroachDB, an open-source, distributed SQL database, uses Cobra for its command-line interface.
5. [rkt](https://github.com/rkt/rkt): rkt, a security-minded, standards-based container runtime, uses Cobra for its CLI.
By adopting these libraries, these projects have been able to focus more on their core functionalities, leaving the complexities of command parsing, configuration management, and user interface to Cobra and Viper.

# Importing Cobra and Viper

Firstly, we import the necessary packages:

{% highlight golang %}
import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)
{% endhighlight %}

Here, `fmt` and `os` are standard Go libraries for formatting and operating system functionalities. The `cobra` and `viper` packages are used to build and manage the CLI configuration.

# Creating the CLI Root Command

The next step is to create the root command for the CLI. This command will be executed if no other subcommands are provided.

{% highlight golang %}
rootCmd := &cobra.Command{
    Use: "mycli",
    Short: "My CLI is a simple CLI application built with Cobra and Viper",
}
{% endhighlight %}

The `Use` field represents the command's name when called, and `Short` is the brief description of the command.

# Adding a Persistent Flag

Next, we add a persistent flag to the root command. As the name suggests, a persistent flag remains consistent across the entire CLI application.

{% highlight golang %}
rootCmd.PersistentFlags().StringVarP(&message, "message", "m","", "A custom message")
{% endhighlight %}

## Binding the Flag to Viper Configuration

After defining the flag, we bind it to Viper's configuration:

{% highlight golang %}
viper.BindPFlag("message", rootCmd.PersistentFlags().Lookup("message"))
{% endhighlight %}

This allows us to use Viper's features with the flag, such as default values and reading from a configuration file.

# Setting Default Configuration

Then we set the default values for our configurations. This value will be used if no other value is provided:

{% highlight golang %}
viper.SetDefault("message", "Welcome to my CLI configured with Viper!")
{% endhighlight %}

## Reading Configuration from a File

Next, we set up Viper to read configuration values from a file:

{% highlight golang %}
viper.SetConfigName("config")
viper.AddConfigPath(".")
err := viper.ReadInConfig()
if err != nil {
    fmt.Println("Unable to read config:", err)
}
{% endhighlight %}

Viper will look for a file named `config` in the current directory.

## Root Command's Run Function

We define what happens when the root command runs:

{% highlight golang %}
rootCmd.Run = func(cmd *cobra.Command, args []string) {
    message := viper.GetString("message")
    fmt.Println(message)
}
{% endhighlight %}

When the root command is run, it fetches the "message" configuration value and prints it out.

## Adding Subcommands

The next part of the code adds two subcommands to our CLI:

{% highlight golang %}
versionCmd := &cobra.Command{
    Use: "version",
    Short: "Print the version number of my

cli",
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println("mycli v0.1")
    },
}

sayHelloCmd := &cobra.Command{
    Use: "sayhello",
    Short: "Say Hello",
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Println("Hello!")
    },
}

rootCmd.AddCommand(versionCmd, sayHelloCmd)
{% endhighlight %}

The `version` command prints the version of our CLI, and the `sayhello` command prints "Hello!".

## Executing the CLI

Finally, the CLI application is executed:

{% highlight golang %}
if err := rootCmd.Execute(); err != nil {
    fmt.Println(err)
    os.Exit(1)
}
{% endhighlight %}

# Using the CLI tool

To use this CLI tool, first, you need to build it. Run `go build` in the directory with your Go source code to create an executable. For example, this command will produce an executable named `mycli` if your source code file is named `mycli.go`.

Once built, you can run the CLI tool using the `./mycli` command. Since we didn't provide subcommands, the root command will execute and print the message from the configuration or the default message.

To use the subcommands, append them after the executable's name. For example, the `./mycli version` will run the `version` subcommand and print `mycli v0.1`. Similarly, `./mycli sayhello` will run the `sayhello` subcommand and print `Hello!`.

The `message` flag can be passed to any command. It's a persistent flag, so it's available for all commands and subcommands. Use `-m` or `--message` to set the message. For instance, `./mycli -m "This is a custom message"` will print `"This is a custom message"` instead of the default message or the message from the configuration file.

To make changes to the configuration, you can create a `config.yaml` file in the same directory with your specified settings. For instance:

{% highlight yaml %}
message: "This is a message from the config file."
{% endhighlight %}

When you run the `./mycli` command now, it will print `"This is a message from the config file."`. If you pass a message with the `-m` flag, the flag's value will take precedence over the configuration file.

This simple CLI tool is very flexible. You can add as many commands and flags as you need and manage complex configurations with Viper.

If there's any error during execution, the program prints the error and exits with a status code of `1`, indicating a failure.

To call the `sayhello` and `version` subcommands of your CLI tool, you'll append them to the root command.

Here's how you'd use the `sayhello` command:

{% highlight yaml %}
./mycli sayhello
{% endhighlight %}

It should print out `Hello!` to the console when you run this.

And here's how you'd use the `version` command:

{% highlight yaml %}
./mycli version
{% endhighlight %}

When you run this, it should print out `mycli v0.1` to the console.

These subcommands are called directly from the command line and execute the respective function associated with them in your Go program. For example, the `sayhello` subcommand triggers the function that prints out `Hello!`, while the `version` subcommand triggers the function that prints out `mycli v0.1`.

You can add the `-m` or `--message` flag to these commands if you want to display a custom message instead. For example:

{% highlight yaml %}
./mycli sayhello -m "Custom Hello Message!"
{% endhighlight %}

This would print `Custom Hello Message!` instead of the default `Hello!`. Similarly, you can add the message flag to the `version` command.

# Conclusion

This code creates a straightforward command-line interface (CLI) application using Go's Cobra and Viper libraries. It has a root command with a persistent flag and two subcommands. Viper is used for managing the application's configuration, including default values and reading from a configuration file. You can extend this example to build complex CLI applications with multiple commands, flags, and configuration options.