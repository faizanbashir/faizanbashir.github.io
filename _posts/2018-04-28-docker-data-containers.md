---
layout: post
title:  "Docker Data Containers"
excerpt: "There is more than one way to manage data in Docker container. Say hello to the Data Containers."
date:   2018-04-28 15:07:19
comments: true
image:
  feature: https://miro.medium.com/max/2784/1*AUiK5PwnsPG_xaT9jcVoSA.jpeg
  credit: thomas shellberg
  creditlink: https://unsplash.com/photos/Ki0dpxd3LGc
---
There is more than one way to manage data in Docker container. Say hello to the Data Containers.
Simply put data containers are containers whose job is just to store/manage data.

Similar to other containers they are managed by the host system. However, they don’t show up when you perform a `docker ps` command.

To create a Data Container we first create a container with a well-known name for future reference. We use *busybox* as the base as it’s small and lightweight in case we want to explore and move the container to another host.

When creating the container, we also provide a volume `-v` option to define where other containers will be reading/writing data.

{% highlight shell %}
$ docker create -v /config --name dataContainer busybox
{% endhighlight %}

With the container in place, we can now copy files from our local client directory into the container.

To copy files into a container you use the command `docker cp`. The following command will copy the *config.conf* file into the config directory of *dataContainer*.

{% highlight shell %}
$ docker cp config.conf dataContainer:/config/
{% endhighlight %}

Now our Data Container has our config, we can reference the container when we launch dependent containers requiring the configuration file.

Using the magical `--volumes-from <container>` option we can use the mount volumes from other containers inside the container being launched. In this case, we’ll launch an Ubuntu container which has reference to our Data Container. When we list the config directory, it will show the files from the attached container.

{% highlight shell %}
$ docker run --volumes-from dataContainer ubuntu ls/config
{% endhighlight %}

If a */config* directory already existed then, the volumes-from would override and be the directory used. You can map multiple volumes to a container.

---
# Import and Export Container data

Data can be imported and exported from a container, using the `docker export` command.

We can move the Data Container to another machine simply by exporting it to a .tar file.

{% highlight shell %}
$ docker export dataContainer > dataContainer.tar
{% endhighlight %}

Likewise we can import the Data Container back into Docker.

{% highlight shell %}
$ docker import dataContainer.tar
{% endhighlight %}

Check out the [Jekyll docs][jekyll] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll’s dedicated Help repository][jekyll-help].

[jekyll]:      http://jekyllrb.com
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-help]: https://github.com/jekyll/jekyll-help
