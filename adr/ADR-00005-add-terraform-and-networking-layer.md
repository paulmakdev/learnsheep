# ADR-00005: Adding Terraform and the AWS Networking Layer

## Status
Accepted

## Summary
Set up terraform for Infrastructure as Code and added the AWS networking layer through it.

## Decision
Decided to use AWS as the provider because it is fairly cheap and widely used.

Decided to use Infrastructure of Code for the AWS setup to make the infrastructure repeatable / easily changed.

Decided to use Terraform because it is open source and easy to use for making Infrastructure as Code.

Decided on the following network architecture for our backend (fairly standard):
- Virtual Private Cloud (VPC) (for each region, currently planning on only 1, can expand if needed using Route 53 AWS service)
  - This is our private network
  - Only we can touch this and make changes
  - Contains public/private subnet pairs for each AZ
    - Public is for the Application Load Balancer (ALB) to be attached to
      - Load balancer sends from Internet Gateway (public) to services (private)
    - Private is for our containers / cache / db
        - We don't want anyone to be able to access those, EXCEPT through our webapp
  - Contains an Internet Gateway (IGW)
    - This gives access to the internet to connect to our subnet, as we describe
    - We can allow only certain connections (like accept only HTTPS connections)
    - Traffic goes from the Internet Gateway to the Application Load Balancer

Why this architecture?
- We can control traffic in/out very easily.
- Our backend only sees the requests made to it, cache and db only touched by backend, NOT anyone else
- Scalable -> we can expand to multiple regions with the same architecture, especially since we have Infrastructure as Code
    - We can also scale up a certain region by increasing the number of containers / increasing resources

Decided that security groups will belong to their respective resources. This seems to be the industry standard.
