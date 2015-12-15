# oAuth

C42 Platform allows to use OAuth 2.0 protocol to authenticate. C42 supports common OAuth 2.0 scenarios such as those for web server, installed, and client-side applications.

This page gives an overview of the OAuth 2.0 authorization scenarios that C42 supports, and provides links to more detailed content. For details about using OAuth 2.0 for authentication, see OpenID Connect.

All applications follow a basic pattern when accessing to C42 API using OAuth 2.0:

1. Obtain OAuth 2.0 credentials from C42.

  It is required to contact C42 to obtain OAuth 2.0 credentials such as a client *ID* and client *secret*. Both are known by C42 and the application. The set of values changes based on what type of application is being built. E.g. a JavaScript application does not require a secret, but a web server application does.

  [Request OAuth Access](/rest-api/api-tokens/)

1. Obtain an access token from the C42 Authorization Server:

  To get the access token is required to make a request to C42 servers with the `service_id`, `grant_type` and `redirect_uri`.

  With that call the user will be redirected to the `redirect_uri` with a code as a parameter in the url. That code is the one that should be used to get the access token.

  Internet is a very good place to find different examples about how to consume an API using the oAuth authentication system.

  We provide of an example made with nodeJS: [c42-node-oauth](https://github.com/calendar42/c42-node-oauth)

  Some other examples found in the net:

  * [Java](https://github.com/google/google-oauth-java-client)
  * [python-oauth2](https://github.com/joestump/python-oauth2)
  * [PHP](https://github.com/thephpleague/oauth2-client)
  * [Ruby](https://github.com/intridea/oauth2)
  * [NodeJS](https://github.com/ciaranj/node-oauth) - used in the c42 example -
  * etc...

1. Send the access token to an API:

  After an application obtains an access token, it sends the token to the C42 API in the HTTP authorization header. It is possible to send tokens as URI query-string parameters, but we don't recommend it, because URI parameters can end up in log files that are not completely secure. Also, it is good REST practice to avoid creating unnecessary URI parameter names.

  `'Authorization': 'Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'`

  Access tokens are valid only for the set of operations and resources described in the scope of the token request. For example, if an access token is issued for the C42 API, it does not grant access to the C42 Contacts API. You can, however, send that access token to the C42 API multiple times for similar operations.

1. Refresh the access token, if necessary.

  Access tokens have limited lifetimes. If your application needs access to a C42 API beyond the lifetime of a single access token, it can obtain a refresh token. A refresh token allows your application to obtain new access tokens.

> Note: Save refresh tokens in secure long-term storage and continue to use them as long as they remain valid. Limits apply to the number of refresh tokens that are issued per client-user combination, and per user across all clients, and these limits are different. If your application requests enough refresh tokens to go over one of the limits, older refresh tokens stop working.

# Silent oAuth Authentication

The C42 oAuth system allows to obtain the access token using a `slient flow`.
It means that the user doesn't need to accept the service and the service can't use the information of the user but all created data by the service.

What is happening in the background is that we are creating a 'sandbox user' for that service with a restricted access to information.

Later the user can merge his information allowing the service access it's old and future information. To do that, will be required the user service acceptance.

To trigger the *oAuth silent authentication* process, is required to send the `email_address` when the access token is requested for the very first time. The token received will be a service restricted token.

To switch to the 'normal access token' will be required to trigger the normal oAuth flow, where the user need to accept the service.

## Scopes (WIP)

Scopes let you to specify exactly what type of access you need. Scopes limit access for OAuth tokens. They do not grant any additional permission beyond that which the user already has.

For the web flow, requested scopes will be displayed to the user on the authorize form.

| Name        | Description|
| ------------- |:---------:|
| Service.read      | Read all calendars and events related to the user and the service. |
| Service.write      | *Read* and modify all calendars and events related to the user and the service. |
| ...      | ... |

> The list of scopes will grow as soon they will be available from the C42 oAuth authentication.

## Which scope(s) should I use?

| Need        | Scope(s) |
| ------------- |:---------:|
| Access to the service related calendars and events, but not modify it. | Service.read |
| Access to the service related calendars and events and modify it. This scope provides of *read* and write access     | Service.write|
| ... | ... |

## Scenarios

### Web server applications

The C42 OAuth 2.0 endpoint supports web server applications that use languages and frameworks such as PHP, Java, Python, Ruby, and ASP.NET.

We allow app developer to manage user data using an email as initial starting point without user interaction by adding the email_address as a parameter in the first oAuth call.

For that is required to accomplish the following requirements:

* The app needs to be registered on the C42 platform
* The email should be sent along in the call in the email_address parameter in the url.
* The email shouldn't belong to a user that has an active service subscription to the service.

For security reasons a Service is only allowed to manage planning of that email, as long as:

* The service CAN ONLY access user data created inside the service.
* The service CAN NOT act as the email address towards other users.

As soon as the service wants to do any of the above, the user needs to approve the relation between his email and the service. This verification can be implicitly triggered based on actions of the user (e.g: sharing an event) or explicitly by the service

> If any of the above list requirements are not covered or a non accepted action is triggered the API would respond with an error code to notify the app that it should ask the user for a service verification.

## Technical implementation

By sending along an email_address param the oAuth flow can result in a flow that doesn't require any user interaction but still results in a user with which the app can manage data for that user.
A registered oAuth App related to a Service requests the following:

```
https://calendar42.com/oauth2/authorize?email_address=someone@somesite.com&app=&token=&scope=...
```

Different actions would be performed based on the current status of the email_address used to request authorization:

| Status         | Performed action |
| ------------- |:---------:|
| email_address is not in C42 | (WIP) |
| email_address is related to inactive user in C42 | (WIP) |
| email_address is related to active user in C42 | (WIP) |
| email_address is related to an inactive ServiceUser of service already (also diff app)    | (WIP) |
| email_address is related to user with an (in)active service-subscription to service         | Access to normal oAuth flow |
| Scope requested is a full scope, not just service                                            | Forbidden |

> In all cases the service will be checked to verify that this app is registered and have access to the requested scopes

Despite this process doesn't require of any user action, it is REQUIRED to perform the oAuth through the browser.
In the case that no user action is required, a solution would be:

1. After to successfully log in in the app, redirect to the C42 oAuth login page, requesting in this way of the authorization.
1. Preform all required redirections to finalize the authorization to our servers.
1. On success redirect to the logged in page, where the token will be used to proceed of all actions to the C42 API.

In this case the user experience could be a 'longer' response time from the login page.
Different options are available like showing a loader with a message explaining which actions are happening in the background.
In a Smartphone Native app a Web-view can be opened in the background and make this process totally invisible for the user.

## Error responses (WIP)

### Authentication errors (WIP)

All calls received with a wrong Token or clientID will be answered with a `403` code status.
