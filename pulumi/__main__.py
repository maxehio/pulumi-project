import pulumi
import pulumi_aws as aws
import json
import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

execution_role = aws.iam.role("base-role")

# Create an IAM Role for ECS tasks
execution_role = aws.iam.Role("ecsExecutionRole",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Effect": "Allow",
        }]
    })
)

# Attach the ECS Task Execution Role policy
policy_attachment = aws.iam.RolePolicyAttachment("ecsExecutionRoleAttachment",
    role=execution_role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
)

# Now reference this role in your ECS Task Definition
task_def = aws.ecs.TaskDefinition("app-task",
    # other properties as before...
    execution_role_arn=execution_role.arn,
)

# Define an ECS Cluster
cluster = aws.ecs.Cluster("app-cluster")

# Define the ECS Task Definition
task_def = aws.ecs.TaskDefinition("app-task",
    family="my-application",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=execution_role.arn,
    container_definitions=json.dumps([{
        "name": "my-container",
        "image": "my-django-app:latest",
        "essential": True,
        "environment": [
        {"name": "DEBUG", "value": "False"},
        {"name": "SECRET_KEY", "value": SECRET_KEY},
        {"name": "CONFIG_VALUE", "value": "Greetings!"}
        ],
        "memory": 512,
        "portMappings": [{"containerPort": 8000, "hostPort": 8000}],
        }]),
)

# Define the ECS Service
service = aws.ecs.Service("app-service",
    cluster=cluster.id,
    desired_count=1,
    launch_type="FARGATE",
    task_definition=task_def.arn,
    network_configuration={
        "assign_public_ip": True,
        "subnets": [subnet.id],
        "security_groups": [security_group.id],
    }
)
