# ADR-00006: Elastic Container Registry (ECR) Setup

## Status
Accepted

## Summary
Set up Elastic Container Registry (ECR) through Terraform and published backend container through Docker.

## Decision
Decided to use Terraform for setting up the ECR policies for our backend container.

Decided on image retention policy for keeping 10 latest Docker images
- Fairly cheap
- Subject to change if needed
- Will be useful if rollback needed, as we currently don't have the budget for a dedicated dev server

Successfully pushed our backend to ECR.
