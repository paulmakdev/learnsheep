# ADR-00010: Designing the frontend of Learnsheep.

## Status
Accepted

## Summary
Added the frontend code and infrastructure necessary. Created a dev and prod site. Added pre-login token for app access without logging in.

## Decision
Decided to implement frontend using React and TypeScript
- Modern framework, quick, fast, and efficient
- Modular development allows us to create components that can be used more than once.

Decided to use Redux
- Industry standard, allows for easy managing of global state without drilling down

Decided to make the homepage have a unique feel
- Added branded sheep all around
- After idling, a portion of the sheep start to move and jump around
- As number of animations / sheep expand, can change which animations / sheep are being used very easily

Decided on making Learnsheep have a very clean feel.
- I am not a designer, it's easier for me to make a clean look than a complicated one

Decided to use css variables to properly manage spacing, font-sizes, etc.

Decided on committing to modular development.
- Made the scrollers on the webpage modular

Decided to make lessons centered
- To make reading on screens easier

Decided to make lessons follow a set pattern.
- Definitions
    - A person should be able to see what immediate knowledge they will gain / half to know
- Concepts
    - A person should be able to understand what the lesson is trying to teach at a high level
- Story
    - Teaching the lesson with maximum engagement, examples, etc.
- Quiz / Game / Questions
    - Locking in the concepts into the brain.
    - Without a quiz, learning is very hard

Decided to make multiple ways to find lessons
- Allows someone to use whichever method they find easiest.

Decided to give lessons a canonical and a Module / Subject / Lesson route. (routes to same page)

Decided to use dictionaries (JSON objects) to show current lessons / lesson details / definitions, etc.
- Can use definitions / concepts for fuzzy search
- Very easy to import

Decided to add a route about the current sessions.

Decided to add a pre-login auth token.
- Some users might not be logged in
- Will save progress up to 30 days
- Progress saves after registering, as we only change email and password, but keep id
- Allows maximum instant engagement
    - Someone can access the full features of the app without having to click too many buttons
- All tokens made pre-login are marked, as well as the user entry in db
- Will not have access to routes like payments when the time comes
- Email and password are going to be NULL for the pre-login created account.

Added proper logging for local testing using Python's logger.

Decided to create env files for dev vs production for Vite so that we can test properly locally.

Decided to use AWS CloudFront to stand in front of our website stored on S3.
- CloudFront hypothetically helps it get served faster.
- We will qualify for free tier for a long time
- Nice to not have to worry about S3 security (all public access blocked)

Decided to define two separate modules based on same code in Terraform config (for dev and prod)
- Allows us to do public testing on the dev site before moving to prod
    - Technically, this is more of QA because we already have the ability to test everything locally
- All it requires is having separate variables

Decided to have Terraform make the roles for the website
- Pushing for keeping things more IaC (Infrastructure as Code)

Decided to make Github Actions push website code.
- Automatically to dev on push to main
- Need to activate workflow for push to prod

Decided to keep a 1 main branch architecture
- Can push to prod manually
- Prod branch only exists for the sake of pushing code, can roll back using dev commits
- Easier for me as a 1 man team
- Subject to change, would be a very quick change

## Future Work
At some point, should add the ECS roles to Terraform to really stick to IaC
