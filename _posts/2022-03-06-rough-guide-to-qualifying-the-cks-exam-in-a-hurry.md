---
layout: post
comments: true
current: post
cover:  assets/images/posts/cks.jpg
navigation: True
title: "Rough Guide to qualifying the CKS exam in a hurry!"
date: 2022-03-06 10:00:00
tags: [Kubernetes]
class: post-template
subclass: 'post tag-kubernetes'
author: faizan
excerpt: This article is based upon my experience on how I approached the CKS exam and cleared it in my first attempt in Sep 2021.
---
This article is based upon my experience on how I approached the CKS exam and cleared it in my first attempt in Sep 2021.

I cleared the CKAD exam back in Feb 2020 followed by CKA in March 2020, the CKS exam was released somewhere around November  2020 but I couldn't get a chance to take the exam before Sep 2021 although I had enrolled for it in Dec 2020. Having said that I have been working with Kubernetes for the past 3 years almost on a day-to-day basis and that experience was an added advantage.

Kubernetes is the most evolved and feature-rich Container Orchestration system to date and it keeps getting better. It has an enormous community to support, building new features and resolving issues, Kubernetes is certainly evolving at a breakneck pace and it becomes a challenge to keep up with its pace of development. This makes it the best bet for a container orchestration solution.

***
## Table of Contents:

* [Resources for the Exam](#resourcesfortheexam)
* [Aliases](aliases)
    * [vi defaults for ~/.vimrc](videfaultsforvimrc)
    * [kubectl defaults for ~/.bashrc](kubectldefaultsforbashrc)
* [Shortcuts](shortcuts)
* [Cheat Sheet](cheatsheet)
    * [kubectl run command](kubectlruncommand)
    * [Generating yaml spec from an existing Pod](generatingyamlspecfromanexistingpod)
    * [kubectl pod commands](kubectlpodcommands)
    * [Printing logs and exporting](printinglogsandexporting)
    * [Creating configmaps and secrets](creatingconfigmapsandsecrets)
    * [Few commands which can be helpful for debugging](fewcommandswhichcanbehelpfulfordebugging)
    * [Rolling updates and Rollouts](rollingupdatesandrollouts)
    * [Scale and Autoscale command](scaleandautoscalecommand)
    * [Network Policy](networkpolicy)
    * [Static Analysis using Kubesec](staticanalysisusingtrivvy)
    * [Vulnerability scanning using Trivvy](vulnerabilityscanningusingtrivvy)
    * [Remove Unwanted Services](removeunwantedsevices)
    * [Runtime Classes](runtimeclasses)
    * [RBAC Commands](rbaccommands)
    * [Cluster Maintenance](clustermaintenance)
* [Exam Tips](examtips)
    * [JSON and JSONPath](jsonandjsonpath)
* [CKS Exam Topics](cksexamtopics)
    * [Securing and Hardening Container Images](securingandhardeningcontainerimages)
    * [Minimising OS Footprint](minimisingosfootprint)
        * [Conatiner Layers](conatinerlayers)
        * [Multi Stage Builds](multistagebuilds)
    * [Limit Node Access](limitnodeaccess)
    * [SSH Hardening](sshhardening)
        * [Disable SSH](disablessh)
        * [Remove Obsolete Packages and Services](removeobsoletepackagesandservices)
        * [Restrict Kernel Modules](restrictkernelmodules)
        * [Identify and Disable Open Ports](identifyanddisableopenports)
    * [Restrict Network Access](restrictnetworkaccess)
        * [Identity a service running on port](identityaservicerunningonport)
        * [UFW Firewall](ufwfirewall)
    * [Linux Syscalls](linuxsyscalls)
        * [Trace Syscalls](tracesyscalls)
    * [AquaSec Tracee](aquasectracee)
    * [Restricting Syscalls with Seccomp](restrictingsyscallswithseccomp)
        * [Seccomp in Kubernetes](seccompinkubernetes)
    * [AppArmor](apparmor)
        * [AppArmor in Kubernetes](apparmorinkubernetes)
    * [Linux Capabilities](linuxcapabilities)
* [Preparation for the Exam](preparationfortheexam)
* [Practice, Practice and Practice!](practicepracticeandpractice)
***

### Resources for the Exam

The following are a few awesome resources available on passing the CKS exam:
1. [Certified Kubernetes Security Specialist by Killer.sh](https://www.udemy.com/course/certified-kubernetes-security-specialist/) 
2. [Certified Kubernetes Security Specialist (CKS) by KodeKloud](https://kodekloud.com/courses/certified-kubernetes-security-specialist-cks/)
3. [Walid Shaari has gathered some indispensable materials for the CKS exam](https://github.com/walidshaari/Certified-Kubernetes-Security-Specialist)
4. [Abdennour's References for CKS Exam Objectives](https://github.com/abdennour/certified-kubernetes-security-specialist)
5. [Ibrahim Jelliti's collection of resources to prepare for the Certified Kubernetes Security Specialist (CKSS) exam](https://github.com/ibrahimjelliti/CKSS-Certified-Kubernetes-Security-Specialist)

The courses for KodeKloud and Killer.sh provide mock exam simulators which are very helpful in preparing for the exam and provide a pretty good idea of what the exam looks like. I strongly suggest enrolling in one or both courses. Linux Foundation also provides you with 2 attempts to exam simulator from killer.sh that way if you are well versed with the contents of the curriculum you can skip the courses and directly go for the exam simulator provided with the exam.

The exam costs $375 but there are offers and deals available if you look for them you might be able to get a better price. The duration of the exam is 2 hours and is valid for 2 years, unlike the CKA and CKAD which are valid for 3 years.

### Aliases

The CKS is a performance-based exam where you are provided with an exam simulator in which you have to work out the problems. You are allowed to open only one tab apart from the exam tab. Since this exam requires you to write a lot of commands thus I figured early on that I'd have to rely on aliases to reduce the number of keystrokes to save time.

I used the **vi** editor during the exam, here I will share some useful tips for this editor.

#### vi defaults for ~/.vimrc:

```
vi ~/.vimrc
---
:set number
:set et
:set sw=2 ts=2 sts=2
---
^: Start of word in line
0: Start of line
$: End of line
w: End of word
GG: End of file
```

#### kubectl defaults for ~/.bashrc:

```
vi ~/.bashrc
---
alias k='kubectl'
alias kg='k get'
alias kd='k describe'
alias kl='k logs'
alias ke='k explain'
alias kr='k replace'
alias kc='k create'
alias kgp='k get po'
alias kgn='k get no'
alias kge='k get ev'
alias kex='k exec -it'
alias kgc='k config get-contexts'
alias ksn='k config set-context --current --namespace'
alias kuc='k config use-context'
alias krun='k run'
export do='--dry-run=client -oyaml'
export force='--grace-period=0 --force'

source <(kubectl completion bash)
source <(kubectl completion bash | sed 's/kubectl/k/g' )
complete -F __start_kubectl k


alias krp='k run test --image=busybox --restart=Never'
alias kuc='k config use-context'
---
```

### Shortcuts:

The `kubectl get` command provides short catchy names for accessing resources and like `pvc` for `persistentstorageclaim`, these can help save a lot of keystrokes and valuable time during the exam.

* **po** for `pods`
* **rs** for `replicasets`
* **deploy** for `deployments`
* **svc** for `services`
* **ns** for `namespace`
* **netpol** for `networkpolicy`
* **pv** for `persistentstorage`
* **pvc** for `persistentstorageclaim`
* **sa** for `serviceaccounts`

### Cheat Sheet

#### kubectl run command

The `kubectl run` command provides a flag `--restart` which allows for the creation of different kinds of Kubernetes objects from a Deployment to CronJob. The below snippet shows the different options available for the `--restart` flag.

```
k run:
--restart=Always                             #Creates a deployment
--restart=Never                              #Creates a Pod
--restart=OnFailure                          #Creates a Job
--restart=OnFailure --schedule="*/1 * * * *" #Creates a CronJob
```

#### Generating yaml spec from an existing Pod

Sometimes it is easier to generate a spec from an existing Pod and make changes to it than create a new one from scratch. The `kubectl get pod` command provides us with the required flags to output the pod spec in the format we want.

```
kgp <pod-name> -o wide

# Generating YAML Pod spec
kgp <pod-name> -o yaml
kgp <pod-name> -o yaml > <pod-name>.yaml

# Get a pod's YAML spec without cluster specific information
kgp my-pod -o yaml --export > <pod-name>.yaml
```

#### kubectl pod commands

The `kubectl run` command provides a lot of options like specifying requests and limits a Pod is supposed to use or the commands a container should run once created.

```
# Output YAML for a nginx pod running a echo command
krun nginx --image=nginx --restart=Never --dry-run -o yaml -- /bin/sh -c 'echo Hello World!'
# Output YAML for a busybox pod running a sleep command
krun busybox --image=busybox:1.28 --restart=Never --dry-run -o yaml -- /bin/sh -c 'while true; do echo sleep; sleep 10; done'
# Run a pod with set requests and limits
krun nginx --image=nginx --restart=Never --requests='cpu=100m,memory=512Mi' --limits='cpu=300m,memory=1Gi'
# Delete Pod without delay
k delete po busybox --grace-period=0 --force
```

#### Printing logs and exporting

Logs are the fundamental source of information when it comes to debugging an application. The `kubectl logs` command provides the functionality to check the logs of a given Pod. The below commands can be used to check the logs of a given Pod.
```
kubectl logs deploy/<podname>
kubectl logs deployment/<podname>
#Follow logs
kubectl logs deploy/<podname> --tail 1 --follow
```

Apart from just looking at logs, we can also export logs to a file for further debugging of sharing the same with anyone.
```
kubectl logs <podname> --namespace <ns> > /path/to/file.format
```

#### Creating config maps and secrets

The `kubectl create` command provides us with the capability to create ConfigMaps and Secrets from the command line, we can also use the YAML file to create the same resources and by using `kubectl apply -f <filename>` we can apply the commands.
```
kc cm my-cm --from-literal=APP_ENV=dev
kc cm my-cm --from-file=test.txt
kc cm my-cm --from-env-file=config.env

kc secret generic my-secret --from-literal=APP_SECRET=sdcdcsdcsdcsdc
kc secret generic my-secret --from-file=secret.txt
kc secret generic my-secret --from-env-file=secret.env
```

#### Few commands which can be helpful for debugging

Debugging is a very important skill while facing issues and errors both in our day jobs while solving problems in the CKS exam. Apart from the ability to output logs from a container the `kubectl exec` commands allow us to log in to a running container and debug issues. While inside the container we can also use utilities like `nc` and `nslookup` to diagnose networking-related issues.
```
# Run busybox container
k run busybox --image=busybox:1.28 --rm --restart=Never -it sh
# Connect to a specific container in a Pod
k exec -it busybox -c busybox2 -- /bin/sh
# adding limits and requests in command
kubectl run nginx --image=nginx --restart=Never --requests='cpu=100m,memory=256Mi' --limits='cpu=200m,memory=512Mi'
# Create a Pod with a service
kubectl run nginx --image=nginx --restart=Never --port=80 --expose
# Check port
nc -z -v -w 2 <service-name> <port-name>
# NSLookup
nslookup <service-name>
nslookup 10-32-0-10.default.pod
```

#### Rolling updates and Rollouts

The `kubectl rollout` command provides the ability to check for the status of updates and if required roll back to a previous version.
```
k set image deploy/nginx nginx=nginx:1.17.0 --record
k rollout status deploy/nginx
k rollout history deploy/nginx
# Rollback to previous version
k rollout undo deploy/nginx
# Rollback to revision number
k rollout undo deploy/nginx --to-revision=2
k rollout pause deploy/nginx
k rollout resume deploy/nginx
k rollout restart deploy/nginx
kubectl run nginx-deploy --image=nginx:1.16 --replias=1 --record
```

#### Scale and Autoscale command

The `kubectl scale` command provides the functionality to scale up or scale down Pods in a given deployment. Using the `kubectl autoscale` command we can define the minimum number of Pods that should be running for a given deployment and the maximum numbers of Pods the deployment can scale to along with the scaling criteria like CPU percentage.
```
k scale deploy/nginx --replicas=6
k autoscale deploy/nginx --min=3 --max=9 --cpu-percent=80
```

#### Network Policy

In a Kubernetes cluster, all Pods can communicate with all Pods by default, which can be a security issue in some implementations. To circumvent this issue Kubernetes introduced Network Policies to allow or deny traffic to and from Pods based on Pod labels which are part of the Pod spec.

The below example denies both the Ingress and Egress traffic for Pods running in all namespaces. 
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: example
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  - Ingress
```

The below example denies both the Ingress and Egress traffic for Pods running in all namespaces. But allows access to DNS resolution services running on port 53.
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  - Ingress
  egress:
  - to:
    ports:
      - port: 53
        protocol: TCP
      - port: 53
        protocol: UDP
```

The below example denies Egress access to the metadata server running on IP address `169.256.169.256` in AWS EC2 Instances.
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name:cloud-metadata-deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
      - ipBlock: 
          cidr: 0.0.0.0/0
          except:
          - 169.256.169.256/32
```

The below example allows Egress access to the metadata server running on IP address `169.256.169.256` in AWS EC2 Instances.
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: cloud-metadata-accessor
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: metadata-accessor
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 169.256.169.256/32
```

#### Static Analysis using Kubesec

Kubesec is a Static Analysis tool for analyzing the YAML files to find issues with the files.
```
kubesec scan pod.yaml

# Using online kubesec API
curl -sSX POST --data-binary @pod.yaml https://v2.kubesec.io/scan

# Running the API locally
kubesec http 8080 &

kubesec scan pod.yaml -o pod_report.json -o json
```

#### Vulnerability scanning using Trivvy

Trivvy is a Vulnerability Scanning tool that scans container images for security issues.
```
trivy image nginx:1.18.0
trivy image --severity CRITICAL nginx:1.18.0
trivy image --severity CRITICAL, HIGH nginx:1.18.0
trivy image --ignore-unfixed nginx:1.18.0

# Scanning image tarball
docker save nginx:1.18.0 > nginx.tar
trivy image --input archive.tar

# Scan and output results to file
trivy image --output python_alpine.txt python:3.10.0a4-alpine
trivy image --severity HIGH --output /root/python.txt python:3.10.0a4-alpine

# Scan image tarball
trivy image --input alpine.tar --format json --output /root/alpine.json
```

#### Remove Unwanted Services

The `systemctl` exposes the capabilities to start, stop, enable, disable and list services running on a Linux Virtual Machine.

List services:
```
systemctl list-units --type service
```
Stop Service:
```
systemctl stop apache2
```
Disable Service:
```
systemctl disable apache2
```
Remove Service:
```
apt remove apache2
```

#### Runtime Classes

Kubernetes introduced the RuntimeClass feature in version `v1.12` for selecting the container runtime configuration. The container runtime configuration is used to run a Pod's underlying containers. Most Kubernetes clusters use the `dockershim` as the Runtime class for the running containers but different container Runtimes can be used. The `dockershim` has been deprecated in Kubernetes version `v1.20`, and will be removed in `v1.24`.

Creating a Runtime Class:
```
apiversion: node.k8s.io/v1beta1
kind: RuntimeClass
metadata:
  name: gvisor
handler: runsc
```
Use a runtime class for any given Pod:
```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx
  name: nginx
spec:
  runtimeClassName: gvisor
  containers:
  - name: nginx
    image: nginx 
```

#### RBAC Commands

In Kubernetes, Role-based access control (RBAC) commands provide a method of regulating access to Kubernetes resources based on the roles of individual users or service accounts.

Create a role
```
kubectl create role developer --resource=pods --verb=create,list,get,update,delete --namespace=development
```

Create a role binding
```
kubectl create rolebinding developer-role-binding --role=developer --user=faizan --namespace=development
```

Validate
```
kubectl auth can-i update pods --namespace=development --as=faizan
```

Create a cluster role
```
kubectl create clusterrole pvviewer-role --resource=persistentvolumes --verb=list
```

Create a Clusterrole Binding association with a service account
```
kubectl create clusterrolebinding pvviewer-role-binding --clusterrole=pvviewer-role --serviceaccount=default:pvviewer
```

#### Cluster Maintenance

The `kubectl drain` command is used to remove all running workloads(Pods) from a given Node. The `kubectl cordon` command is used to cordon a node to mark it as schedulable. The `kubectl uncordon` command is used to set the node as schedulable meaning the Controller Manager can schedule new Pods to the given node.

Draining a node of all pods
```
kubectl drain node-1
```
Drain a node and ignore daemonsets
```
kubectl drain node01 --ignore-daemonsets
```
Force Drain:
```
kubectl drain node02 --ignore-daemonsets --force
```
Mark a node un schedulable, no new pods can be scheduled on this node:
```
kubectl cordon node-1
```
Mark a node schedulable
```
kubectl uncordon node-1
```

### Exam Tips

The Kubernetes `kubectl get` command provides the user with an output flag the `-o` or `--output` which helps us in formatting the output in the form of json, yaml, wide or custom-columns.

#### JSON and JSONPath

Outputs the contents of all the pods in the form of a JSON Object:
```
kubectl get pods -o json
```
The JSONPath outputs a specific key from the JSON Object:
```
kubectl get pods -o=jsonpath='{@}'
kubectl get pods -o=jsonpath='{.items[0]}'
```
The `.items[*]` is used where we have multiple objects for instance multiple containers with a Pod config:
```
# For list of items use .items[*]
k get pods -o 'jsonpath={.items[*].metadata.labels.version}'
# For single item
k get po busybox -o jsonpath='{.metadata}'
k get po busybox -o jsonpath="{['.metadata.name', '.metadata.namespace']}{'\n'}"
```
The command returns the internal IP of a Node using JSONPath:
```
kubectl get nodes -o=jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'
```
The command checks for Equality on a specific key:
```
kubectl get pod api-stag-765797cf-lrd8q -o=jsonpath='{.spec.volumes[?(@.name=="api-data")].persistentVolumeClaim.claimName}'
kubectl get pod -o=jsonpath='{.items[*].spec.tolerations[?(@.effect=="NoSchedule")].key}'
```
Custom Columns are helpful in order to output specific fields:
```
kubectl get pods -o='custom-columns=PODS:.metadata.name,Images:.spec.containers[*].image'
```

### CKS Exam Topics

The CKS exam covers delve on topics related to security in the Kubernetes ecosystem. Kubernetes security is a vast topic to cover in one article, this article contains some of the topics covered in the exam.

#### Securing and Hardening Container Images

While designing container images to run your code pay special attention to securing and hardening measures in order to prevent hacks and privilege escalation attacks. Keep the below points in mind while building the container images:

1. Use specific package versions like `alpine:3.13`.
2. Don't run as root, use the `USER <username>` to block root access.
3. Make filesystem read-only in the `securityContext` using `readOnlyRootFilesystem: true`
4. Remove shell access using `RUN rm -rf /bin/*`

#### Minimising OS Footprint

##### Conatiner Layers

The instructions `RUN` , `COPY` and `ADD` create container layers. Other instructions create temporary intermediate images and do not increase the size of the build. Instructions that create layers add to the size of the resulting image.

A typical Dockerfile looks like the one given below, it adds a single layer using the `RUN` instruction.
```
FROM ubuntu

RUN apt-get update && apt-get install -y golang-go

CMD ["sh"]
```

##### Multi Stage Builds

Multi-Stage builds leverage multiple `FROM` statements in the Dockerfile. The `FROM` instruction marks a new stage in the build, combining multiple `FROM` statements allow to leverage from the previous build in order to selectively copy binaries over to the new build stage omitting the unnecessary binaries. The resulting Docker image is considerably smaller in size with a drastically reduced attack surface.

```
FROM ubuntu:20.04 AS build
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y golang-go
COPY app.go .
RUN CGO_ENABLED=0 go build app.go

FROM alpine:3.13
RUN chmod a-w /etc
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -h /home/appuser
RUN rm -rf /bin/*
COPY --from=build /app /home/appuser/
USER appuser
CMD ["/home/appuser/app"]
```

#### Limit Node Access

Access Control files contain sensitive information about users/groups in the Linux OS.
```
#Stores information about the UID/GID, user shell, and home directory for a user
/etc/passwd
#Stores the user password in a hashed format
/etc/shadow
#Stores information about the group a user belongs
/etc/group
#Stored information about the Sudoers present in the system
/etc/sudoers
```

Disable user account helps in securing access to a Node by disabling login to a given user account.
```
usermod -s /bin/nologin <username>
```

Disabling the `root` user account is of special significance as the root account has all the capabilities.
```
usermod -s /bin/nologin root
```

Add a user with a home directory and shell
```
adduser --home /opt/faizanbashir --shell /bin/bash --uid 2328 --ingroup admin faizanbashir
useradd -d /opt/faizanbashir -s /bin/bash -G admin -u 2328 faizanbashir
```

Delete the user account
```
userdel <username>
```

Delete a Group
```
groupdel <groupname>
```

Add user to group
```
adduser <username> <groupname>
```

Remove user from a Group
```
#deluser faizanbashir admin
deluser <username> <groupname>
```

Set a password for the user
```
passwd <username>
```

Elevate a user to Sudoer
```
vim /etc/sudoers
>>>
faizanbashir ALL=(ALL:ALL) ALL

#Enable sudo with no password
vim /etc/sudoers
>>>
faizanbashir ALL=(ALL) NOPASSWD:ALL

visudo
usermod -aG sudo faizanbashir
usermod faizanbashir -G admin
```

#### SSH Hardening

##### Disable SSH

The configuration is given in the `/etc/ssh/sshd_config` can be leveraged to secure SSH access to Linux nodes. Setting the `PermitRootLogin` to `no` disables the root login on a node. To enforce using a key to login and disabling login using passwords to nodes the `PasswordAuthentication` can be set to `no`.
```
vim /etc/ssh/sshd_config
>>
PermitRootLogin no
PasswordAuthentication no
<<
# Restart SSHD Service
systemctl restart sshd
```

Set no login for the root user:
```
usermod -s /bin/nologin root
```

SSH Copy user key / Passwordless SSH:
```
ssh-copy-id -i ~/.ssh/id_rsa.pub faizanbashir@node01
ssh faizanbashir@node01
```

#### Remove Obsolete Packages and Services

List all services running on a Ubuntu machine.
```
systemctl list-units --type service
systemctl list-units --type service --state running
```

Stop and disable and remove a service:
```
systemctl stop apache2
systemctl disable apache2
apt remove apache2
```

#### Restrict Kernel Modules

In Linux, Kernel modules are pieces of code that can be loaded and unloaded into the kernel upon demand. They extend the functionality of the kernel without the need to reboot the system. A module can be configured as built-in or loadable.

List all Kernel Modules
```
lsmod
```

Manually Load Modules into Kernel
```
modprobe pcspkr
```

Blacklist a module: (Reference: CIS Benchmarks -> 3.4 Uncommon Network Protocols)
```
cat /etc/modprobe.d/blacklist.conf
>>>
blacklist sctp
blacklist dccp

# Shutdown for changes to take effect
shutdown -r now

# Verify
lsmod | grep dccp
```

#### Identify and Disable Open Ports

Check for Open Ports:
```
netstat -an | grep -w LISTEN
netstat -natp | grep 9090

nc -zv <hostname|IP> 22
nc -zv <hostname|IP> 10-22

ufw deny 8080
```
Check Port usage:
```
/etc/services | grep -w 53
```
Reference Doc for list of open ports:
https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#control-plane-node-s

#### Restrict Network Access

##### Identity a service running on port:
```
systemctl status ssh
cat /etc/services | grep ssh
netstat -an | grep 22 | grep -w LISTEN
```

##### UFW Firewall

Uncomplicated Fire Wall(UFW) is a tool for managing firewall rules in Arch Linux, Debian, or Ubuntu. UFW provides the functionality to allow and block traffic on a given port and from a given source.

Installing UFW Firewall
```
apt-get update
apt-get install ufw
systemctl enable ufw
systemctl start ufw
ufw status
ufw status numbered
```

Allow all outbound and inbound connections
```
ufw default allow outgoing
ufw default allow incoming
```

Allow Rules
```
ufw allow 22
ufw allow 1000:2000/tcp
ufw allow from 172.16.238.5 to any port 22 proto tcp
ufw allow from 172.16.238.5 to any port 80 proto tcp
ufw allow from 172.16.100.0/28 to any port 80 proto tcp
```

Deny Rules
```
ufw deny 8080
```

Enable / Activate Firewall
```
ufw enable
```

Delete rules
```
ufw delete deny 8080
ufw delete <rule-line>
```

Reset rules
```
ufw reset
```

#### Linux Syscalls

Linux Syscalls are used to make requests from user space into the Linux kernel. For instance, while creating a file the userspace makes a request to the Linux Kernel to create the file. 

Kernel Space has the following:
- Kernel Code
- Kernel Extensions
- Device Drivers

##### Tracing Syscalls using Strace

Tracing syscalls using strace
```
which strace
strace touch /tmp/error.log
```

Get PID of service
```
pidof sshd
strace -p <pid>
```

List all syscalls made during an operation
```
strace -c touch /tmp/error.log
```

Consolidated listing syscalls: (Count and summarise)
```
strace -cw ls /
```

Follow a PID and consolidate
```
strace -p 3502 -f -cw
```

#### AquaSec Tracee

AquaSec Tracee was created by Aqua Security which uses eBPF to trace events in containers. Tracee makes use of eBPF (Extended Berkeley Packet Filter) at runtime directly in the kernel space without interfering with the kernel source or loading any kernel modules.
- Binary stored at `/tmp/tracee`
- Needs access to the following, in read-only mode if run using a container with `--privileged` capability:
	- `/tmp/tracee` -> Default workspace
	- `/lib/modules` -> Kernel Headers
	- `/usr/src` -> Kernel Headers

Running Tracee in Docker container
```
docker run --name tracee --rm --privileged --pid=host \
  -v /lib/modules/:/lib/modules/:ro -v /usr/src/:/usr/src/ro \
  -v /tmp/tracee:/tmp/tracee aquasec/tracee:0.4.0 --trace comm=ls

# List syscalls made by all the new process on the host
docker run --name tracee --rm --privileged --pid=host \
  -v /lib/modules/:/lib/modules/:ro -v /usr/src/:/usr/src/ro \
  -v /tmp/tracee:/tmp/tracee aquasec/tracee:0.4.0 --trace pid=new

# List syscalls made from any new container
docker run --name tracee --rm --privileged --pid=host \
  -v /lib/modules/:/lib/modules/:ro -v /usr/src/:/usr/src/ro \
  -v /tmp/tracee:/tmp/tracee aquasec/tracee:0.4.0 --trace container=new
```

#### Restricting Syscalls with Seccomp

**SECCOMP** - Secure Computing Mode is a Linux Kernel level feature that can be used to sandbox applications to only use the syscalls they need.

Check support for seccomp:
```
grep -i seccomp /boot/config-$(uname -r)
```

Test to change system time:
```
docker run -it --rm docker/whalesay /bin/sh
# date -s '19 APR 2013 22:00:00'

ps -ef
```

Check seccomp status for any PID:
```
grep -i seccomp /proc/1/status
```

Seccomp modes:
- Mode 0: Disabled
- Mode 1: Strict
- Mode 2: Filtered

The following configuration is used to whitelist syscalls. While list profile is secure but syscalls have to be selectively enabled as it blocks all syscalls by default.
```
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X32"
  ],
  "syscalls": [
    {
      "names": [
        "<syscall-1>",
        "<syscall-2>",
        "<syscall-3>"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

The following configuration is used to blacklist syscalls. The black list profile has a greater attack surface than the white list. 
```
{
  "defaultAction": "SCMP_ACT_ALLOW",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_X32"
  ],
  "syscalls": [
    {
      "names": [
        "<syscall-1>",
        "<syscall-2>",
        "<syscall-3>"
      ],
      "action": "SCMP_ACT_ERRNO"
    }
  ]
}
```

The Docker seccomp profile blocks 60 of the 300+ syscalls on the x86 architecture.

Using seccomp profiles with docker
```
docker run -it --rm --security-opt seccomp=/root/custom.json docker/whalesay /bin/sh
```

Allow all syscalls with the container
```
docker run -it --rm --security-opt seccomp=unconfined docker/whalesay /bin/sh

# Verify
grep -i seccomp /proc/1/status

# Output should be:
Seccomp:         0
```

Docker container to get container runtime related information:
```
docker run r.j3ss.co/amicontained amicontained
```

##### Seccomp in Kubernetes

Secure computing mode (SECCOMP) is a Linux kernel feature. You can use it to restrict the actions available within the container. [Seccomp documentation](https://kubernetes.io/docs/tutorials/clusters/seccomp)

Run amicontained in Kubernetes:
```
kubectl run amicontained --image r.j3ss.co/amicontained amicontained -- amicontained
```

As of version `v1.20` Kubernetes does not implement seccomp by default.

Seccomp 'RuntimeDefault' docker profile in Kubernetes:
```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: amicontained
  name: amicontained
spec:
  securityContext:
    seccompProfile:
      type: RuntimeDefault
  containers:
  - args:
    - amicontained
    image: r.j3ss.co/amicontained
    name: amicontained
    securityContext:
      allowPrivilegeEscalation: false
```

Default seccomp location in kubelets
```
/var/lib/kubelet/seccomp
```

Create a seccomp profile in node
```
mkdir -p /var/lib/kubelet/seccomp/profiles

# Add a profile for audit
vim /var/lib/kubelet/seccomp/profiles/audit.json
>>>
{
  defaultAction: "SCMP_ACT_LOG"
}

# Add a profile for violations (Blocks all syscalls by default, will let nothing run)
vim /var/lib/kubelet/seccomp/profiles/violation.json
>>>
{
  defaultAction: "SCMP_ACT_ERRNO"
}
```

Local seccomp profile, this file should exist locally on a  node to be able to work
```
...
securityContext:
  seccompProfile:
    type: Localhost
    localhostProfile: profiles/audit.json
...
```

The above profile will enable syscalls to be saved to a file
```
grep syscall /var/log/syslog
```

Mapping syscall numbers to syscall name
```
grep -w 35 /usr/include/asm/unistd_64.h

# OR
grep -w 35 /usr/include/asm-generic/unistd.h
```

#### AppArmor

AppArmor is a Linux security module that is used to confine a program to a limited set of resources.

Install AppArmor utils
```
apt-get install apparmor-utils
```

Check if AppArmor is running and enabled
```
systemctl status apparmor

cat /sys/module/apparmor/parameters/enabled
Y
```

The AppArmor profiles are stored at
```
cat /etc/apparmor.d/root.add_data.sh
```

Listing AppArmor profiles
```
cat /sys/kernel/security/apparmor/profiles
```

Deny all file write profile
```
profile apparmor-deny-write flags=(attach_disconnected) {
  file,
  # Deny all file writes.
  deny /** w,
}
```

Deny write to `/proc` files
```
profile apparmor-deny-proc-write flags=(attach_disconnected) {
  file,
  # Deny all file writes.
  deny /proc/* w,
}
```

Deny remount root FS
```
profile apparmor-deny-remount-root flags=(attach_disconnected) {

  # Deny all file writes.
  deny mount options=(ro, remount) -> /,
}
```

Check profile status
```
aa-status
```

Profile load modes
- `Enforce`, monitor and enforce the rules
- `Complain`, will not enforce the rules but logs them as events
- `Unconfined`, will not enforce or log events

Check if a profile is valid
```
apparmor_parser /etc/apparmor.d/root.add_data.sh
```

Disable a profile
```
apparmor_parser -R /etc/apparmor.d/root.add_data.sh
ln -s /etc/apparmor.d/root.add_data.sh /etc/apparmor.d/disable/
```

Generate a profile and answer the series of questions that follow
```
aa-genprof /root/add_data.sh
```

Generate profile for a command
```
aa-genprof curl
```

Disable profile from logs
```
aa-logprof
```

##### AppArmor in Kubernetes

To be used with Kubernetes the following prerequisites must be met:
- Kubernetes version should be greater than `1.4`
- AppArmor Kernel module should be enabled
- AppArmor profile should be loaded in the kernel
- Container runtime should be supported

Sample usage in Kubernetes:
```
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper
  annotations:
    container.apparmor.security.beta.kubernetes.io/<container-name>: localhost/<profile-name>
spec:
  containers:
  - name: ubuntu-sleeper
    image: ubuntu
    command: ["sh", "-c", "echo 'Sleeping for an hour!' && sleep 1h"]
```

**Note**: The container should run in a node containing the AppArmor profile.

#### Linux Capabilities

The Linux capabilities feature breaks up the privileges available to processes run as the `root` user into smaller groups of privileges. This way a process running with `root` privilege can be limited to get only the minimal permissions it needs to perform its operation. Docker supports the Linux capabilities as part of the docker run command: with `--cap-add` and `--cap-drop`. By default, a container is started with several capabilities that are allowed by default and can be dropped. Other permissions can be added manually. Both `--cap-add` and `--cap-drop` support the ALL value, to allow or drop all capabilities. By default Docker containers run with 14 capabilities.

- Kernel < 2.2
	- Privileged Process
	- Unprivileged Process
- Kernel >= 2.2
	- Privileged Process
		- `CAP_CHOWN`
		- `CAP_SYS_TIME`
		- `CAP_SYS_BOOT`
		- `CAP_NET_ADMIN`

[Refer to this document for the full list of Linux Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)

Check what capabilities a command needs
```
getcap /usr/bin/ping
```

Get process capabilities
```
getpcaps <pid>
```

Add security capabilities
```
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper
spec:
  containers:
  - name: ubuntu-sleeper
    image: ubuntu
    command: ["sleep", "1000"]
    securityContext:
      capabilities:
        add: ["SYS_TIME"]
        drop: ["CHOWN"]
```


### Preparation for the Exam

CKS is considered a pretty tough exam by many but based on my experience I think given good enough practice and understanding the concepts the exam is pretty manageable within two hours. 

It is imperative to understand the underlying Kubernetes concepts and since the eligibility for CKS is to qualify the CKA exam, the candidate is supposed to have a strong understanding of Kubernetes and its functioning. What additional is required for CKS is to understand the threats and security implications introduced by container orchestration.

The introduction of the CKS exam is an indication that the security of containers should not be taken lightly, security mechanisms should be in place to thwart attacks on Kubernetes clusters. The [Tesla cryptocurrency hack](https://www.wired.com/story/cryptojacking-tesla-amazon-cloud/) thanks to an unprotected Kubernetes dashboard brings to light the risks associated with Kubernetes or any other container orchestration engine. [Hackerone has a Kubernetes bounty page](https://hackerone.com/kubernetes?type=team) listing the source code repo's used in a standard Kubernetes cluster.

### Practice, Practice, and Practice!

Practice is the key to cracking the exam, I personally found the exam simulators by KodeKloud and Killer.sh were immensely helpful for me while I didn't have a lot of time to prepare for the CKS exam as I had for the CKA exam, while I was working on Kubernetes in my day job. Practice is the key to success, best of luck with the exam.