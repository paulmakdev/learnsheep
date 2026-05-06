# ADR-00008: Updating auth and adding me and stat endpoints.

## Status
Accepted

## Summary
Added refresh token logic to auth. Added stat endpoints for things like lesson history (progress). Added me endpoint for login verification + display name.

## Decision
Decided to incorporate refresh token logic into our singular JWT access token.
- Having two tokens is hard to keep track of
- No one should be generating API access outside of regular app use
- Everything we want in a refresh token is there, i.e. max amount of time before required login again
- Allows for instantaneous revocation
    - Only con with instantaneous revocation is it requires us to have a semi-stateful auth system
        - However, I believe that where current devices are logged in could spark curiosity in the user to learn more about auth & will help track sessions for the user

Added tests for access revocation, refreshing access, and proper access expiration.

Decided to use session ids for internal tracking of access tokens (to not take up much space).

Added set logic to cache for easy storing of session ids.

Added logic so that we store device information and login time with session ids in the cache
- Easier for user to revoke access
- User can see exactly who is logged in and for how long -- we want the user to be able to keep track of information like this in case they find something fishy, promotes sense of security

Decided to create a function that generates public session ids and links them to private session ids internally when a user requests it
- Allows us to keep our internal logic separate, while still having unique session ids

## Future Decisions
Do we add DB logging for sessions? Do we care? Will this help us with analysis, or better yet, security analysis?
