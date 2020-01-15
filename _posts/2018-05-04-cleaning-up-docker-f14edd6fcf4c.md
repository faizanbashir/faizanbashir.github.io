---
layout: post
current: post
cover:  assets/images/posts/1*C6BkVKRpoVK_Pq1TLqlSkQ1.png
navigation: True
title: "Cleaning Up Docker"
date: 2018-05-04 15:07:19
tags: [Docker, Containers]
class: post-template
subclass: 'post tag-getting-started'
author: faizan
---
With the passage of time running Docker in development, we tend to accumulate a lot of unused images. Sometimes for testing, research or just trying out fun new stuff. Its always cool to run new software in containers, lights up new possibilities for those of us interested in constantly learning new technologies. Downside is a lot of precious SSD memory occupied with rarely used or unused images, the worse thing is we hardly notice. But the guys at Docker Inc. have done a great task by keeping a track of all things Docker.

Say hello to the `system` command, part of the docker management commands and simply awesomeness. The `system` command provides info from disk usage to system-wide information, ain’t that cool.

***
### Disk usage using `df` command:

{% highlight shell %}
$ docker system df
{% endhighlight %}

Returns something like this,

{% highlight shell %}
TYPE              TOTAL     ACTIVE     SIZE         RECLAIMABLE
Images            35        6          8.332GB      7.364GB (88%)
Containers        12        12         417.6MB      0B (0%)
Local Volumes     67        2          2.828GB      2.828GB (100%)
Build Cache                            0B           0B
{% endhighlight %}

Notice the `Reclaimable` this is the size you can recover, it is calculated by subtracting the size of active images from the size of total images.

***
### Real time events using `events` command:

{% highlight shell %}
$ docker system events
{% endhighlight %}

Returns the list of real time events from the server, based on Docker object types.

Formatting output

{% highlight shell %}
$ docker system events --format 'Type={{.Type}}  Status={{.Status}}  ID={{.ID}}'
{% endhighlight %}

or simply format the output as JSON

{% highlight shell %}
$ docker system events --format '{{json .}}'
{% endhighlight %}

***
### System-wide info using `info` command:

Another cool command to get all the system related information is the info command. You will be amazed to see the amount of info you can get.

{% highlight shell %}
$ docker system info
{% endhighlight %}

***
### Remove unused data using `prune` command:

Now that we have all the info we need, its cleanup time, but beware against using this command half asleep.

{% highlight shell %}
$ docker system prune
WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all dangling images
        - all build cache
Are you sure you want to continue? [y/N]
{% endhighlight %}

Further we can remove exactly what we want, using any of the following commands, feast you eyes ladies and gents.

{% highlight shell %}
$ docker system prune -a --volumes
$ docker image prune
$ docker container prune
$ docker volume prune
$ docker network prune
{% endhighlight %}

All of the above commands will prompt for confirmation, so wash your face with cold water or take a shot of Espresso before issuing any of these ;).

*Originally published at [HackerNoon](https://hackernoon.com/cleaning-up-docker-f14edd6fcf4c)*