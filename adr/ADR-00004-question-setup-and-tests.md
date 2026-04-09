# ADR-00004: Question Setup and Tests

## Status
Accepted

## Summary
Added question and answer capability to the API, level progression, and wrote tests.

## Decision
Created the idea of a generated question.

A generated question has the following properties:
- Can only be answered once (new values generated each time)
- Has an answer solution list
- Can have a set of possible answer choices supplied to user (but not verifying that something is an option when answer returned, as we only care if correct or not)
- Has an associated session token used to answer the question
- Associated with a specific user
- Uses specific generators for the question expression
- Has certain generated values that are set BEFORE sending to user

Made it so that a user can only answer THEIR question using a session token appended to their user id (prepended on backend).

Added ask endpoint
- to get a question based on lesson id and difficulty (defaults difficulty to EASY)

Added answer endpoint
- to answer a question (identified by session id) with a certain answer
- errors out appropriately if a user tries to answer a question that isn't theirs or session token expired

This is a short summary of how the flow of questions should work (for future reference):
- User requests a question for a certain lesson at a certain difficulty level
- System picks a question from the db, at that difficulty or lower (picking lower difficulty if requested doesn't exist, and picking higher if lower doesn't exist, otherwise NoQuestionsFoundError raised)
- System gets the values defined by the db-defined generators, if any
- System gets the values defined by the custom-function generators, if any
- System replaces variable values in question with values from generators
- System defines any answer choices, as well as the answer itself
- System stores answer, variables, and other details in Redis cache using token:user notation
- System returns the question, the template, the variable values, any answer choices, the question sesson token
User decides to answer question
- User sends a response to the answer endpoint with the session token and answer
- System uses token and user id to fetch right answer from Redis cache
- System verifies if answer is correct or not, adjusts level / level xp
- System logs response and generated question in QuestionHistory table
- System returns correct or incorrect to user, as well as the level / level xp after answering


Note that I only did testing so far on a math question -- as we create more questions, we can write more tests / do test-driven development.
Right now the goal is to make the concept work and build it out from there.

Created a NumberGeneratorConfig for generating random numbers for math equations -> this will help us be consistent.

Decided to use simpify for math expressions, it seems to be a well-supported library that allows us to use variables easily.

Changed the way requirements work to better fit how the monorepo should be built.
- requirements-dev.txt is everything we need for committing / linting + backend
- ./backend/requirements.txt is everything we need for backend
