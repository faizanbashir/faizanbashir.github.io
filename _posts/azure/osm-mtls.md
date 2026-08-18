# Implementing mTLS on an Azure Kubernetes Service (AKS) Cluster using Open Service Mesh

In this guide, we will demonstrate the steps needed to implement Mutual Transport Layer Security (mTLS) on an Azure Kubernetes Service (AKS) cluster using Open Service Mesh (OSM). mTLS provides bidirectional encryption of communications between a client and server, significantly enhancing the security of your cluster.

## Prerequisites

To follow along with this guide, you should have:

- An active Azure subscription
- The Azure CLI installed on your local machine
- An AKS cluster up and running
- `kubectl` and `osm` command-line tools installed

## Table of Contents

- [Installing Open Service Mesh](#installing-open-service-mesh)
- [Enabling mTLS on OSM](#enabling-mtls-on-osm)
- [Injecting OSM Sidecar Proxy](#injecting-osm-sidecar-proxy)
- [Validating mTLS](#validating-mtls)
- [Conclusion](#conclusion)

## Installing Open Service Mesh

The first step is to install the OSM controller on our AKS cluster. This is as simple as running the `osm install` command:

```bash
osm install
```

## Enabling mTLS on OSM

By default, OSM enables mTLS. However, if it has been disabled, you can enable it again using the `osm mesh upgrade` command:

```bash
osm mesh upgrade --enable-mtls
```

## Injecting OSM Sidecar Proxy

The next step is to add the applications to the OSM service mesh by injecting an Envoy sidecar proxy into the application's pods. For this, you will need to label your application's namespace with `openservicemesh.io/monitored-by=osm`:

```bash
kubectl label namespace <your_namespace> openservicemesh.io/monitored-by=osm
```

Next, for existing deployments, you would need to restart your deployments after labeling the namespace. You can do this by scaling your deployment down to 0 and then back up again:

```bash
kubectl scale deploy <your_deployment> --replicas=0 -n <your_namespace>
kubectl scale deploy <your_deployment> --replicas=<original_replica_count> -n <your_namespace>
```

New pods created in the namespace will automatically have the Envoy proxy sidecar injected, which is responsible for encrypting and decrypting the mTLS communications.

## Validating mTLS

To confirm mTLS is working correctly, you can check the outbound connections of the Envoy proxy logs:

```bash
kubectl logs -n <your_namespace> <pod_name> envoy -f | grep 'TLS handshake'
```

The logs should show a successful TLS handshake for your services' communications.

## Conclusion

With Open Service Mesh, it is straightforward to enhance the security of your Azure Kubernetes Service cluster by enabling mTLS. The process of setting up mTLS with OSM mainly involves installing the OSM control plane, enabling mTLS, and injecting the Envoy sidecar proxy into your application pods. It is crucial to validate the mTLS setup to ensure the secure communication of your services in the cluster.