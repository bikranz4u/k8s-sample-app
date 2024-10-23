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

### Build

#### Steps to Build and Push Docker Images:

```bash
docker build -t <your-docker-registry>/app-a:latest -f Dockerfile .
docker build -t <your-docker-registry>/app-b:latest -f Dockerfile .
docker build -t <your-docker-registry>/app-c:latest -f Dockerfile .
```

```bash
docker push your-docker-registry/app-a:latest
docker push your-docker-registry/app-b:latest
docker push your-docker-registry/app-c:latest
```
