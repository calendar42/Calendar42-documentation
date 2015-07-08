Event Subscriptions are resources describing the relationship between Users and Events in the system.

This relationship might be be based on one or more relations:

* Indirect relations through calendars: The user is related to the Event as a result of the Event being in one ore more Calendars that the user is subscribed to.
* Direct relations: The user is directly related to the Event, without any Calendar in between

Within this relational structure, the Event Subscriptions represent the summary of these different relations. 

* [Model Schema](#model-schema) - overview of the Event Subscription Model with detailed fields
* [GET](#get) - to retrieve a set of Event Subscriptions
* [POST by User ID](#post-by-user-id) -  to relate an existing C42 User to an Event by id
* [POST by phone number/ email ](#post-by-phone-number-email) - to relate a new User to an Event by email or phone number
* [PUT](#put) - to replace the relation between a User and an Event
* [PATCH](#patch) - to update the relation between a User and an Event (e.g. the access rights)
* [DELETE](#delete) - to remove the relation between a User and an Event

## Model Schema

```javascript
    {
        "id": string,                       # read only
        "event_id": string,                 # write only on POST
        "subscriber": {
            "first_name": string,           # read only
            "last_name": string,            # read only
            "id": string,                   # write
            "email": string,                # write
            "phone_number": string          # write
        },
        "is_invitation": boolean,           # write
        "permission": permission,           # write
        "actor":   {
            "first_name": string,           # read only
            "last_name": string,            # read only
            "id": string                    # read only
        },
        "message": string,                  # write only on POST
        "created": datetime,                # read only
        "calendar_ids": array,              # @todo
        "rsvp_status": rsvp_status          # @todo
    }
```

* **Event Subscription specific fields**
    * `subscriber`
        * Specifies the user that is subscribed to the event
        * Described by user_id, first_name and last_name
        * first_name and last_name are overwritten by any existing known values in the system
    * `is_invitation`
        * Determines whether the subscriber is expected to respond with setting an rsvp status
        * When a subscription is created with is_invitation is `true`, the rsvp_status will automatically be set to `not_replied`
        * When a subscription is created with is_invitation is not set or `false`, the rsvp_status will not be set automatically
    * `actor`
        * Specifies the user that created the subscription, is set automatically by the system upon creation
    * `message`
        * Specifies the private message set by the creator
        * Will only be returned to the subscriber specified and the actor. Not to any other users that have access to the subscription
    * `calendar_ids`
        * Specifies through which calendars (if any), the subscriber is related to the event.
        * A user might for instance have access to one event through to calendars: the event is then within two calendars to which the subscriber both has access to.
    * `permission`
        * The permission reflects the summary of the permission based on the direct and indirect relations between the user and the event.
        * The permission is calculated as follows:
            * If there is a direct relation, the permission of this relation always overrules
            * Otherwise the highest permission of the indirect relations is returned (write > read & subscribed > invited)


* **Contants used:**
    * [permission](rest-api/constants/#permission)
    * [rsvp_status](rest-api/constants/#rsvp-status)

## GET

To retrieve a set of Event Subscriptions

* **Supported Filters**:
    * service_ids       = `[{service_id},]`
    * event_ids         = `[{event_id},]`
    * subscriber_ids    = `[{user_id},]`
    * sync_token        = `{sync_token}`
    * calendar_ids      = `[{calendar_id},]`
    * rsvp_status       = `{rsvp_status}`
* **Supported Ordering**:
    * order_by=creation_date
    * order_by=sync_token
* **Unordered and unfiltered**
    * When not sending along any filters or ordering, all subscriptions are returned that belong to Events you have access, ordered by creation date.

```
@todo: Add more information about the different filters
```

**Example Request to /event-subscriptions:**

```javascript
    // response to GET: /event-subscriptions
    {
        "data": [
            {
                "id": "42abc42def42ghi_42abc42de",
                "event_id": "42abc42def42ghi",
                "subscriber": {
                    "first_name": "Ella",
                    "last_name": "Bartledan",
                    "user_id": "42abc42de"
                },
                "is_invitation": true,
                "permission": "invited_read",
                "actor":   {
                    "first_name": "Arthur",
                    "last_name": "Dent",
                    "user_id": "42abc42def42ghi"
                },
                "message": "Are you coming to the end of the universe?",
                "created": "2042-02-12T15:19:21:00.000000Z",
                "calendar_ids": [],
                "rsvp_status" "not_replied"
            }
        ],
        "meta_data": {
            "sync_token": 142,
            "count": 2,
            "offset": 0
        }
    }
```

**Examples of using filters and ordering**

* Synchronizing any missed event subscriptions based on the sync token
    * `GET: /event-subscriptions?sync_token=42&order_by=sync_token`
* Retrieving all the Event Subscriptions of a single user
    * `GET: /event-subscriptions?subscriber_ids=[42abc42de]`

```
@todo: Add more examples
```

## POST [ by user id ]

To subscribe a user to an event an Event.

**Example Request Payload - POST: /event-subscriptions**

```javascript
    {
        "event_id": "42abc42def42ghi",
        "subscriber": {
            "user_id": "42abc42de"
        }
        "is_invitation": true,
        "permission": "member_write",
        "message": "Want to meet up?",
    }
```

Success Response:

```javascript
    {
        "data": [
            {
                "id": "42abc42def42ghi_42abc42de",
                "event_id": "42abc42def42ghi",
                "subscriber": {
                    "first_name": "",
                    "last_name": "",
                    "user_id": "42abc42de"
                }
                "is_invitation": true,
                "permission": "member_write",
                "actor":   {
                    "first_name": "Arthur",
                    "last_name": "Dent",
                    "user_id": "42sdf42sd"
                },
                "message": "Want to meet up?",
                "created": "2042-02-12T15:19:21:00.000000Z",
                "calendar_ids": [],
                "rsvp_status" "not_replied"
            }
        ],
        "meta_data": {
            "sync_token": 142
        }
    }
```

Error Responses:

```javascript
    # Not authorized
    {
      "error": {
        "status_code": 404,
        "message": "...",
        "code": "..."
      }
    }

    # ...

```

**Notes on posting Event Subscriptions**

* First name and last name can be set, but are overruled by the system if the first and last name are already set by the user related to the user_id.


## POST [ by phone number/ email ]

An Event Subscription can contain both an email and a phonenumber. In our platform a email and phonenumber con be connected to one single user the moment they are verified by the same user. After this verification, adding a subscription to either the phone number or the mail address will result in the same subscription towards the same user.

```
@todo: Add more information about how we deal with the subscription id, after people merge there accounts.
```
```
@todo: Add more information about how we deal with the passed along first and last names.
```

**Example Request Payload - POST: /event-subscriptions**

```javascript
    // by phone number
    {
        "event_id": "17171771717171717717171_2a98898b9892",
        "subscriber": {
            "first_name": "Ella",
            "last_name": "Bartledan",
            "phone_number" "0031612345678",
        }
        "is_invitation": true,
        "permission": "invited_read",
    }
    // by email
    {
        "event_id": "17171771717171717717171_2a98898b9892",
        "subscriber": {
            'first_name': 'Ella',
            'last_name': 'Bartledan',
            'email': 'ella@bartledan.com',
        }
        "is_invitation": true,
        "permission": "invited_read",
    }
```

The Success Response is similar to the when creating an Event Subscription by user_id, except that the subscriber will be extended with a server-side generated id.

Error responses are also be similar.


**Notes on merging of accounts**

Merged user/subscription after the user has verified his phonenumber and email-address:

When the user verified his email and phonenumber the subscriptions will be merged and result in a single subscription.

Subscription object after email and phonenumber vefification
```javascript
{
    "data": [
        {
            
            // ...

            "subscriber": {
                "id": "34jnlk45j44bn2",
                'first_name': 'Jaap',
                'last_name': 'de Vries',
                'email': 'devries@example.com',
                'phonenumber': 0031612345678,
            }

            // ...

        }   
    ],
    "meta_data": {

        // ...
        
    }
}
```

## PUT

* Used to completely replace someones subscription

**Example Request Payload - PUT: /event-subscriptions/{event_subscription_id}**

```javascript
  {
        "event_id":"42abc42def42ghi"
        "subscriber": {
            "user_id": "42abc42de"
        }
        "is_invitation": true,
        "permission": "member_write",
        "message": "A new message",
    }
```

```javascript
# Success Response
    # Same full object as on POST
```

```javascript
# Error Response
    # Same errors as on POST
```


## PATCH

* Used to change someones rights on an event
```
@todo: Used to change someones rsvp to an event?
```
```
@todo: Used to change through which calendars someone is related to an event?
```

**Example Request Payload - PATCH: /event-subscriptions/{event_subscription_id}**

```javascript
    # Change the rights of a user
    {
        "permission": "member_read",            # permission_type [write]
    }
```

Success & error responses are similar as POST

## DELETE

* Used to remove someone from a subscription

**Example Request - DELETE: /event-subscriptions/{event_subscription_id}**

* `DELETE /event-subscriptions/42abc42def42ghi_42abc42de`

Success Response

```javascript
    // Empty response: 204
```

Error Response similar to POST
