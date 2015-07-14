# REST API Introduction

Using our [REST](http://en.wikipedia.org/wiki/Representational_state_transfer) API, you can make Calendar42 do pretty much anything planning related you want. The only thing left to do for you is showing up!

## Request an API token

Request an [API Token](/rest-api/api-tokens/) to start developing!

## Authenticate

Our authentication scheme uses a simple token-based HTTP Authentication scheme. For clients to authenticate, the token key should be included in the `Authorization` HTTP header. The key should be prefixed by the string literal `Token`, with whitespace separating the two strings. For example:

* `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`

Tokens are one-on-one related to users on our platform. The data that is accessible with these tokens is thus also related to the relationships this user has to services, calendars and events. 

## References

* [Usage](/rest-api/usage/)
* [Constants](/rest-api/constants/)
* [Objects](/rest-api/objects/)
* [Endpoints](/rest-api/endpoints/)

## Interactive documentation

* [Interactive API documentation](https://calendar42.com/api)
