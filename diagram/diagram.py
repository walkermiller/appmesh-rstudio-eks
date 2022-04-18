#! /opt/homebrew/bin/python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EKS, Fargate, ElasticContainerServiceContainer as Container
from diagrams.aws.network import VPC, ALB
from diagrams.aws.storage import EFS

from diagrams.k8s.compute import  Deployment, Pod
from diagrams.k8s.network import Ingress
from diagrams.k8s.group import Namespace
from diagrams.k8s.storage import PersistentVolume as PV, PersistentVolumeClaim as PVC, Volume
from diagrams.aws.general import Client


# graph_attr = {
#     # "splines":"curved",
#     "layout":"neato",
# }

with Diagram("Rstudio EKS Solution", direction="LR"):

    vpc_cluster = Cluster("AWS VPC")


    with vpc_cluster:

        alb = ALB("ALB")
        efs = EFS("Shared and Persistent EFS")
        with Cluster("EKS Cluster"):
            with Cluster("EKS Namespace: rstudio"):
                ingress = Ingress("Ingress")
                with Cluster ("Rstudio User 1 Deployment"):
                    with Cluster ("Fargate Node"):
                        with Cluster ("Deployment Pod"):
                            deploy_group1_haproxy = Container("haproxy container")
                            deploy_group1_rstudio = Container("rstudio container")
                        deploy_group1_volume = Volume("EFS")
                deploy_group1_pv = PV("EFS") 
                deploy_group1_pvc = PVC("EFS")
                with Cluster ("Rstudio User 2 Deployment"):
                    with Cluster ("Fargate Node"):
                        with Cluster ("Deployment Pod"):
                            deploy_group2_haproxy = Container("haproxy container")
                            deploy_group2_rstudio = Container("rstudio container")
                        deploy_group2_volume = Volume("EFS")
                deploy_group2_pv = PV("EFS") 
                deploy_group2_pvc = PVC("EFS")
                with Cluster ("Rstudio User 3 Deployment"):
                    with Cluster ("Fargate Node"):
                        with Cluster ("Deployment Pod"):
                            deploy_group3_haproxy = Container("haproxy container")
                            deploy_group3_rstudio = Container("rstudio container")
                        deploy_group3_volume = Volume("EFS")
                deploy_group3_pv = PV("EFS") 
                deploy_group3_pvc = PVC("EFS")
            # with Cluster("EKS Namespace: flux-system"):
            #     Deployment("Flux GITOPS")
    
    ## Define Connections
    Client("RStudio User") >> Edge(label="HTTPS (443)", style="bold") >> alb >> Edge(label="HTTPS (9099)", style="bold") >> ingress
    ingress >> Edge(label="user1.example.com HTTPS (9099)", style="bold") >> deploy_group1_haproxy
    ingress >> Edge(label="user2.example.com HTTPS (9099)", style="bold") >> deploy_group2_haproxy
    ingress >> Edge(label="user3.example.com HTTPS (9099)", style="bold") >> deploy_group3_haproxy
    deploy_group1_haproxy \
        >> Edge(label="HTTP (8787)", style="bold") >> deploy_group1_rstudio \
        << Edge(label="/data", style="bold") \
        << deploy_group1_volume \
        << deploy_group1_pv \
        << deploy_group1_pvc \
        << Edge(label="HTTPS", style="bold") \
        << efs
    deploy_group2_haproxy \
        >> Edge(label="HTTP (8787)", style="bold") \
        >> deploy_group2_rstudio \
        << Edge(label="/data", style="bold") << deploy_group2_volume \
        << deploy_group2_pv \
        << deploy_group2_pvc \
        << Edge(label="HTTPS", style="bold") \
        << efs
    deploy_group3_haproxy \
        >> Edge(label="HTTP (8787)", style="bold") \
        >> deploy_group3_rstudio \
        << Edge(label="/data", style="bold") \
        << deploy_group3_volume << deploy_group3_pv \
        << deploy_group3_pvc \
        << Edge(label="HTTPS", style="bold") \
        << efs