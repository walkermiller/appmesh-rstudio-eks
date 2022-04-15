## Architecture
![](diagram/rstudio_eks_solution.png)

## Installation
### Create EFS 
```
 aws cloudformation create-stack --stack-name rstudio-efs --template-body  file://efs.yaml
```
### Create EKS Cluster using eksctl

#### Modify eks.yaml as needed. 

#### Create the Cluster
```
eksctl create cluster -f eks.yaml   
```
### Generate Certificates
You can skip this step if you already have generated certs. 
```
cd /tmp/
mkdir certs

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/privateKey.key -out certs/certificate.crt
openssl rsa -in certs/privateKey.key -text > certs/private.pem 
openssl x509 -inform PEM -in certs/certificate.crt > certs/public.pem 

## HAProxy requires the certs in one file. 
cat certs/private.pem >> certs/public_and_private.pem
cat certs/public.pem >> certs/public_and_private.pem
```
### Create secret in EKS for the certificates
```
kubectl create secret generic rstudio-certs --from-file=certs/
```

