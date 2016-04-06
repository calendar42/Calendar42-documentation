# oAuth

This page gives an overview of the oAuth 2.0 authorization scenarios that C42 supports, and provides links to more detailed content. For details about using oAuth 2.0 for authentication, see OpenID Connect.

All applications follow a basic pattern when accessing to C42 API using oAuth 2.0:

**Obtain oAuth 2.0 credentials from C42**

  It is required to contact C42 to obtain oAuth 2.0 credentials such as a client *ID* and client *secret*. Both are known by C42 and the application. The set of values changes based on what type of application is being built. E.g. a JavaScript applications do not require a secret, but a web server application does.

  [Request oAuth Access](/rest-api/api-tokens/)

**Obtain an access token from the C42 Authorization Server**

  The user should be sent to the C42 oAuth page with the parameters `service_id`, `grant_type` and `redirect_uri`. There the user will be able to login/register and allow your app to access to his C42 information.

  After the user is successfully logged in, he will be directed to the `redirect_uri` with a `code` as a parameter in the url. That code should then be used to get the actual access token for that user on the C42 platform.

  All over the web different examples about how to consume an API using oAuth can be found.

  We provide of an example made with nodeJS that also includes an extension dubbed "Silent oAuth Authentication": [C42-node-oauth](https://github.com/calendar42/c42-node-oauth)

  Some plain oAuth implementations are:

  * [Java](https://github.com/google/google-oauth-java-client)
  * [Python requests-oauthlib](http://requests-oauthlib.readthedocs.org/)
  * [PHP](https://github.com/thephpleague/oauth2-client)
  * [Ruby](https://github.com/intridea/oauth2)
  * [NodeJS](https://github.com/ciaranj/node-oauth) - used in the C42 example -
  * etc...

**Send the access token to an API**

  The access token retrieved in the previous step needs to be send in the HTTP authorization header with each API request:

  `'Authorization': 'Bearer 9944fake99c62btoken8ad8examplebbdfc6ee4b'`

  It is possible to send tokens as URI query-string parameters, but we **do not recommend it**, as it's considered to be less secure.

**Refresh the access token, if necessary**

  Access tokens have limited lifetimes. If your application needs access to a C42 API beyond the lifetime of a single access token, it can obtain a refresh token. A refresh token allows your application to obtain new access tokens.

> Note: Save your refresh tokens in a **secure** long-term storage and keep using them as long as they remain valid. Limits apply to the number of refresh tokens that are issued per client-user combination, and per user across all clients, and these limits are different. If your application requests enough refresh tokens to go over one of the limits, older refresh tokens stop working.

## Scopes

Scopes let you to specify exactly what type of access you need. Scopes limit access for oAuth tokens. They do not grant any additional permission beyond that which the user already has.

For the web flow, requested scopes will be displayed to the user on the authorize form.

| Name        | Description|
| ------------- |:---------:|
| Service.read      | Read all calendars and events related to the user and the service. |
| Service.write      | Read *and modify* all calendars and events related to the user and the service. |

> Note: The list of scopes will grow as soon they will be available from the C42 oAuth authentication.

**Which scope(s) should I use?**

| Need        | Scope(s) |
| ------------- |:---------:|
| Access to the service related calendars and events, but not modify it. | Service.read |
| Access to the service related calendars and events and modify it. This scope provides of read and write access     | Service.write|

## Scenarios

**Web server applications**

The C42 oAuth 2.0 endpoint supports web server applications that use languages and frameworks such as PHP, Java, Python, Ruby, and ASP.NET.

For that the app needs to be registered on the C42 platform.

For security reasons:

* The service CAN ONLY access user data created inside the service.
* The service CAN NOT act as the email address towards other users.

As soon as the service wants to do any of the above, the user needs to approve the relation between his email and the service. This verification can be implicitly triggered based on actions of the user (e.g: sharing an event) or explicitly by the service

> If any of the above list requirements are not covered or a non accepted action is triggered the API would respond with an error code to notify the app that it should ask the user for a service verification.

## Silent oAuth Authentication

**Silent oAuth Authentication is a C42 specific extension to the oAuth standard in order to allow applications to store C42 data in relation to a certain email-address without requiring any user interaction to confirm. As no user-interaction is required, multiple limitations to the usage are set in place. In actual usage, the flow only adds one parameter to the request of the access_token: `email_address`.**

**Purpose**

This silent flow enables applications to offer *Personal* C42 Planning & Mobility services to their end-users without requiring any explicit user acceptance by their users. It allows to store and retrieve user related planning data in a "C42 Data Sandbox" that is related to an email address and your C42 service, ready to be enriched with services like automatic trip-suggestions or automatic check-ins.

As this "C42 data sandbox" can be created and accessed through a small tweak to the oAuth 2.0 specification, it is easy to integrate based on the large set of existing oAuth 2.0 libraries. All you need to provide is the email address of a user, that is used as identifier of the service related sandbox.

**limitations**

In order to make the silent oAuth flow secure without any explicit user interaction, several limitations are in place:

Limitations on creation of a Sandbox

* A "C42 Data Sandbox" will ONLY be created if:
  * The email address is NOT related to an activated account in C42
  * The email address is NOT related to any account that is related to the service that requests the Sandbox (e.g. a service admin)
* If no Sandbox can be created due to the reasons above, an error will be returned, and the regular non-silent oAuth flow will need to be presented to the user

Limitations on allowed actions to perform
* The service CAN ONLY create data in the Sandbox and retrieve (enriched) data from this same Sandbox
* As the email address is not verified by the user, the service can't act in name of the user towards other users:
  * The CAN NOT share data (e.g. add event subscriptions to the created data)
  * All data of a user will be contained in the Sandbox

These limitations can be removed by letting the user related to the email address go through the regular oAuth flow, with it verifying their mail and explicitly accepting the access to the data again. C42 will then merge the earlier created Data Sandbox into the active user Data.

**Usage**

To trigger the *Silent oAuth Authentication* process, it is required to send the `email_address` and one of the service scopes when the access token is requested for the very first time. The token received will be a service restricted token.

A registered oAuth App related to a Service requests the following:

```
https://calendar42.com/oauth2/authorize?email_address=someone@somesite.com&app=&token=&scope=...
```

Different actions can be expected based on the current status of the email_address used to request authorization:

| Status         | Performed action |
| ------------- |:---------:|
| email_address is **not** related to a user with an (in)active service-subscription to the service | SUCCESS: Creation of a sandbox user and subscribe it to the service of the oauth application |
| email_address is related to a user with an (in)active service-subscription to the service          | ERROR: Access to normal oAuth flow |
| Scope requested is a full scope, not just service                                            | ERROR: Access to normal oAuth flow |

> In all cases the service will be checked to verify that this app is registered and have access to the requested scopes

Despite this process doesn't require of any user action, it is **REQUIRED** to perform the oAuth through the browser.
In the case that no user action is required, a solution would be:

1. After to successfully log in in the app, redirect to the C42 oAuth login page, requesting in this way of the authorization.
1. Preform all required redirections to finalize the authorization to our servers.
1. On success redirect to the logged in page, where the token will be used to proceed of all actions to the C42 API.

In this case the Silent oAuth flow only impacts the user experience minimally by offering a slightly longer response time from the login page.
Different options are:

* showing a loader with a message explaining which actions are happening in the background.
* (in a Native app) opening a Web-view off-screen and making this process totally invisible for the user.

# Error responses (WIP)

**Authentication errors (WIP)**

All calls received with a wrong Token or clientID will be answered with a `403` code status.
