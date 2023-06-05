---
layout: post
comments: true
current: post
cover: assets/images/posts/nick-tiemeyer-tNGcZlycLtQ-unsplash_resized.webp
navigation: True
title: "Building a Basic gRPC Server and Client in Go"
date: 2023-06-05 11:11:11
tags: [Golang]
class: post-template
subclass: 'post tag-golang'
author: faizan
excerpt: Discover how to create a basic gRPC server and client using Go. This step-by-step guide, complete with code samples, makes it easy to understand and implement efficient microservices communication.
social_excrpt: "Explore the power of gRPC and Go in creating efficient, language-agnostic microservices. Our latest article is a step-by-step guide on building a basic gRPC server and client in Go. Dive in and learn more! 🚀💻 #GoLang #gRPC #Microservices"
---

# Building a Basic gRPC Server and Client in Go

In the ever-evolving world of microservices and distributed systems, gRPC provides a high-performance framework to build APIs. Its efficient binary serialization, and comprehensive support for numerous languages including Go, make it an excellent choice for communication between services. This article guides you through building a basic gRPC server and client in Go with complete code samples.

## Prerequisites

To follow along, ensure you have the following:

- Go installed (version `1.16` or later)
- Protocol Buffer Compiler installed
- Basic knowledge of Go programming language
- [Basic knowledge of gRPC](/introduction-to-grpc)

## Table of Contents

- [Introduction to gRPC and Protocol Buffers](#introduction-to-grpc-and-protocol-buffers)
- [Building a Basic gRPC Server in Go](#building-a-basic-grpc-server-in-go)
- [Building a gRPC Client in Go](#building-a-grpc-client-in-go)
- [Running and Testing the Application](#running-and-testing-the-application)
- [Conclusion](#conclusion)

## Introduction to gRPC and Protocol Buffers

gRPC is a high-performance, open-source framework developed by Google. It uses Protocol Buffers (protobuf) as its interface definition language, defining services and message types for communication.

First, we need to define our service using protobuf. Install the protobuf compiler and Go protobuf plugin:

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.26
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.1
```

## Code Structure

```bash
learninggrpc/
├── go.mod
├── pb/
│   ├── hello.pb.go
│   └── hello_grpc.pb.go
├── client/
│   └── main.go
└── server/
    └── main.go
```

```
git mod init learninggrpc
```

Now, let's create a `proto` file called `hello.proto` in the `pb` directory to define a simple `Hello` service:

```protobuf
syntax = "proto3";

option go_package = "learninggrpc/pb";

service HelloService {
    rpc SayHello (HelloRequest) returns (HelloResponse);
}

message HelloRequest {
    string greeting = 1;
}

message HelloResponse {
    string reply = 1;
}
```

## Building a Basic gRPC Server in Go

Once we have our service definition, we can proceed to build our gRPC server. First, we need to generate Go code from our `proto` file:

```bash
protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative hello.proto
```

Now, let's build our gRPC server:

```go
package main

import (
	"context"
	"log"
	"net"

	"learninggrpc/pb"
	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedHelloServiceServer
}

func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloResponse, error) {
	return &pb.HelloResponse{Reply: "Hello " + in.GetGreeting()}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterHelloServiceServer(s, &server{})
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
```

## Building a gRPC Client in Go

Now that we have our server, let's create a gRPC client to communicate with it:

```go
package main

import (
	"context"
	"log"
	"time"

	"learninggrpc/pb"
	"google.golang.org/grpc"
)

func main() {
	conn, err := grpc.Dial("localhost:50051", grpc.WithInsecure(), grpc.WithBlock())
	
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewHelloServiceClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	r, err := c.SayHello(ctx, &pb.HelloRequest{Greeting: "world"})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
	log.Printf("Greeting: %s", r.GetReply())
}
```

## Running and Testing the Application

Finally, start the server, and then run the client:

```bash
go run server.go
go run client.go
```

The client should print: "Greeting: Hello world".

## Conclusion

In this tutorial, we've walked through the steps of creating a basic gRPC server and client in Go. With gRPC, you can build efficient, high-performance microservices that are language-agnostic. If you're interested in delving deeper into gRPC's operational mechanics, data types, and how it powers efficient remote procedure calls, our comprehensive guide, [Introduction to gRPC](/introduction-to-grpc), is an excellent resource.