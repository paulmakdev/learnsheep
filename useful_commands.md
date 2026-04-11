
## Docker

### How to build the backend Docker container from root
docker build -t learnsheep-backend -f backend/Dockerfile .

### How to start all Docker containers from root
docker compose up -d

### How to stop all Docker containers from root
docker compose down

### Give Docker access to AWS ECS
aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

## Terraform

### How to check out changes to infrastructure before applying
terraform plan

### How to publish infrastructure
terraform apply

### How to view an output variable
terraform output $variable_name
