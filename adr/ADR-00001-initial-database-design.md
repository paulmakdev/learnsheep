# ADR-00001: Initial Database Design

## Status
Accepted

## Summary
Detail of decisions made in initial databse design and why.

## Decision
`users` table:

id: Easy way to reference user, has no meaning elsewhere (security), and can change email if need be
anonymous_id: Used to reference user before they sign up
email: unique, used as anti-bot measure as well
hashed_salted_password: salt helps prevent birthday attacks, hash makes it hard to find
role: enum-based, used to define if someone is there to learn, to teach / manage students, etc.
display_name: gives users a sense of uniqueness
created_at: when user account created
updated_at: when the user object was updated last
user_source: where the user came from (useful for analytics)
gdpr_consent_at: Need consent in California + EU to use user data (compliance)
data_deletion_requested_at: must be an option in California, EU (compliance)

`lessons`, `modules`, `subjects`, `module-lessons`, `subject-modules` tables:

lesson_metadata: Used for whatever extra information we might want to store about a lesson
module_metadata: Used for whatever extra information we might want to store about a module
subject_metadata: Used for whatever extra information we might want to store about a subject
- These metadata fields will include stuff like base-image paths (so it's easy to visually select a lesson)

id: easy to keep track of
title: used for naming
s3_key: used for page source

The `module-lessons` and `subject-modules` tables exist to identify relationships between the lessons, modules, and subjects. A lesson can belong to multiple modules, and a module can belong to multiple subjects. The results will be cached, and are used to generate the JSON for the lesson selector.

`subscriptions` table:

Used to keep track of user's current and past subscriptions.

id: keep track of a subscriptiopn
user_id: id of user with the subscription
status: status of subscription -- is it active or inactive
billing_frequency: how often the period changes
current_period_start: period start
current_period_end: period end
recurring: whether or not the user is only subscribed for x months or longer
start_day: day the subscription was originally created
cancel_day: day the subscription was cancelled
cancel_reason: text reason why the subscription was cancelled
cancel_enum_reason: once we have a good list of reasons why people might unsubscribe, can build an easy selector for easier analysis

indexes:
- user_id: will need to check subscription on user every time logging in and for other things

`questions` table:

Used for all the quizzing that will be done on Learnsheep

id: keep track of a question
lesson_id: what lesson this question belongs to or should be asked in
difficulty: how hard is the question
template: JSON used to build the question dynamically
times_encountered: number of times a question was asked
times_correct: number of times people got the question correct (used to track difficulty with times_encountered)
generator_group_id: id of the generator which should be used for the question template

`question_history` table:

Used to keep track of the quizzes that a user has taken on Learnsheep.

id: unique id for every answer
user_id: user to whom it was asked
question_id: which question was asked
lesson_id: which lesson was the question asked in
question_terms: the terms used dynamically in the question
question_answer: the correct answer to the question
user_answer: the user's answer to the question
correct: is the user's answer correct?

constraints:
- question_id + lesson_id matches the question_id + lesson_id combo in the questions table

indexes:
- user_id + lesson_id: used for question history for a specific user on a specific lesson

`question_generator_groups` and `question_predefined_values` tables:

Used for having content sets for questions. I.e. Let's say I have a question like:
_ goes to the _.

I don't want to use random nouns. I want to use a set like
Bob, store
Billy, supermarket

or other common lists in this way. This just gives me an easier way to generate similar questions and sentences in quizzes if need be.

For question_generator_groups, we have:

id: id of the generator group
generator_type: word generator? number generator?
name: description of the generator and why it exists

So for question_predefined_values, we have:

id: id of the predefined value
generator_group_id: the generator this value belongs to
value: the value itself
value_type: used by generator along with pair_order
pair_index: only exists if it belongs to a pair. So from our example, Bob and store would both have pair_index 1.
pair_order: used for the order that these groupings should be in.

indexes:
- generator_group_id + pair_index, used to pick which values to use for the generator this time

`progress` table:

id: id of progress
user_id: which user has progress
lesson_id: on which lesson is there progress
level: what's the current level of progress on this lesson by this user
level_progress: how far along the level we are
answered_questions: how many questions answered
questions_correct: how many questions were answered right
questions_incorrect: how many questions were answered wrong
understanding_metadata: what subtopics does the user struggle with or what do they excel at?
updated_at: when was this updated -> can use to check if user is learning

indexes:
- user_id + lesson_id, used to see progress by a user for a lesson
- lesson_id, can be used for statistics based on just a lesson id

`payments` table:

id: id of payment
subscription_id: id of subscription
user_id: user_id which made payment
amount_cents: how much was paid
period_start: start of payment period
period_end: end of payment period
failure_reason: reason the payment might have failed (used to keep track of errors)
provider: which payment provider was used
provider_payment_id: the id of the payment under the provider
provider_invoice_id: the invoice id of the payment under the provider
invoice_url: url of invoice under the provider
retry_count: how many times payment tried to redo if failed
next_retry_at: when next payment attempt might have to be made
created_at: time payment was first attempted / made
updated_at: when payment updated / completed

indexes:
- user_id: check payment history
- subscription_id: run subscription-based analytics for dashboard

`interactions` table:

id: interaction id
user_id: which user interacted
session_id: to group interactions together
anonymous_id: for non logged-in users

event_type: type of event (click, submit, etc.)
event_category: category of event (navigation, lesson, quiz, etc.)

page_url: full url
page_path: domain-specific url
referrer_url: where the traffic came from

properties: event-specific payload

ip_address
user_agent
device_type
browser
os
screen_width
screen_height

created_at: when event was created
client_ts: client timestamp
server_ts: server timestamp

indexes:
- user_id + session_id, used to keep track of a user's events, as well as which session they were in when event happened

