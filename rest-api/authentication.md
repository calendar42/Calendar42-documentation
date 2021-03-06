## User Token

**Authentication**

C42 provides of user related tokens. This tokens allow the app or user to have access to all information related to a certain user.

[Request User Token](/rest-api/api-tokens/)

**Authorization**

User Tokens give access to the data through the relationships the user has to services, calendars and events, the user needs to be active.

It should be added in the `Authorization` HTTP header under the `Token` tag. E.g:

`'Authorization': 'Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'`

## Action Token

**Authentication**

C42 provides of action related tokens. This tokens are similar as User Tokens in behavior, but the scope is based on the endpoints were the token have access to.

[Request Action Token](/rest-api/api-tokens/)

**Authorization**

  Server Tokens give access to the data through the relationships the user has to services, calendars and events.

The Token needs to be added in the `Authorization` HTTP header under the `ActionToken` tag. E.g:

`'Authorization': 'ActionToken 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'`

To use this type of token the user **needs** to be **active**.

Server Tokens should **not** be shared or embedded in web-apps.

## oAuth

**Authentication**

C42 Platform allows to use OAuth 2.0 protocol to authenticate. C42 supports common OAuth 2.0 scenarios such as those for web server, installed, and client-side applications.

This process requires the acceptance of the user as the app can have access to the information is aiming for.

[Request App oAuth Access](/rest-api/api-tokens/)

**Authorization**

The oAuth authorization process allows an *App* to have access to user information.
What defines the scope of this app is the service where the app is registered to.

To have more information about scopes, as implementation of an oAuth authentication and authorization process check our [oAuth-authorization](/rest-api/oAuth-authorization) page.

## Silent oAuth

**Authentication**

C42 Platform allows to use OAuth 2.0 protocol to authenticate in a *silent* way.
It means the user is not requested to accept the rights the app will have and the app won't have access to any data that is not created by the app or under the service the app is related to.

[Request App oAuth Access](/rest-api/api-tokens/)

**Authorization**

The Silent oAuth authorization process allows an *App* to have access to the information of a **sandBox** user.

A sandBox user have a closed environment, and the information that can be managed on it is only the one is created in that sandBox. In this way the application that makes use of this authentication method will never have access to the information the user created by it's own before or after.

The only way for the application to have access to this information is by getting user authorization through the normal oAuth Authentication process, where the user explicitly allows the app access to his information.

As in the normal oAuth process, what defines the scope of this app is the service where the app is registered to.

For more information about scopes, implementation and authorization process check our [oAuth-authorization](/rest-api/oAuth-authorization) documentation page.
