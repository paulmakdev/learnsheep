# ADR-00009: Initial User Object

## Status
Accepted

## Decision
Decided to add the following fields in the user object for the following reasons:

id: Easy way to reference user, has no meaning elsewhere (security), and can change email if need be
anonymous_id: Used to reference user before they sign up
email: unique, used as anti-bot measure as well
hashed_salted_password: salt helps prevent birthday attacks, hash makes it hard to find
role: enum-based, used to define if someone is there to learn, to teach / manage students, etc.
display_name: gives users a sense of uniqueness
created_at: when user account created
updated_at: when the user object was updated last
last_interaction_tz: last user interaction time (used to keep track of inactivity)
subscription: enum-based, currently just either subscribed or not

Enums:

Subscription
- No Subscription
- Learner
- Teacher

Role
- Student: 
    TEACHER = 'teacher'
    PARENT = 'parent'
    LOCAL_ADMIN = 'local-admin'
    ADMIN = 'admin'

Notes:
last_interaction_tz will be computed automatically after each interaction using SQLAlchemy
