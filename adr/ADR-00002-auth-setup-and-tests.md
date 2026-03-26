# ADR-00002: Auth Setup and Tests

## Status
Accepted

## Summary
Detail of auth setup and related choices made.

## Decision
Decided to use JWT vs session tokens because JWT allows the client to connect to any server with bearer token verification.

Decided to use passlib because it allows for easy encryption / verification, etc.

Decided to use bcrypt for encryption because it is slow (discourages attackers), secure, and automatically salts passwords.

Decided to keep email / password login blind to which credential is wrong if error (to discourage phishing and other attacks).

Decided to use pydantic for verifying all types, values, etc. This makes the code a LOT cleaner. Also lets us not reinvent the wheel.
- Note that we still have to verify all business logic, which is normal and expected.

Decided to use pytest for testing (modern). Allows us to quickly build tests databases and destroy when done. Easily repeatable and quick.
- Also integrates very easily with FastAPI

Added login and registration endpoints w/ email and password, but note that at some point we should add functionality for Google logins as well (commonly used)
- people might be too lazy to use email, password
- might be the same logic, need to research
