# Introduction

Building web applications can become complex and time consuming when a number of technologies are involved. A web application built on the blazing fast Golang provides developers a benefits of a well designed modern programming language. To continue the scalability of a developer’s tech stack, MongoDB is a NoSQL database is designed to scale and work with frequent changes. Developers can use Docker to simplify the process of packaging and deploying their applications.

Docker Compose has further simplified the development environment by allowing you to define your infrastructure, including your application services, network volumes, and bind mounts, in a single file. Using Docker Compose provides ease of use over running multiple `docker container run` commands. It allows you to define all your services in a single Compose file, and with a single command you create and start all the services from your configuration. This ensures that there is version control throughout your container infrastructure. Docker Compose uses a project name to isolate environments from each other, this allows you to run multiple environments on a single host.

In this tutorial you will build, package, and run your to-do web application with Golang, and MongoDB inside of Docker containers. You will define the entire stack configuration in a docker-compose.yml file, along with configuration files for Golang application and MongoDB. We will be using the Gorilla Mux router in Golang, to serve the application. MongoDB provides a persitence layer to the application as the todo items will be stored in MongoDB and can be accessed across multiple restarts.

## Prerequisites
To follow this tutorial, you will need the following:

1. [A non-root user with sudo privileges configured by following the steps in the Initial Server Setup tutorial.](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
2. [Docker installed with the instructions from Step 1 and Step 2 of How To Install and Use Docker.](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-sudo-enabled-user-on-ubuntu-20-04-quickstart)
3. Docker Compose installed with the instructions from Step 1 of How To Install Docker Compose.

# Step 1 -- The Docker Compose file. A walkthrough of the docker-compose file and its configuration.
Building your applications on Docker allows you to version infrastructure easily depending on configuration changes you make in Docker Compose. The infrastructure can be defined in a single file and built with a single command. In this step, you will set up the `docker-compose.yml` file to run your Go Todo application.

The `docker-compose.yml` file lets you define your application infrastructure as individual services. The services can be connected to each other and each can have a volume attached to it for persistent storage. Volumes are stored in a part of the host filesystem managed by Docker (`/var/lib/docker/volumes/` on Linux).

Volumes are the best way to persist data in Docker, as the data in the volumes can be exported or shared with other applications.

To get started, create a directory for the application in the home directory on your server:

```sh
mkdir goapp
Move into the newly created directory:

cd goapp
```

Next, create the `docker-compose.yml` file:

```sh
nano docker-compose.yml
```

The `docker-compose.yml` file starts with a version number that identifies the Docker Compose file version. Docker Compose file version `3` targets Docker Engine version `1.13.0+`, which is a prerequisite for this setup. You will also add the services tag that you will define in the next step:

```sh
nano docker-compose.yml

version: '3'
services:
```

You will now define todo as the first service in your `docker-compose.yml` file. Add the following code to define the Golang Todo service:

```yml
docker-compose.yml
. . .
  todo:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: todo
    image: faizanbashir.me/todo:latest
    restart: on-failure
    tty: true
    environment:
      DB_PORT: ${DB_PORT}
      DB_HOSTNAME: ${DB_HOSTNAME}
      DB_USERNAME: ${DB_USERNAME}
      DB_DATABASE: ${DB_DATABASE}
      DB_PASSWORD: ${DB_PASSWORD}
      SERVER_PORT: ${SERVER_PORT}
      SERVER_HOST: ${SERVER_HOST}
      SERVER_READ_TIMEOUT: ${SERVER_READ_TIMEOUT}
      SERVER_WRITE_TIMEOUT: ${SERVER_WRITE_TIMEOUT}
    ports:
      - "8080:8080"
    networks:
      - app-network
```

The `build` property defines the `context` of the build. In this case, the current folder that will contain the `Dockerfile`.

You use the `container_name` property to define a name for each container. The `image` property specifies the image name and what the Docker image will be tagged as. The `restart` property defines how the container should be restarted—in your case it is `on-failure`. This means your containers will only be stopped when the Docker Engine is stopped/restarted or when you explicitly stop the containers. The benefit of using the `on-failure` property is that the containers will start automatically once the Docker Engine is restarted or any error occurs.

The `environment` property contains the environment variables that are passed to the container. You need to provide a secure password for the environment variable `DB_PASSWORD`.

The `networks` property specifies the networks the Todo service will have access to.

With the Todo service defined, you’re ready to add the MongoDB configuration to the file. In this example, you will use the official `6.0.4` version mongo image. Add the following code to your `docker-compose.yml` file following the flask service:

```yml
docker-compose.yml
. . .
  mongodb:
    image: mongo:6.0.4
    container_name: mongodb
    restart: unless-stopped
    command: mongod --auth
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${DB_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${DB_PASSWORD}
      MONGO_INITDB_DATABASE: ${DB_DATABASE}
      MONGODB_DATA_DIR: ${DB_DATA_DIR}
      MONDODB_LOG_DIR: ${DB_LOG_DIR}
    volumes:
      - todo-data:/data/db
    networks:
      - app-network
```

The `container_name` for this service is `mongodb` with a `restart` policy of `unless-stopped`. You use the command property to define the command that will be executed when the container is started. The command `mongod --auth` will disable logging into the MongoDB shell without credentials, which will secure MongoDB by requiring authentication.

The environment variables `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD` create a root user with the given credentials, so be sure to replace the placeholder with a strong password.

MongoDB stores its data in /data/db by default, but we can define a designated folder for the data to be written to the named volume `todo-data` for persistence. As a result you won’t lose your databases in the event of a restart. The `mongodb` service exposes the default port `27017`.

Next, you will create `bridge` networks to allow the containers to communicate with each other. Append the following lines to the end of your file:

```yml
docker-compose.yml
. . .
networks:
  app-network:
    driver: bridge
```

You defined one networks the `app-network` the services to connect to.

Next, you will use volumes to persist the database, application, and configuration files. Since your application will use the databases and files, it is imperative to persist the changes made to them. The volumes are managed by Docker and stored on the filesystem. Add this code to the `docker-compose.yml` file to configure the volumes:

```yml
docker-compose.yml
. . .
volumes:
  todo-data:
    driver: local
```

The `volumes` section declares the volumes that the application will use to persist data. Here you have defined the volume `todo-data` for persisting your MongoDB databases. The volume uses a local driver to store the data locally. The volumes are used to persist this data so that your MongoDB data could be lost once you restart the containers.

Your complete `docker-compose.yml` file will look like this:

```yml
docker-compose.yml
version: '3.3'

services:

  todo:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: todo
    image: faizanbashir.me/todo:latest
    restart: on-failure
    tty: true
    environment:
      DB_PORT: ${DB_PORT}
      DB_HOSTNAME: ${DB_HOSTNAME}
      DB_USERNAME: ${DB_USERNAME}
      DB_DATABASE: ${DB_DATABASE}
      DB_PASSWORD: ${DB_PASSWORD}
      SERVER_PORT: ${SERVER_PORT}
      SERVER_HOST: ${SERVER_HOST}
      SERVER_READ_TIMEOUT: ${SERVER_READ_TIMEOUT}
      SERVER_WRITE_TIMEOUT: ${SERVER_WRITE_TIMEOUT}
    ports:
      - "8080:8080"
    networks:
      - app-network

  mongodb:
    image: mongo:6.0.4
    container_name: mongodb
    restart: on-failure
    command: mongod --auth
    ports:
      - "27017:27017"
    environment:
      MONGODB_DATABASE: ${DB_DATABASE}
      MONGO_INITDB_ROOT_USERNAME: ${DB_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${DB_PASSWORD}
      MONGODB_DATA_DIR: ${DB_DATA_DIR}
      MONDODB_LOG_DIR: ${DB_LOG_DIR}
    volumes:
      - todo-data:/data/db
    networks:
      - app-network

#Docker Networks
networks:
  app-network:
    driver: bridge
#Volumes
volumes:
  todo-data:
    driver: local
```

Save the file and exit the editor after verifying your configuration.

You’ve defined the Docker configuration for your entire application stack in the `docker-compose.yml` file. You will now move on to writing the `Dockerfile` for our Golang Todo application.

## Step 1.1 — Writing the Golang Todo application Dockerfile
With Docker, you can build containers to run your applications from a file called `Dockerfile`. The Dockerfile is a tool that enables you to create custom images that you can use to install the software required by your application and configure your containers based on your requirements. You can push the custom images you create to Docker Hub or any private registry.

In this step, you’ll write the `Dockerfile` for the Golang Todo application service. To get started, create the `Dockerfile` in the current directory:

```sh
nano Dockerfile
```

Add the following code to the `Dockefile`:

```Dockerfile
FROM golang:1.17.0-alpine3.13 AS builder
LABEL MAINTAINER="Faizan Bashir <faizan.ibn.bashir@gmail.com>"

WORKDIR /go/src/app

COPY . .

RUN go mod tidy

RUN CGO_ENABLED=0 GOOS=linux go build -o /go/bin/todo

# Multi Stage build
FROM alpine:3.13

# Labelling the image
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL maintainer="faizanbashir" \
  org.opencontainers.image.created=$BUILD_DATE \
  org.opencontainers.image.url="https://github.com/faizanbashir/k8s-golang-mongodb" \
  org.opencontainers.image.source="https://github.com/faizanbashir/k8s-golang-mongodb" \
  org.opencontainers.image.version=$VERSION \
  org.opencontainers.image.revision=$REVISION \
  org.opencontainers.image.vendor="faizanbashir" \
  org.opencontainers.image.title="k8s-golang-mongodb" \
  org.opencontainers.image.description="Golang Todo API" \
  org.opencontainers.image.licenses="Apache"

```

In this `Dockerfile`, you are creating an image on top of the `golang:1.17.0-alpine3.13` image that is based on Alpine `3.13` with Golang `1.17.0` pre-installed as the build container. Once the binary is built in the `builder`, we will create a new stage in the build which will use `alpine:3.13` as the base image. The `LABEL` directive is used to add labels to the container with some metadata. The `RUN` directive is used to create a group, add a user and install a few softare packages.

The `ARG` directive is used to define the environment variables.

Add the following code block to copy the Flask application into the container and install the necessary dependencies:

```Dockerfile
. . .
RUN addgroup -S app \
  && adduser -S -g app app \
  && apk --no-cache add \
  curl openssl netcat-openbsd iputils

WORKDIR /home/app

COPY --from=builder /go/bin/todo .
RUN chown -R app:app ./

HEALTHCHECK CMD curl -sS http://localhost:8080/todo/healthz || exit 1

USER app

EXPOSE 8080

CMD [ "./todo" ]
```

The `WORKDIR` directive defines the working directory for the container. Be sure to replace the `LABEL MAINTAINER` field with your name and email address.

The `COPY` directive us used to copy from the `builder` stage into the `alpine`, next we set the ownership using the `RUN chown` command. The `HEALTHCHECK` directive is used to run a curl command to the health check url to see if everything is working fine. The `USER` directive is used to set the `app` user which created previously. Finally the `EXPOSE` command is used to expose a port in our case port `8080` and the `CMD` directive is used to set the command that starts the application, in our case `./todo`.

Your completed Dockerfile will look like the following:

```Dockerfile
FROM golang:1.17.0-alpine3.13 AS builder
LABEL MAINTAINER="Faizan Bashir <faizan.ibn.bashir@gmail.com>"

WORKDIR /go/src/app

COPY . .

RUN go mod tidy

RUN CGO_ENABLED=0 GOOS=linux go build -o /go/bin/todo

# Multi Stage build
FROM alpine:3.13

# Labelling the image
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL maintainer="faizanbashir" \
  org.opencontainers.image.created=$BUILD_DATE \
  org.opencontainers.image.url="https://github.com/faizanbashir/k8s-golang-mongodb" \
  org.opencontainers.image.source="https://github.com/faizanbashir/k8s-golang-mongodb" \
  org.opencontainers.image.version=$VERSION \
  org.opencontainers.image.revision=$REVISION \
  org.opencontainers.image.vendor="faizanbashir" \
  org.opencontainers.image.title="k8s-golang-mongodb" \
  org.opencontainers.image.description="Golang Todo API" \
  org.opencontainers.image.licenses="Apache"

RUN addgroup -S app \
  && adduser -S -g app app \
  && apk --no-cache add \
  curl openssl netcat-openbsd iputils

WORKDIR /home/app

COPY --from=builder /go/bin/todo .
RUN chown -R app:app ./

HEALTHCHECK CMD curl -sS http://localhost:8080/todo/healthz || exit 1

USER app

EXPOSE 8080

CMD [ "./todo" ]
```

Save the file and exit the text editor.

# Step 2 -- Persistent Data. Going through the configuration and the persistent data requirements for the project.

Since your application will use the databases and files, it is imperative to persist the changes made to them. The volumes are managed by Docker and stored on the filesystem. Add this code to the `docker-compose.yml` file to configure the volumes:

```yml
docker-compose.yml
. . .
volumes:
  todo-data:
    driver: local
```

The `volumes` section declares the volumes that the application will use to persist data. Here you have defined the volume `todo-data` for persisting your MongoDB databases. The volume uses a local driver to store the data locally. The volumes are used to persist this data so that your MongoDB data could be lost once you restart the containers.

# Step 3 -- Configuring Golang. Configuring Golang to connect with the MongoDB database
Now that you’ve built out your environment, you’re ready to build your application. In this step, you will write a Todo API application that will save and display Todo notes sent in from a POST request.

Get started by creating the main.go file in the root directory:

```sh
touch main.go
```

Next we want to initialise a module in Go.

```sh
go mod init main
```

Next we start writing our Golang Todo application:

```go
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/kelseyhightower/envconfig"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)
```

The `package main` directive define that this is the main file of our program since we intent it to be the entrypoint of our application. Next up we imported all required packages to be used be our program into the `import` section.

Next we will create the data structure for our program used to connect to the database, expose the server and define the Todo table structure.

```go
// The Config struct contains Application configuration
type Config struct {
	Server struct {
		Host         string        `envconfig:"SERVER_HOST"`
		Port         string        `envconfig:"SERVER_PORT"`
		ReadTimeout  time.Duration `envconfig:"SERVER_READ_TIMEOUT"`
		WriteTimeout time.Duration `envconfig:"SERVER_WRITE_TIMEOUT"`
	}
	Database struct {
		DB       string `envconfig:"DB_DATABASE"`
		Username string `envconfig:"DB_USERNAME"`
		Password string `envconfig:"DB_PASSWORD"`
		Hostname string `envconfig:"DB_HOSTNAME"`
		Port     int    `envconfig:"DB_PORT"`
	}
}

// A Todo struct contains data like todo, creation and completion date
type Todo struct {
	ID        primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	Todo      string             `bson:"todo,omitempty" json:"todo"`
	Done      bool               `bson:"done,omitempty" json:"done,omitempty"`
	CreatedAt time.Time          `bson:"created_at,omitempty" json:"created_at"`
}
```

The `Config` struct is composed of two structs `Server` and `Database`. The `Server` struct is used to expose the `Host`, `Port`, `ReadTimeout` and `WriteTimeout` for our API Server. The `Database` is used to connect to the database. The values are loaded from a `.env` file present in the root directory, the library `envconfig` provides the functionality for mapping the values in the `.env` file to the `Server` and `Database` structs.

Next up the `Todo` struct serves as a database model storing the MongoDB ID, the todo item, a boolean field denoting whether the todo was completed and the todo item creation time. Next up we will be loading the configuration values from the `.env` file into the `Server` and `Database` structs.

```go
var db *mongo.Database

var cfg Config

func init() {
	loadENV(&cfg)
	err := connectDB()
	if err != nil {
		log.Fatal(err)
	}
}

func loadENV(cfg *Config) {
	err := envconfig.Process("", cfg)
	if err != nil {
		log.Fatal(err)
	}
}
```

In the above code snipped we are initialising the `db` varible of type `*mongo.Database`, next we are initialising a variable `cfg` of type `Config` struct which we defined in the previous snippet. The `init` function calls the `loadENV` function to initialise the configuration object from the values provided in the `.env` file. Next up we call the `connectDB` function to initalise the database, we will define the function in the snippet given below:

```go
func connectDB() error {
	connectionString := fmt.Sprintf("mongodb://%s:%s@%s:%d/%s", cfg.Database.Username, cfg.Database.Password, cfg.Database.Hostname, cfg.Database.Port, cfg.Database.DB)
	fmt.Println(connectionString)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(connectionString))
	if err != nil {
		fmt.Println(" [-] Failed connecting to MongoDB!")
		return err
	}
	err = client.Ping(ctx, readpref.Primary())
	if err != nil {
		fmt.Println(" [-] Failed pinging MongoDB!")
		return err
	}

	fmt.Println(" [+] Connected to MongoDB!")
	db = client.Database(cfg.Database.DB)

	return nil
}
```

The `connectDB` function builds a connection string from the values present in the configuration variable `cfg`. Next we create a `context` object to pass to the db connection the context object has a timeout of 10 seconds. We use the `mongo.Connect` function to connect to the database, we print error message in case the connection errors out. Next we try to ping the MongoDB to establish that we have successfully connected to the MongoDB database. Finally the connection object is stored in the previouly degined `db` variable.

```go
func main() {
	fmt.Println("Initializing web server!")
	log.Fatal(run())
}

func run() error {
	mux := makeMuxRouter()
	httpAddr := cfg.Server.Port
	log.Println("Listening on:", httpAddr)
	server := &http.Server{
		Addr:           ":" + httpAddr,
		Handler:        mux,
		ReadTimeout:    cfg.Server.ReadTimeout * time.Second,
		WriteTimeout:   cfg.Server.WriteTimeout * time.Second,
		MaxHeaderBytes: 1 << 20,
	}

	if err := server.ListenAndServe(); err != nil {
		return err
	}
	return nil
}

func makeMuxRouter() http.Handler {
	router := mux.NewRouter()

	api := router.PathPrefix("/todo").Subrouter()
	api.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Welcome to Golang TODO app!"}`))
	}).Methods(http.MethodGet)
	api.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status": "OK"}`))
	}).Methods(http.MethodGet)
	api.HandleFunc("/list", getTodo).Methods(http.MethodGet)
	api.HandleFunc("/create", addTodo).Methods(http.MethodPost)
	return api
}
```

The `main` function is the entrypoint to the program, but the `init` function is executed before the main function for initialising required objects. The `run` function is used to create a web server and the `makeMuxRouter` function is used to define the routes for our Todo application. Next up we will define the handlers for our routes.

```go
func getTodo(w http.ResponseWriter, r *http.Request) {
	collection := db.Collection("todo")

	var todos []Todo
	findOptions := options.Find()
	findOptions.SetLimit(20)

	cur, err := collection.Find(context.TODO(), bson.D{}, findOptions)
	if err != nil {
		log.Fatal(err)
	}

	for cur.Next(context.TODO()) {
		var elem Todo
		err := cur.Decode(&elem)
		if err != nil {
			log.Fatal(err)
		}
		todos = append(todos, elem)
	}

	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}

	cur.Close(context.TODO())
	fmt.Printf("Found multiple documents: %+v\n", todos)
	out, err := json.MarshalIndent(todos, "", "  ")
	if err != nil {
		http.Error(w, fmt.Sprintf("Unable to get todos: %s", err.Error()), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(out)
}

func addTodo(w http.ResponseWriter, r *http.Request) {
	var todo Todo
	err := json.NewDecoder(r.Body).Decode(&todo)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	err = insert(todo)
	if err != nil {
		http.Error(w, fmt.Sprintf("Unable to add todo: %s", err.Error()), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"status": "OK", "message": "Added TODO!"}`))
}

func insert(todo Todo) error {
	collection := db.Collection("todo")

	todo.CreatedAt = time.Now()
	fmt.Println(todo.Todo)

	insertResult, err := collection.InsertOne(context.TODO(), todo)
	if err != nil {
		return err
	}
	fmt.Println(insertResult.InsertedID)
	return nil
}
```

The `getTodo` function is used to retreieve Todo items from the MongoDB database, this will return a maximum of 20 Todo items from the database. Finally we are marshalling them to be returned as response in the form of json objects. The `addTodo` function adds a Todo item into the database, it calls the `insert` function to add the item to the database. Finally returning with a message about the status of the addition.

# Step 4 -- Installing the Go packages. Next, install the required GoLang packages.
Conclusion. A wrap-up and recap of the steps.

To install the dependencies we need to run the following command:

```go
go mod tidy
```

To run the application we can use the following command:

```go
go run ./main.go
```

The dependencies referenced in the `main.go` file are added to the `go.mod` file. The implementation of this tutorial will use `Gorilla Mux`, `Kelseyhightower Envconfig`, and `Mongo-Driver`. Our go.mod file will look something like the follwing:

```go
module faizanbashir.me/todo

go 1.17

require (
	github.com/gorilla/mux v1.7.4
	github.com/kelseyhightower/envconfig v1.4.0
	go.mongodb.org/mongo-driver v1.3.5
)
```

Finally our `main.go` file will look something like this:

```go
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"github.com/kelseyhightower/envconfig"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

// The Config struct contains Application configuration
type Config struct {
	Server struct {
		Host         string        `envconfig:"SERVER_HOST"`
		Port         string        `envconfig:"SERVER_PORT"`
		ReadTimeout  time.Duration `envconfig:"SERVER_READ_TIMEOUT"`
		WriteTimeout time.Duration `envconfig:"SERVER_WRITE_TIMEOUT"`
	}
	Database struct {
		DB       string `envconfig:"DB_DATABASE"`
		Username string `envconfig:"DB_USERNAME"`
		Password string `envconfig:"DB_PASSWORD"`
		Hostname string `envconfig:"DB_HOSTNAME"`
		Port     int    `envconfig:"DB_PORT"`
	}
}

// A Todo struct contains data like todo, creation and completion date
type Todo struct {
	ID        primitive.ObjectID `bson:"_id,omitempty" json:"id"`
	Todo      string             `bson:"todo,omitempty" json:"todo"`
	Done      bool               `bson:"done,omitempty" json:"done,omitempty"`
	CreatedAt time.Time          `bson:"created_at,omitempty" json:"created_at"`
}

var db *mongo.Database

var cfg Config

func init() {
	loadENV(&cfg)
	err := connectDB()
	if err != nil {
		log.Fatal(err)
	}
}

func loadENV(cfg *Config) {
	err := envconfig.Process("", cfg)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	fmt.Println("Initializing web server!")
	log.Fatal(run())
}

func run() error {
	mux := makeMuxRouter()
	httpAddr := cfg.Server.Port
	log.Println("Listening on:", httpAddr)
	server := &http.Server{
		Addr:           ":" + httpAddr,
		Handler:        mux,
		ReadTimeout:    cfg.Server.ReadTimeout * time.Second,
		WriteTimeout:   cfg.Server.WriteTimeout * time.Second,
		MaxHeaderBytes: 1 << 20,
	}

	if err := server.ListenAndServe(); err != nil {
		return err
	}
	return nil
}

func makeMuxRouter() http.Handler {
	router := mux.NewRouter()

	api := router.PathPrefix("/todo").Subrouter()
	api.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"message": "Welcome to Golang TODO app!"}`))
	}).Methods(http.MethodGet)
	api.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status": "OK"}`))
	}).Methods(http.MethodGet)
	api.HandleFunc("/list", getTodo).Methods(http.MethodGet)
	api.HandleFunc("/create", addTodo).Methods(http.MethodPost)
	return api
}

func connectDB() error {
	connectionString := fmt.Sprintf("mongodb://%s:%s@%s:%d/%s", cfg.Database.Username, cfg.Database.Password, cfg.Database.Hostname, cfg.Database.Port, cfg.Database.DB)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(connectionString))
	if err != nil {
		fmt.Println(" [-] Failed connecting to MongoDB!")
		return err
	}
	err = client.Ping(ctx, readpref.Primary())
	if err != nil {
		fmt.Println(" [-] Failed pinging MongoDB!")
		return err
	}

	fmt.Println(" [+] Connected to MongoDB!")
	db = client.Database(cfg.Database.DB)

	return nil
}

func getTodo(w http.ResponseWriter, r *http.Request) {
	collection := db.Collection("todo")

	var todos []Todo
	findOptions := options.Find()
	findOptions.SetLimit(20)

	cur, err := collection.Find(context.TODO(), bson.D{}, findOptions)
	if err != nil {
		log.Fatal(err)
	}

	for cur.Next(context.TODO()) {
		var elem Todo
		err := cur.Decode(&elem)
		if err != nil {
			log.Fatal(err)
		}
		todos = append(todos, elem)
	}

	if err := cur.Err(); err != nil {
		log.Fatal(err)
	}

	cur.Close(context.TODO())
	fmt.Printf("Found multiple documents: %+v\n", todos)
	out, err := json.MarshalIndent(todos, "", "  ")
	if err != nil {
		http.Error(w, fmt.Sprintf("Unable to get todos: %s", err.Error()), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write(out)
}

func addTodo(w http.ResponseWriter, r *http.Request) {
	var todo Todo
	err := json.NewDecoder(r.Body).Decode(&todo)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	err = insert(todo)
	if err != nil {
		http.Error(w, fmt.Sprintf("Unable to add todo: %s", err.Error()), http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"status": "OK", "message": "Added TODO!"}`))
}

func insert(todo Todo) error {
	collection := db.Collection("todo")

	todo.CreatedAt = time.Now()
	fmt.Println(todo.Todo)

	insertResult, err := collection.InsertOne(context.TODO(), todo)
	if err != nil {
		return err
	}
	fmt.Println(insertResult.InsertedID)
	return nil
}
```

The to-do app is now in place, so you’re ready to start running the application in containers.

# Step 5 -- Running the Containers. Running the containers is a validation step to check on the previous configuration we have done.
Now that you have defined all of the services in your `docker-compose.yml` file and their configurations, you can start the containers.

Since the services are defined in a single file, you need to issue a single command to start the containers, create the volumes, and set up the networks. This command also builds the image for your Golang application. Run the following command to build the containers:

```sh
docker compose up -d
```

When running the command for the first time, it will download all of the necessary Docker images, which can take some time. Once the images are downloaded and stored in your local machine, docker-compose will create your containers. The `-d` flag daemonizes the process, which allows it to run as a background process.

Use the following command to list the running containers once the build process is complete:

```sh
docker ps
```

You will see output similar to the following:

```sh
Output
CONTAINER ID        IMAGE                           COMMAND                  CREATED             STATUS              PORTS                                      NAMES
9c53ea054917        digitalocean.com/golang:1.17.0  "./todo"                 2 weeks ago         Up 2 weeks          8080/tcp                                   todo
45a5a91fc0db        mongo:6.0.4                     "docker-entrypoint.s…"   2 weeks ago         Up 2 weeks          27017/tcp                                  mongodb
```

The CONTAINER ID is a unique identifier that is used to access containers. The IMAGE defines the image name for the given container. The NAMES field is the service name under which containers are created, similar to CONTAINER ID these can be used to access containers. Finally, the STATUS provides information regarding the state of the container whether it’s running, restarting, or stopped.

You’ve used the docker-compose command to build your containers from your configuration files. In the next step, you will create a MongoDB user for your application.

# Step 6 -- Creating a user for MongoDB. This step goes through creating a MongoDB for interacting with the database. 
By default, MongoDB allows users to log in without credentials and grants unlimited privileges. In this step, you will secure your MongoDB database by creating a dedicated user to access it.

To do this, you will need the root username and password that you set in the `docker-compose.yml` file environment variables `MONGO_INITDB_ROOT_USERNAME` and `MONGO_INITDB_ROOT_PASSWORD` for the mongodb service. In general, it’s better to avoid using the root administrative account when interacting with the database. Instead, you will create a dedicated database user for your Golang Todo application, as well as a new database that the Todo app will be allowed to access.

To create a new user, first start an interactive shell on the mongodb container:

```sh
docker exec -it mongodb bash
```

You use the `docker exec` command in order to run a command inside a running container along with the `-it` flag to run an interactive shell inside the container.

Once inside the container, log in to the MongoDB root administrative account:

```sh
mongosh -u mongodbuser -p
```

You will be prompted for the password that you entered as the value for the `MONGO_INITDB_ROOT_PASSWORD` variable in the `docker-compose.yml` file. The password can be changed by setting a new value for the `MONGO_INITDB_ROOT_PASSWORD` in the mongodb service, in which case you will have to re-run the docker-compose up `-d` command.

Run the `show dbs;` command to list all databases:

```sh
show dbs;
```

You will see the following output:

```sh
Output
admin    0.000GB
config   0.000GB
local    0.000GB
5 rows in set (0.00 sec)
```

The admin database is a special database that grants administrative permissions to users. If a user has read access to the admin database, they will have read and write permissions to all other databases. Since the output lists the admin database, the user has access to this database and can therefore read and write to all other databases.

Saving the first to-do note will automatically create the MongoDB database. MongoDB allows you to switch to a database that does not exist using the use database command. It creates a database when a document is saved to a collection. Therefore the database is not created here; that will happen when you save your first to-do note in the database from the API. Execute the use command to switch to the `todoapp` database:

```sh
use todoapp
```

Next, create a new user that will be allowed to access this database:

```sh
db.createUser({user: 'todouser', pwd: 'your password', roles: [{role: 'readWrite', db: 'todoapp'}]})
```

You will see a success message similar to the one given below:

```json
Successfully added user: {
        "user" : "todouser",
        "roles" : [
                {
                        "role" : "readWrite",
                        "db" : "todoapp"
                }
        ]
}
```

Now that you have added the user, log out of the database.

```sh
exit
```

This command creates a user named `todouser` with readWrite access to the `todo` database. Be sure to use a secure password in the pwd field. The user and pwd here are the values you defined in the `docker-compose.yml` file under the environment variables section for the Todo service.

Log in to the authenticated database with the following command:

```sh
mongosh -u todouser -p your password --authenticationDatabase todoapp
```

Now that you have added the user, log out of the database.

```sh
exit
```

And finally, exit the container:

```sh
exit
```

You’ve now configured a dedicated database and user account for your Todo application. The database components are ready, so now you can move on to running the Golang to-do app.

# Step 7 — Running the Golang To-do App
Now that your services are configured and running, you can test your application by navigating to `http://your_server_ip:port/todo` in a browser. Additionally, you can run curl to see the JSON response from Golang:

```sh
curl -i http://your_server_ip:port/todo/
```

You will receive the following response:

Output

```json
{"message": "Welcome to Golang TODO app!"}
```

The configuration for the Golang application is passed to the application from the `docker-compose.yml` file. The configuration regarding the database connection is set using the `MONGODB_*` variables defined in the environment section of the Todo service.

To test everything out, create a to-do note using the Golang API. You can do this with a `POST` curl request to the `/todo/create` route:

```sh
curl -i -H "Content-Type: application/json" -X POST -d '{"todo": "Dockerize Go application with MongoDB backend"}' http://your_server_ip:port/todo/create
```

This request results in a response with a status code of `201 CREATED` when the to-do item is saved to MongoDB:

Output

```json
{"status": "OK", "message": "Added TODO!"}
```

You can list all of the to-do notes from MongoDB with a GET request to the `/todo/list` route:

```sh
curl -i http://your_server_ip:port/todo/list
```

Output

```json
{"data":[{"id":"5c9fa25591cb7b000a180b60","todo":"Dockerize Golang application with MongoDB backend"}],"status":true}
```

With this, you have Dockerized a Golang API running a MongoDB backend deployed to your servers. For a production environment you can use sudo systemctl enable docker to ensure your Docker service automatically starts at runtime.

# Conclusion
In this tutorial, you deployed a Golang application with Docker and MongoDB. You now have a functioning modern stateless API application that can be scaled. Although you can achieve this result by using a command like `docker container run`, the `docker-compose.yml` simplifies your job as this stack can be put into version control and updated as necessary.