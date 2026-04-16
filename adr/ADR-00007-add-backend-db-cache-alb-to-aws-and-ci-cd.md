# ADR-00007: Making the backend, db, cache, and load balancer live on AWS. Also added CI/CD for auto-deployment.

## Status
Accepted

## Summary
Set up the backend (ECS container), database (RDS), ALB (Application Load Balancer) and Redis cache (ElastiCache) on AWS.

## Decision
Followed the infrastructure defined in ADR-00005. This is the final structure we have:
When making requests:
Internet -> Our VPC -> IGW -> 1 of 2 public subnets (based on AZ) -> ALB -> 1 of 2 private subnets (based on AZ) -> backend

From there, the backend has access to
- Redis cache
- Our db
- VPC endpoints (AWS services living inside of our private subnet like secrets manager, ECR, and EC2)
  - These are a bit expensive, but it is the proper security structure that we want

The backend can only send requests back through the same way they went in.

Decided to have AWS generate the db credentials for us through Terraform and the "manage_master_user_password" field.
- This changed the way we got the creds in our backend, adjusted

Decided to have Terraform generate Redis creds
- Either way, Redis cache is NOT exposed to the internet, but this is an extra security measure for potential compliance in the future
- Just need to make sure that .tfvars file is not pushed to public
- Adding key to Redis lets use encrypted communications too (TLS)

Decided to add automatic CI and CD through Github Actions.
- We have lint and backend (pytest that works locally too) tests running automatically
- We automatically create a new container image based on our backend and push it to ECR.
- This way, we have final checks and pushing that is automatic, so we can focus on tests and development

Also made sure our Alembic migrations are working properly with Postgres enums.

Tested that our container is successfully running in the AWS Cloud!
