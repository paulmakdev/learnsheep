![Learnsheep sheep saying that app architecture is for everybody.](static-readme-assets/learnsheep_transparent_architecture_image.png)

Visit us live at [https://learnsheep.com](https://learnsheep.com)

# Table of Contents

- [Mission](#mission)
- [Architecture](#architecture)
    - [Infrastructure](#infrastructure)
        - [What is it built on?](#what-is-the-infrastructure-built-on)
        - [How is it provisioned?](#how-is-the-infrastructure-provisioned)
        - [What does it actually look like and why?](#what-does-the-infrastructure-look-like-and-why)
            - [Website Infrastructure](#website-infrastructure)
            - [Backend Infrastructure](#api-infrastructure)
- [The App Itself and Decision Logs](#the-app-itself-and-decision-logs)
- [Usage of Repository](#usage)
- [Final Message](#final-message)


# Learnsheep's Mission
## What is Learnsheep?
Learnsheep is an educational site created to give everyone access to high-quality, easy-to-understand education.
## Who is Learnsheep for?
Everyone!
## Why is Learnsheep unique?
Sometimes hard concepts are not explained in a way everyone can understand; Learnsheep is trying to fix that.
Every lesson is crafted with common language and does not assume prior knowledge.

# Learnsheep's Architecture
## Infrastructure
### What is the infrastructure built on?
Learnsheep's infrastructure is powered by AWS, CloudFlare, and GitHub.

Why AWS?
- Easy to manage, low-cost infrastructure

Why CloudFlare?
- Cheap domain & DNS services :)

Why GitHub?
- Version control and easy GitHub Actions to automate pushing to infrastructure.

### How is the infrastructure provisioned?
Learnsheep is dedicated to Infrastructure as Code (IaC). We use Terraform to provision the AWS infrastructure and manage CloudFlare DNS as needed.
Why Infrastructure as Code?
- Easily auditable
- Easy to review
- No need to chase down settings someone made 7 years ago
- Allows us to scale as needed
- Easy to keep track of changes

Why Terraform?
- Terraform is an industry standard for managing AWS infrastructure, it is well-made, and free to use (for our case, at time of writing)
- Very easy to break down infrastructure into modules

### What does the infrastructure look like and why?
#### Website Infrastructure
On a high level, this is how connecting to learnsheep.com works:
1. You send a request to the DNS server (CloudFlare) for learnsheep.com (if not already cached), which replies with the IP of our CloudFront distribution.
2. The CloudFront distribution sees the request and serves you index.html from our S3 bucket.
3. index.html imports the minified JavaScript (React) from the S3 bucket as well (using the same path)

Why do we connect to learnsheep.com in this way?
- This is fairly standard React single-page application architecture, so we have plenty of resources for debugging
- S3 bucket remains hidden from public
- We can update the website in pretty much one click.
- It is generally very fast

What architecture did we have to provision for this?
- S3 Bucket
    - For hosting the static files which serve the website
    - Easy to setup and configure version revision as needed
    - Since storage is fairly small, it is very cheap
    - We don't pay for egress through CloudFront (so we don't double pay)
- CloudFront
    - Hides the S3 bucket from public
    - Allows us to route API requests to our API instead of S3
    - Allows us to make index.html our default page (which is what we want for React single page app)
    - Generous free tier for egress and request number
- CloudFlare
    - This is our DNS server
    - Many free tools, easy to setup, and cheap

#### Backend Infrastructure
Now that we have talked about the website, let's talk about the API.

On a high level this is how the API works:
1. Your browser, based on your actions with learnsheep.com, decides to send an API request to learnsheep.com/api/*
2. The browser sends a request to the DNS server (CloudFlare) for learnsheep.com (if not already cached), which replies with the IP of our CloudFront distribution.
3. The browser sends the API request to the IP of the CloudFront distribution.
4. The CloudFront distribution sees the browser's API request, and notes the path of /api/*, so based on the rules, it must send the API request to api.learnsheep.com.
5. CloudFront sends a request to the DNS server (CloudFlare) for api.learnsheep.com, which replies with the IP of our Application Load Balancer (ALB).
6. CloudFront sends the API request to the Application Load Balancer.
7. The Application Load Balancer decrypts the HTTPS request and sends it to the backend container running on Elastic Container Service (ECS).
8. The backend verifies that the origin of the request is learnsheep.com (checks Origin header).
9. The backend processes the request and communicates with the Redis cache (ElastiCache) and Postgres database (RDS) as needed to fulfill the request.
10. The backend sends a response back to the ALB, which forwards it over HTTPS to CloudFront, which returns it to the browser.

Why do we connect to our API in this way?
- We can only access our API through requests to learnsheep.com/api -- this allows us to avoid Cross-Origin Resource Sharing (CORS) exploits
    - Long story short, badsite.com can't just send requests on your behalf to the API.
- Cookies, which will hold our auth tokens for the web version of the app, are only sent on API requests made by the user
    - They are strictly sent (based on their settings) only on requests to learnsheep.com to prevent all sorts of auth attacks
- We can control our backend and how we deal with requests behind the scenes
    - At any point, we are free to completely change the backend, route requests differently, or change which requests go where
    - We can always increase the number of load balancers or change the way we are balancing loads
- We can control the amount of resources our backend needs
    - We can scale the backend containers up and down as needed, with varying amounts of resources
    - We can increase the size of caches / change the read/write capabilities of the databases
- There is only one way to access our API, and that's through the Application Load Balancer
    - The Application Load Balancer lives on a public subnet, but sends requests to our backend which lives on a private subnet with the cache and the database.
    - There is no other way to access the backend, cache, or database, as we have strict security groups and rules
    - The backend, cache, and database don't even have a developer backdoor
        - If logs are needed, one can check CloudWatch for errors (automatically populated based on our settings)
        - This gives us maximum security, even if the speed of development may be slightly hindered

What architecture did we have to provision for this?
- CloudFront
    - Allows us to route API requests to our API instead of S3
    - Hides backend requests
    - Automatically filters some bots
    - Allows us to make index.html our default page (which is what we want for React single page app)
    - Generous free tier for egress and request number
- CloudFlare
    - This is our DNS server
    - Many free tools, easy to setup, and cheap
- Virtual Private Cloud (VPC)
    - This is where our Application Load Balancer and backend live.
    - This is our own network, where we can control the traffic and rules
    - We can separate public and private traffic in our VPC
- Internet Gateway (IGW)
    - Provides internet access to the public subnets in the VPC.
- Application Load Balancer (ALB)
    - Receives requests and automatically distributes them to a healthy (based on health check) container containing the backend, based on preset rules
- Elastic Container Registry (ECR)
    - Stores our backend container definition so we can run it at any time
- Elastic Container Service (ECS)
    - Runs a certain number of backend containers with a set number of resources, based on the definitions set
- ElastiCache
    - Runs our Redis cache (managed service)
- Relational Database Service (RDS)
    - Runs our Postgres database (managed service)
- Private VPC Endpoints
    - These endpoints allow us to connect to AWS services directly within our private subnet (no public access or traffic)
    - We have interface endpoints (paid) for the following services:
        - Elastic Container Registry (ECR) API: Allows us to run the commands necessary for pulling our backend containers
        - Elastic Container Registry (ECR) DKR (Docker Registry): Allows us to do the data transfer to actually get the backend containers
        - CloudWatch: Allows us to export logs
        - Secrets Manager: Allows us to store secrets within AWS -- secrets are identified by resource number and automatically translated by AWS
    - We have gateway endpoints (free) for the following services:
        - S3: Allows us to access static files, as needed, for the backend (could be used for quiz system).

Why do we need an ElastiCache (Redis) cache?
- We use ElastiCache because it allows us to use Redis as a managed service, giving us fairly cheap pricing, easy scaling, high availability
- Some things, like session tokens, access tokens, or quiz questions (generated), need fast and temporary access
    - Redis gives us the ability to find information very quickly (based on string keys) and auto-expires what we don't need

Why did we choose Relational Database Service (RDS)?
- Most of Learnsheep's data is row-based (relational)
- We can run Postgres instances
    - Our team has experience with Postgres
    - Easy to combine with SQLAlchemy / Alembic
- We have fairly cheap pricing, easy scaling, high availability, and we don't have to patch anything or manage storage, it is managed by AWS
    - We do not have a large enough team or specific need to justify running our own database instances
    - Having or managing all of these features is an undertaking in and of itself -- the costs are high with little benefit

Why did we choose Elastic Container Service (ECS)?
- We can auto-scale as needed, both vertically and horizontally
- We can test our containers easily from anywhere
- We don't have to manage the underlying operating system
- We don't need the more complicated overhead of tools like Kubernetes to manage the containers (especially at this stage)

# The App Itself and Decision Logs

You can find every decision made when creating the app in the decision logs (architecture decision records (ADRs)) found in the [adr](adr) folder.

All major app design decisions can be found in the folder
- Each record is associated with GitHub commits (for tracking)
- Allows us to track progress easily
- Allows us to go back and check why certain design choices were made
- Keeps development focused and specific

# Usage
I ask that you do not directly copy this code or train models on it.

I reserve the right to make any and all changes to this repository.

As always, everyone always has the right to take ideas, think about them, and change them to suit their needs. Inspiration is always welcome and is a fundamental part of the mission of Learnsheep. I ask that you use good judgement :).

# Final Message
Learning is for everybody, even sheep, and even you. You can do it. I believe in you.

[Table of Contents](#table-of-contents)
