## Architecture
![](diagram/rstudio_eks_solution.png)

## Installation
### Create EFS 
```
 aws cloudformation create-stack --stack-name rstudio-efs --template-body  file://efs.yaml
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

### Import Certificate into ACM
```
aws acm import-certificate --certificate fileb://certs/public.pem --private-key fileb://certs/private.pem
```
Record the generated ARN, as it will be used when creating EKS cluster resources. You can update it in [](/clusters/rstudio/aws-lb-controller.yaml)

### Create Profile for the EFS CSI Driver
```
curl -o efs-iam-policy-example.json https://raw.githubusercontent.com/kubernetes-sigs/aws-efs-csi-driver/v1.3.2/docs/iam-policy-example.json
aws iam create-policy --policy-name AmazonEKS_EFS_CSI_Driver_Policy --policy-document file://efs-iam-policy-example.json
```
### Create Profile fo the ALB Controller
```
curl -o alb_iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.1/docs/install/iam_policy.json
aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://alb_iam_policy.json
```



### Create EKS Cluster using eksctl

#### Modify eks.yaml as needed. 

#### Create the Cluster
```
eksctl create cluster -f eks.yaml   
```

### Create secret to be used for rstudio password
```
kubectl create secret generic rstudio --from-literal=passwword=***********
```

### Create secret in EKS for the certificates
```
kubectl create secret generic rstudio-certs --from-file=certs/
```

### Flux
Flux will be installed to the EKS Cluster when it is created, and will immediately start synching against the git repo specified in it's configuration. 
#### What Flux will install
* Help Repose for AWS componenets
* AWS Load Balancer Controller
* EFS Components (Storage Class, Persistent Volume, and the Persistent Volume Claim) that enable mounting of EFS
* All of the components for the RStudio Deployment (Ingress, Services, and the Deployment)




