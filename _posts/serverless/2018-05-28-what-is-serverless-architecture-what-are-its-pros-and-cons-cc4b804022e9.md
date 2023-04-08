---
layout: post
comments: true
current: post
cover:  assets/images/posts/1*16x1_xEclXT4MB0FN_xr2g.webp
navigation: True
title: "What is Serverless Architecture? What are its Pros and Cons?"
date: 2018-05-13 15:07:19
tags: [Serverless]
class: post-template
subclass: 'post tag-serverless'
author: faizan
---
Serverless, the new buzzword in town has been gaining a lot of attention from the pros and the rookies in the tech industry. Partly due to the manner in which cloud vendors like AWS have hyped the architecture, from conferences to meetups to blog posts to almost everywhere. But serverless is not just about the hype, it promises the possibility of ideal business implementations which sounds quite pleasant to the ears and probably light on the budget as well.

> “Focus on your application, not the infrastructure”

Sounds relieving though, knowing a lot of your daylight hours go into implementing, maintaining, debugging, and monitoring the infrastructure. With all of that infrastructure heavy lifting out of the way, we really can focus on the business goals our applications serve. A lot of productive efforts could be channeled in the right direction, where they were meant to be ideally. Maybe it sounds too good to be true, but this is the way things should have been. At least for those of you who cant afford to spend a lot of time caught up in the web of intricacies in modern complex infrastructure.

Expectations apart, Serverless is really breaking ground in its path to disrupt your server infrastructure. Serverless is already used in production by companies like Netflix, Reuters, AOL, and Telenor. Industry-wide adoption is constantly increasing. Serverless is all set to take up its own place, but don’t expect Serverless to conquer your infrastructure completely. There will be use cases where serverless might prove to be the wrong choice.

***

### So, What is Serverless?

Serverless is a cloud computing execution model where the cloud provider dynamically manages the allocation and provisioning of servers. A serverless application runs in stateless compute containers that are event-triggered, ephemeral (may last for one invocation), and fully managed by the cloud provider. Pricing is based on the number of executions rather than pre-purchased compute capacity, isn’t it the ideal framework for that project you have been planning since a long time? Well, go ahead do it.

>Serverless applications are event-driven cloud-based systems where application development rely solely on a combination of third-party services, client-side logic and cloud-hosted remote procedure calls (Functions as a Service).

Most of the cloud providers have invested heavily in serverless and thats a lot of money; with the given massive promotion and realistic offering you can safely assume serverless to be one of the most used cloud services in upcoming years. Here are some of the currently available cloud services:

![Cloud Providers](assets/images/posts/1*t4O4UXpdG68MQboNKC6bBw.jpeg)
Source: [https://www.slideshare.net/loige/building-a-serverless-company-with-nodejs-react-and-the-serverless-framework-jsday-2017-verona](https://www.slideshare.net/loige/building-a-serverless-company-with-nodejs-react-and-the-serverless-framework-jsday-2017-verona)

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Google Cloud Functions](https://cloud.google.com/functions/)
- [Azure Functions](https://azure.microsoft.com/en-us/services/functions/)
- [IBM OpenWhisk](https://www.ibm.com/cloud-computing/bluemix/openwhisk)
- [Alibaba Function Compute](https://www.alibabacloud.com/product/function-compute)
- [Iron Functions](http://open.iron.io/)
- [Auth0 Webtask](https://webtask.io/)
- [Oracle Fn Project](https://fnproject.io/)
- [Spotinst](https://spotinst.com/) 
- [Kubeless](https://kubeless.io/)

***

### Traditional vs. Serverless Architecture

![Traditional vs Serverless](assets/images/posts/1*x_v5NRC3TTMt1MaYl1gMUg.jpeg)
Source: [https://www.gocd.org/2017/06/26/serverless-architecture-continuous-delivery/](https://www.gocd.org/2017/06/26/serverless-architecture-continuous-delivery/)

For years your applications have run on servers which you had to patch, update, and continuously look after late nights and early mornings due to all the unimaginable errors that broke your production. As long as you managed them, the whole responsibility of their proper functioning was on you. Serverless tends to be unlike the aforementioned, you no longer need to worry about the underlying servers. Reason being, they are not managed by you anymore and with management out of the picture the responsibility falls on the Cloud vendors. But regardless the cool features of Serverless in some cases, the traditional architecture outshines it.

#### Pricing
One of the major advantages of using Serverless is reduced cost, for years the cost of provisioning servers and maintaining that 24x7 server team which blew a hole in your pocket is gone. The cost model of Serverless is execution-based: you’re charged for the number of executions. You’re allotted a certain number of seconds of use that varies with the amount of memory you require. Likewise, the price per MS (millisecond) varies with the amount of memory you require. Obviously, shorter running functions are more adaptable to this model with a peak execution time of 300-second to 15-minutes for most Cloud vendors.

*The winner here is Serverless Architecture.*

#### Networking
The downside is that Serverless functions are accessed only as private APIs. To access these you must set up an API Gateway. This doesn’t have an impact on your pricing or process, but it means you cannot directly access them through the usual IP, snap!

*The winner here is Traditional Architecture.*

#### 3rd Party Dependencies
Most, if not all of your projects have external dependencies, they rely on libraries that are not built into the language or framework you use. You often use libraries with functionality that includes cryptography, image processing, etc., these libraries can be pretty heavy. Without system-level access, you must package these dependencies into the application itself.

>Reinventing the wheel isn’t always a good idea.

*The winner here is based on the context. For simple applications with few dependencies, Serverless is the winner; for anything more complex, Traditional Architecture is the winner.*

#### Environments
Setting up different environments for Serverless is as easy as setting up a single environment. Given that it’s pay per execution, this is a large improvement over traditional servers, you no longer need to set up dev, staging, and production machines. Eventually you’d lose count of all the environments, at some point.

*The winner here is Serverless Architecture.*

#### Timeout
With Serverless computing, there’s a [hard 15-minute timeout limit for AWS Lambda](https://aws.amazon.com/about-aws/whats-new/2018/10/aws-lambda-supports-functions-that-can-run-up-to-15-minutes/). Too complex or long-running functions aren’t good for Serverless, but having a hard timeout makes it impossible to perform certain tasks. A hard limit on this time makes Serverless unusable for applications that have variable execution times, and for certain services which require information from an external source. This is likely to change in the future.

*The clear winner here is Traditional Architecture.*

#### Scale
Scaling process for Serverless is automatic and seamless, but there is a lack of control or entire absence of control. While automatic scaling is great, it’s difficult not to be able to address and mitigate errors related to new Serverless instances.

*It’s a tie between Serverless and Traditional Architecture.*

***

### Functions as a Service (FaaS)
FaaS is an implementation of Serverless architectures where engineers can deploy an individual function or a piece of business logic. They start within milliseconds (~100ms for AWS Lambda) and process individual requests within a 300-second to 15-minute timeout imposed by most cloud vendors.

#### Principles of FaaS:
- Complete management of servers
- Invocation based billing
- Event-driven and instantaneously scalable

#### Key properties of FaaS:
##### Independent, server-side, logical functions
FaaS are similar to the functions you’re used to writing in programming languages, small, separate, units of logic that take input arguments, operate on the input and return the result.

##### Stateless
With Serverless, everything is stateless, you can’t save a file to disk on one execution of your function and expect it to be there at the next. Any two invocations of the same function could run on completely different containers under the hood.

##### Ephemeral
FaaS are designed to spin up quickly, do their work and then shut down again. They do not linger unused. As long as the task is performed the underlying containers are scrapped.

##### Event-triggered
Although functions can be invoked directly, yet they are usually triggered by events from other cloud services such as HTTP requests, new database entries or inbound message notifications. FaaS are often used and thought of as the glue between services in a cloud environment.

##### Scalable by default
With stateless functions multiple containers can be initialised, allowing as many functions to be run (in parallel, if necessary) as needed to continually service all incoming requests.

##### Fully managed by a Cloud vendor
AWS Lambda, Azure Functions, IBM OpenWhisk and Google Cloud Functions are most well-known FaaS solutions available. Each offering typically supports a range of languages and runtimes e.g. Node.js, Python, .NET Core, Java.

***

### The Serverless App
A Serverless solution consists of a web server, Lambda functions (FaaS), security token service (STS), user authentication and database.

![Serverless App](assets/images/posts/1*TIrjN7EjLUVJmJ6YvHR7Dg.png)
Source: [http://blog.tonyfendall.com/2015/12/serverless-architectures-using-aws-lambda/](http://blog.tonyfendall.com/2015/12/serverless-architectures-using-aws-lambda/)

- **Client Application** — The UI of your application is rendered client side in Modern Frontend Javascript App which allows us to use a simple, static web server.
- **Web Server** — Amazon S3 provides a robust and simple web server. All of the static HTML, CSS and JS files for our application can be served from S3.
- **Lambda functions (FaaS)** — They are the key enablers in Serverless architecture. Some popular examples of FaaS are AWS Lambda, Google Cloud Functions and Microsoft Azure Functions. AWS Lambda is used in this framework. The application services for logging in and accessing data will be built as Lambda functions. These functions will read and write from your database and provide JSON responses.
- **Security Token Service (STS)** — generates temporary AWS credentials (API key and secret key) for users of the application. These temporary credentials are used by the client application to invoke the AWS API (and thus invoke Lambda).
- **User Authentication** — AWS Cognito is an identity service which is integrated with AWS Lambda. With Amazon Cognito, you can easily add user sign-up and sign-in to your mobile and web apps. It also has the options to authenticate users through social identity providers such as Facebook, Twitter or Amazon, with SAML identity solutions, or using your own identity system.
- **Database** — AWS DynamoDB provides a fully managed NoSQL database. DynamoDB is not essential for a serverless application but is used as an example here.

***

### Benefits of Serverless Architecture

#### From business perspective
1. The cost incurred by a serverless application is based on the number of function executions, measured in milliseconds instead of hours.
2. Process agility: Smaller deployable units result in faster delivery of features to the market, increasing the ability to adapt to change.
3. Cost of hiring backend infrastructure engineers goes down.
4. Reduced operational costs

#### From developer perspective
1. Reduced liability, no backend infrastructure to be responsible for.
2. Zero system administration.
3. Easier operational management.
4. Fosters adoption of Nanoservices, Microservices, SOA Principles.
5. Faster set up.
6. Scalable, no need to worry about the number of concurrent requests.
7. Monitoring out of the box.
8. Fosters innovation.

#### From user perspective
1. If businesses are using that competitive edge to ship features faster, then customers are receiving new features quicker than before.
2. It is possible that users can more easily provide their own storage backend(i.e Dropbox, Google Drive).
3. It’s more likely that these kinds of apps may offer client-side caching, which provides a better offline experience.

***

### Drawbacks of Serverless Architecture

#### From business perspective
1. Reduced overall control.
2. Vendor lock-in requires more trust for a third-party provider.
3. Additional exposure to risk requires more trust for a third party provider.
4. Security risk.
5. Disaster recovery risk
6. Cost is unpredictable because the number of executions is not predefined
7. All of these drawbacks can be mitigated with open-source alternatives but at the expense of cost benefits mentioned previously

#### From developer perspective
1. Immature technology results in component fragmentation, unclear best-practices.
2. Architectural complexity.
3. The discipline required against function sprawl.
4. Multi-tenancy means it’s technically possible that neighbour functions could hog the system resources behind the scenes.
5. Testing locally becomes tricky.
6. Significant restrictions on the local state.
7. Execution duration is capped.
8. Lack of operational tools

#### From user perspective
1. Unless architected correctly, an app could provide a poor user experience as a result of increased request latency.

***

![Serverless Framework](assets/images/posts/1*oDBqXrshDx-kEVUg1e6Rhw.png)
Source: [https://serverless.com/](https://serverless.com)

Serverless platforms need infrastructures where they can be executed, provider agnostic frameworks provide a platform agnostic way to define and deploy Serverless code on various cloud platforms or commercial services.

- [Serverless Framework](https://serverless.com/) (Javascript, Python, Golang)
- [Apex](https://apex.run/) (Javascript)
- [ClaudiaJS](https://claudiajs.com) (Javascript)
- [Sparta](https://gosparta.io) (Golang)
- [Gordon](https://github.com/jorgebastida/gordon) (Javascript)
- [Zappa](https://www.zappa.io/) (Python)
- [Up](https://github.com/apex/up) (Javascript, Python, Golang, Crystal)

***

### Summary
Serverless architecture is certainly very exciting, but it comes with a bunch of limitations. As the validity and success of architectures depend on the business requirements and by no means solely on technology. In the same way, Serverless can shine when used in proper place.

Take a look at the awesomeness that is Serverless, it's time to take a peek at what Serverless looks from the inside. Here are few links to get you started on your Serverless journey.

[Serverless/examples](https://github.com/serverless/examples)

[anaibol/awesome-serverless](https://github.com/anaibol/awesome-serverless)

[Building Serverless Contact Form For Static Websites](https://hackernoon.com/building-serverless-contact-form-for-static-websites-b0e622d5a035)

I hope this article helped in the understanding of Serverless Computing. I’d love to hear about how you use Serverless in your projects. Share the knowledge, help it reach more people.

*Originally published at [HackerNoon](https://hackernoon.com/what-is-serverless-architecture-what-are-its-pros-and-cons-cc4b804022e9)*