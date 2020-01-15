---
layout: post
current: post
cover:  assets/images/posts/1*lYvXrG9rcgLg42weUyOfyg1.jpeg
navigation: True
title: "Building Serverless Contact Form For Static Websites"
date: 2018-07-25 15:07:19
tags: [Serverless]
class: post-template
subclass: 'post tag-serverless'
author: faizan
---
### Introduction
A few years ago AWS launched static hosting service S3, which was a paradigm shift for hosting static websites. The tech was crystal clear, all the static assets (HTML, CSS, and JS) would reside in an S3 bucket to host your impressive website. A pretty cool idea I personally liked it, really. Had it not been for that super important contact form hosting on S3 would have been cool but your contact form would be a joke unless you had another server in place to service AJAX requests from that form. The moment you had that service ready, the S3 solution wouldn’t appear so attractive at all.

In the age of cutting edge technology, there’s always jaw-dropping innovations around the corner. One of the awesome tech innovation happens to be serverless. Not that there are no servers involved but you can care less about them now. Serverless can be a proper and viable solution to a lot of problems, it is the most perfect solution for your static hosted contact form. Keep reading by the end of this post you will be able to handle your website forms in the most inexpensive and simplest manner possible.

***

### The Serverless Framework

![Serverless Framework](assets/images/posts/1*oDBqXrshDx-kEVUg1e6Rhw.png)
Source: [https://serverless.com/](https://serverless.com/)

> Serverless is your toolkit for deploying and operating serverless architectures. Focus on your application, not your infrastructure.
— [Serverless.com](https://serverless.com)

The Swiss army knife of Serverless technologies. Serverless Framework is a free and open-source web framework written in Node.js. Serverless was the first framework to be developed for building applications exclusively on AWS Lambda, the serverless computing platform provided by Amazon Web Services. Currently, applications developed with Serverless Framework can be deployed to other FaaS service providers. Here is the list of the Serverless cloud services supported by the Serverless Framework:

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

#### Getting started with Serverless Framework
Obviously, you are pretty excited to get started with the Serverless Framework, let’s cut to the chase and start by installing Serverless.

Setting up Serverless is simple. You need to install it through npm and link it to your AWS account.

##### 1. Installing Serverless Globally
Time to get hands-on Serverless stuff.

{% highlight shell %}
$ npm install serverless -g
{% endhighlight %}

This command installs Serverless globally on your local machine. The Serverless commands are now available to you from your terminal.

**Note**: Running Linux, you may want to run the above command as sudo.

##### 2. Create an IAM user in the AWS Console
Go to your [AWS Console](https://console.aws.amazon.com/), you will find the [IAM service](https://console.aws.amazon.com/iam/home) listed below the “Security, Identity & Compliance” group. Inside the IAM dashboard click on the Users tab and click “Add User” button.
![AWS IAM Dashboard User Tab](assets/images/posts/1*VtA7fGzE2a_h6yMTl69lBw.png)

Create a new user and allow the user **programmatic access** by clicking on the Programmatic access checkbox. Next, in the permissions section, you need to add a set of permissions to the user. From the list of available options under the “Attach existing policies directly” check the **AdministratorAccess**.

![Attach Policy](assets/images/posts/1*d_6PWCnAeK25k7P7CaL1uA.png)

After the user is created, you will have access to the users **Access Key ID** and **Secret Access Key**. You will be required to use these keys in the next step.

![Access Keys](assets/images/posts/1*7FqyvVFoRxZClqC16SevXw.png)

**Word of Caution**: These are the kind of credentials you don’t want to lose even by mistake, remember you have provided **AdministratorAccess** to this user. The user with **AdministratorAccess** can do pretty much everything with your AWS account.

##### 3. Configuring Serverless to use IAM Credentials
Great! With the keys, you can set up Serverless Framework to access your AWS account. Switch to your terminal and use this command to configure Serverless:

{% highlight shell %}
$ sls config credentials --provider aws --key xxxxxxxxxxxxxx --secret xxxxxxxxxxxxxx --profile <username>
{% endhighlight %}

Now your Serverless installation knows what account AWS to connect.
Note: `sls` is an alias for the `serverless` command. You can use both to the same effect. But `sls` is kinda cool.

##### 4. Creating a service
With the Serverless Framework hooked up with your AWS account, you can set up a Serverless project in a jiffy. Fire up the terminal and issue the following command:

{% highlight shell %}
$ sls create --template aws-python --path <your-folder-path>
{% endhighlight %}

The `--template` flag is used to specify a preset template with the given settings. In the above command the template `aws-python` will set up the project configured to use AWS as the provider and Python as the runtime. The command will auto-generate `serverless.yml` , `handler.py` and `.gitignore` file with preset values.
The configuration is defined in the `serverless.yml` file. This file is the most important file in the Serverless Framework. It’s almost magical, given how it can spin up the infrastructure you have defined in it. The contents of the auto-generated `serverless.yml` file will look something like this:

{% highlight yaml %}
service: <your-service-name>
provider:
  name: aws
  runtime: python2.7
functions:
  hello:
    handler: handler.hello
{% endhighlight %}

The `provider` section defines everything related to the service provider, there are a lot more properties to configure it further you can take a look at them [here](https://serverless.com/framework/docs/providers/aws/guide/serverless.yml/). In the auto-generated `serverless.yml` file, you need to add two important tags under the `provider` section, which are as follows:

{% highlight yaml %}
region: <your-aws-region>
profile: <aws-username-with-programmatic-access>
{% endhighlight %}

The `functions` property is used to declare the serverless functions, you can declare multiple `functions` under this property. The above example declares a function called `hello` present in the `handler.py` file. Browse over to the handler.py file and you will find something like this:

{% highlight python %}
import json
def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed      successfully!",
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
{% endhighlight %}

***

#### The Serverless App
Our Serverless solution makes use of AWS infrastructure, it consists of API Gateway, Lambda Functions, DynamoDB and Simple Email Service(SES). To achieve this end result we will use the previously introduced Serverless Framework.

![Architecture of Serverless App](assets/images/posts/1*Be-VuMqQEg6Ifh60bFtDcQ.png)

- **Static Website** — Amazon S3 provides a robust and simple web server. All of the static HTML, CSS and JS files for your application can be served from S3. The contact form on our static website is submitted using AJAX.
- **API Gateway** — The API Gateway is the event source for the application, it acts as a bridge between our contact form and serverless lambda function. It routes the request from the contact form to the lambda function. The API Gateway also performs tasks such as access control, monitoring, API version control and traffic management.
- **AWS Lambda** — AWS Lambda is the place where the action takes place. Lambda functions run in stateless compute containers that are event-triggered, managed and ephemeral. In our example, we use a lambda function to send email using SES and store the request contents in DynamoDB NoSQL database.
- **Simple Email Service (SES)** — The cloud-based email sending service from Amazon. Scalable email service, you can send marketing and transactional emails using SES. In our example, we use SES to send emails using a verified email address.
- **DynamoDB** — DynamoDB provides a scalable, consistent, fully managed and non-relational database from Amazon. In our example, we use DynamoDB to store and retrieve the messages received from the static contact form.

You can find the source code for the demo application here. Go ahead and clone it!

[faizanbashir/python-ses-dynamodb-contactform](https://github.com/faizanbashir/python-ses-dynamodb-contactform)

***

#### Application Walkthrough
Let’s have a stroll through the demo application before we actually deploy it on AWS.

##### 1. Demystifying the serverless.yml file
The serverless.yml file defines the services the application needs to use and interact with. The resources and the actions the Serverless functions can perform are listed under the `iamRoleStatements` property. It lists the actions and resources.

{% highlight yaml %}
iamRoleStatements:
  - Effect: "Allow"
    Action:
      - ses:SendEmail
      - ses:SendRawEmail
    Resource: "*"
  - Effect: "Allow"
    Action:
      - dynamodb:Scan
      - dynamodb:PutItem
    Resource: "arn:aws:dynamodb:${opt:region, self:provider.region}:*:table/${self:provider.environment.DYNAMODB_TABLE}"
{% endhighlight %}

In the `serverless.yml` we are allowing the Serverless functions to use `ses:SendEmail` and `dynamoDB:PutItem` actions among many others defined above.

Since Lambda runs serverless functions in the cloud, we need to define the functions somewhere. Functions are defined using the `functions` property. In our example application we have defined events attached to them.

{% highlight yaml %}
functions:
  sendMail:
    handler: handler.sendMail
    description: Send Email using AWS SES Service
    events:
      - http:
          path: sendMail
          method: post
          integration: lambda
          cors: true
          response:
            headers:
              "Access-Control-Allow_Origin": "'*'"
  list:
    handler: handler.list
    description: List all the contact form submissions
    events:
      - http:
          path: list
          method: get
          integration: lambda
          cors: true
          response:
            headers:
              "Access-Control-Allow_Origin": "'*'"
{% endhighlight %}

Another great feature of Serverless Framework is that it will create an API in the AWS API Gateway and link it with relevant Lambda function. This is done using the `http` property defined in the `events` property.

##### 2. Creating Resources
With Serverless Framework you create resources like a DynamoDB table as we have done here. This snippet of code is responsible for creating a DynamoDB table with the given configuration.

{% highlight yaml %}
resources:
  Resources:
    ContactFormDynamoDbTable:
      Type: 'AWS::DynamoDB::Table'
      DeletionPolicy: Retain
      Properties:
        AttributeDefinitions:
          -
            AttributeName: id
            AttributeType: S
        KeySchema:
          -
            AttributeName: id
            KeyType: HASH
        ProvisionedThroughput:
          ReadCapacityUnits: 1
          WriteCapacityUnits: 1
        TableName: ${self:provider.environment.DYNAMODB_TABLE}
{% endhighlight %}

##### 3. Peek into the Serverless functions
The demo application is written in **python**, it uses [boto3](https://github.com/boto/boto3) AWS SDK to send emails using SES and for performing read/write operations on DynamoDB.

{% gist 98a726fa369754f337c65d5e30123d3a %}

The `sendMail` function is triggered when a `POST` request is received from the contact form on the `/sendMail` path. The list function is triggered by a `GET` request to `/list` path defined in the `serverless.yml` file.

***

#### Building the Application
Now that you have set up and configured the Serverless Framework in your machine, it’s time to get things rolling.

##### 1. Clone the application
Let’s start by cloning the application from Github.

{% highlight shell %}
$ git clone https://github.com/faizanbashir/python-ses-dynamodb-contactform
$ cd python-ses-dynamodb-contactform
{% endhighlight %}

##### 2. Verify e-mail address with SES
Fast-forward to verifying the email you intend to send email from SES. All you need to do is add an email address, AWS will send you a verification with a link to verify the email address.

![Verify a New Email Address](assets/images/posts/1*f_Y1mmdgKjtvxjBZL8zdIw.png)

After verifying the email address, the “Verification Status” for the email will show up as “verified”.

![Verification Status](assets/images/posts/1*IqxxKMYybvn0PlSPWgWgew.png)

##### 3. Configuring the application
You need to configure the `serverless.yml` with your account specific details to make it work. Replace the `region`, `profile` and `SENDER_EMAIL` properties in `serverless.yml` as seen here:

{% highlight yaml %}
provider:
  name: aws
  runtime: python2.7
  region: <aws-region>
  profile: <aws-user>
  ...
environment:
  SENDER_EMAIL: <verified-email-address>
{% endhighlight %}

Awesome! with the configuration done you can turn your attention to deploying the application.

##### 4. Deploying to AWS
Everything in place now you can deploy application with a single command, ain’t that super cool.

{% highlight shell %}
$ sls deploy -v
{% endhighlight %}

It will take a minute or two to execute if you religiously followed this tutorial, at the end it will provide you a list of endpoints to use for calling our functions. It will look something like this:

{% highlight shell %}
endpoints:
POST - https://xxx.execute-api.xx.amazonaws.com/development/sendMail
GET - https://xxxx.execute-api.xx.amazonaws.com/development/list
{% endhighlight %}

##### 5. Testing the endpoints
Now that we have the endpoints let’s test application to see if it’s working or not. The `/sendMail` endpoint expects input in JSON format.

{% highlight shell %}
$ curl --header "Content-Type: application/json" \
--request POST \
--data '{"firstname": "John", "lastname": "Doe", "email": "john@doe.com", "message": "Hi there"}'\
https://xxx.execute-api.xx.amazonaws.com/development/sendMail
{% endhighlight %}

If the email is sent and the entry written to DynamoDB the request will exit with a response like this.

{% highlight shell %}
> "Email Sent!"
{% endhighlight %}

Now, let’s test the `/list` endpoint in the same manner with the `GET` endpoint you got after deploying the application.

{% highlight shell %}
$ curl https://xxxx.execute-api.xx.amazonaws.com/development/list
{% endhighlight %}

The `/list` endpoint response will look something like this:

{% highlight shell %}
> {"body": [{"firstname": "John", "lastname": "Doe", "email": "john@doe.com", "updatedAt": 1529425349731, "message": "Hi there", "id": "f651c404-73dc-11e8-bf3e-be54be0b5d22", "createdAt": 1529425349731}], "statusCode": 200}
{% endhighlight %}

##### 6. The Contact Form
With the Serverless functions working properly we can go ahead and integrate it into our static contact form. The static form code is in the `public` folder.

Open the `index.html` file in your favourite IDE and update the `URL` variable with the `/sendMail` endpoint and you are good to go.

{% highlight shell %}
//Insert your lambda function URL here

var URL = "https://xxx.execute-api.xx.amazonaws.com/development/sendMail";
{% endhighlight %}

Navigate to the page using the `file:///<path>/<to>/<folder>/index.html` in the browser or upload it to S3 bucket and enable static hosting.

{% highlight shell %}
$ aws s3 sync public s3://your-bucket-name
{% endhighlight %}

![Serverless Contact Form](assets/images/posts/1*G6Q3XRI6tADC38nbcJohkQ.png)

Treat yourself with a Cappuccino, Latte or <insert-your-favorite-drink>. You just implemented a cool way to keep your website on static hosting with handling your forms, thanks to Serverless.

***

### Afterthoughts
Serverless is definitely the way forward, not just for the worlds static contact forms. Serverless has opened a universe of opportunities for you, the contact form was just to get started with. How about using Serverless for your website analytics, a visitor counter or maybe click tracking?
Endless opportunities are waiting for you. Get started for your next project in Serverless, it’ll be an awesome journey.

*Originally published at [www.serverlessops.io.](https://www.serverlessops.io/blog/serverless-contact-form-for-static-websites)*