### PROBLEM Statement

1. Create 3 applications :
   A, B ,C in python language and deploy them in any Kubernetes Cluster(Minikube)
2. When API to Application A is called, it needs to connect with application B and provide the response of POD IP.
3. Application B cannot be called independently or through App C, It should be only called through Application A
4. When API to Application C is called, it should be returning its own IP.
5. Application A or C cannot be called by each other.
6. All the deny rules above need to be handled at kubernetes layer, not at the application code level
7. The connectivity between A and B needs to be secure i.e TLS communication, but again this should be configured outside of application code.

### Abstract

To achieve the problem requirements in a Kubernetes environment

1. Create Python Applications (A, B, C) using flask

```bash
Application A:
    - Exposes an API endpoint /connect-b.
    - Connects to Application B and returns the POD IP of Application B.
    - Cannot connect to Application C.
```

```bash
Application B:
    - Exposes an API endpoint /pod-ip.
    - Can only be accessed by Application A.
    - Responds with its own POD IP.
```

```bash
Application C:
    - Exposes an API endpoint /pod-ip.
    - Responds with its own POD IP.
    - Cannot connect to Application A.
```

### Create Cluster
```bash
kind create cluster --config kind-config.yaml
```

### Build

#### Steps to Build and Push Docker Images:

```bash
docker build -t app-a:latest -f Dockerfile .
docker build -t app-b:latest -f Dockerfile .
docker build -t app-c:latest -f Dockerfile .
```

## For remote hub
```bash
kind load docker-image app-a:0.0.1 --name k8splayground
kind load docker-image app-b:0.0.1 --name k8splayground
kind load docker-image app-c:0.0.1 --name k8splayground

docker push your-docker-registry/app-a:latest
docker push your-docker-registry/app-b:latest
docker push your-docker-registry/app-c:latest
```
### Create namespace
```bash
kubectl apply -f k8s-manifests/namespace.yaml
```

### Deploy and Expose

```bash
kubectl apply -f k8s-manifests/deployments/
```

```bash
kubectl apply -f k8s-manifests/services/
```

at this point there is no restriction for accessing different services

```bash
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests# k exec -it app-c-97dfbf968-hcch2 -n app-c -- curl 192.168.45.67:5000/connect-b
{
  "app_b_response": {
    "message": "Hello from Application B!",
    "pod_ip": "192.168.188.6"
  },
  "message": "Connected to Application B"
}
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests# k exec -it app-c-97dfbf968-hcch2 -n app-c -- curl 192.168.188.6:5000/connect-b
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests# k exec -it app-c-97dfbf968-hcch2 -n app-c -- curl 192.168.188.6:5000/
{
  "message": "Hello from Application B!",
  "pod_ip": "192.168.188.6"
}
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests#
$
```


## Apply Network policy
```bash
 k apply -f network-policies/deny-all.yaml
 k apply -f network-policies/allow-app-a-to-app-b.yaml
```

### The connectivity will be restricted from C to A and B , B only accepts from A

```bash
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests# k exec -it app-c-97dfbf968-hcch2 -n app-c -- curl 192.168.188.6:5000/
^Ccommand terminated with exit code 130
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests# k exec -it app-c-97dfbf968-hcch2 -n app-c -- curl 192.168.45.67:5000/
^Ccommand terminated with exit code 130
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests# k exec -it app-a-7cf96b494-54j7h -n app-ab -- curl 192
.168.188.6:5000/
^Ccommand terminated with exit code 130
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests# k apply -f network-policies/allow-app-a-to-app-b.yaml
networkpolicy.networking.k8s.io/allow-app-a-to-app-b created
networkpolicy.networking.k8s.io/default-deny-all unchanged
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests# k exec -it app-a-7cf96b494-54j7h -n app-ab -- curl 192.168.188.6:5000/
{
  "message": "Hello from Application B!",
  "pod_ip": "192.168.188.6"
}
root@DESKTOP-813F7DC:/mnt/c/Users/Bikram/Downloads/k8s-sample-app/k8s-manifests#
```

### TLS connectivity using ingress , other options can be istio /linkerd or similar
### NOT USED FOR this requirement , DO NOT DEPLOY
- genrate a private key and a self-signed certificate
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout tls.key -out tls.crt \
-subj "/CN=app-b.example.com/O=Home"

```
- Create a Kubernetes Secret
```bash
kubectl create secret tls app-tls --cert=tls.crt --key=tls.key -n app-ab
```

- Configure ingress with tls
```bash
kubectl label nodes k8splayground-control-plane ingress-ready=true
kubectl label nodes k8splayground-worker ingress-ready=true
kubectl label nodes k8splayground-worker2 ingress-ready=true
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```
##### TLS connectivity using istio 
### Used for this requirement
```bash
kubectl label namespace app-ab istio-injection=enabled
kubectl label namespace app-c istio-injection=enabled
```

`istioctl install --set profile=demo`

```bash
k apply -f ingress/ision/ .
```



### Delete istio 
`istioctl uninstall --purge`


