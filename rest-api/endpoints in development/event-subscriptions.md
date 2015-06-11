**NOTE: This Endpoint is currently under development**

Event Subscriptions are resources describing the relationship between Users and Events in the system.

**Contants used:**

* permission: http://docs.calendar42.com/en/latest/rest-api/constants/#permission

## Retrieve Event Subscriptions objects

To know who was planned in on a event the /event-subscriptions end-point is used.

Subscription request can be filtered on:

* service_ids       = [{service_id},]
* event_ids         = [{event_id},]
* subscriber_ids    = [{user_id},]
* sync_token        = {sync_token}
* calendar_ids      = [{calendar_id},]
* rsvp_status       = [{rsvp_status}]

@todo: Add more information about the different filters

### GET /event-subscriptions

* Used to retrieve all Event Subscriptions

#### GET /event-subscriptions/

```javascript
# response
    {
        "data": [
            {
                "event_id": string,                 # write only on POST
                "subscriber": {                     # => person object
                    "first_name": string,           # read only
                    "last_name": string,            # read only
                    "user_id": string               # write
                },
                "is_invitation": true,              # write
                "permission": permission,           # write
                "actor":   {                        # => person object
                    "first_name": string,           # read only
                    "last_name": string,            # read only
                    "user_id": string               # read only
                },
                "message": string,                  # write only on POST
                "created": date,                    # read only
                "calendar_ids": array               # @todo
                "rsvp_status" rsvp_status           # @todo
            }
        ],
        "meta_data": {
            "sync_token": 142,
            "count": 2,
            "offset": 0
        }
    }
```

@todo: Add more information about the different fields

## Manage Event Subscriptions by user id

To add a user to an event an Event Subscription should be created.

### POST /event-subscriptions [by user id]

* Used to invite someone to an event

```javascript
# Request Payload on /event-subscriptions
  {
        "event_id": "42abc42def42ghi",            # string [write only on POST]
        "subscriber": {
            "user_id": "42abc42de"          # string [write]
        }
        "is_invitation": true,              # boolean [write]
        "permission": "member_write",       # permission_type [write]
        "message": "Want to meet up?",      # string [write only on POST]
    }
```

```javascript
# Success Response
    {
        "data": [
            {
                "id": "42abc42def42ghi_42abc42de",  # string [read only]
                "object": {
                    "object_type": "event",         # string [write only on POST]
                    "id": "42abc42def42ghi",        # write only on POST
                }
                "subscriber": {                     # => person object
                    "first_name": string,           # read only
                    "last_name": string,            # read only
                    "user_id": string               # write
                }
                "is_invitation": true,              # write
                "permission": permission,           # write
                "actor":   {                        # => person object
                    "first_name": string,           # read only
                    "last_name": string,            # read only
                    "user_id": string               # read only
                },
                "message": string,                  # write only on POST
                "created": date,                    # read only
            }
        ],
        "meta_data": {
            "sync_token": 142
        }
    }
```

```javascript
# Error Responses

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

### PATCH /event-subscriptions/{event_subscription_id} [by user id]

* Used to change someones rights on an event
* @todo: Used to change someones rsvp to an event?
* @todo: Used to change through which calendars someone is related to an event?

```javascript
# Request Payload on /event-subscriptions/{event_subscription_id}
    # Change the rights of a user
    {
        "permission": "member_read",            # permission_type [write]
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

#### PUT /event-subscriptions/{event_subscription_id} [by user id]

* Used to completely replace someones subscription

```javascript
# Request Payload on /event-subscriptions/{event_subscription_id} 
  {
        "object": {
            "object_type": "event"          # object_type [write only on POST]
            "id": "42abc42def42ghi",        # string [write only on POST]
        }
        "subscriber": {
            "user_id": "42abc42de"          # string [write]
        }
        "is_invitation": true,              # boolean [write]
        "permission": "member_write",       # permission_type [write]
        "message": "A new message",         # string [write only on POST]
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

#### DELETE /event-subscriptions/{event_subscription_id} [by user id]

* Used to remove someone from a subscription

```javascript
# Request
  DELETE /event-subscriptions/42abc42def42ghi_42abc42de
```

```javascript
# Success Response
    # Empty response: 204
```

```javascript
# Error Response
    # Same errors as on POST
```


### Add subscriptions by phone number or email

An Event Subscription can contain both an email and a phonenumber. In our platform a email and phonenumber con be connected to one single user the moment they are verified by the same user. After this verification, adding a subscription to either the phone number or the mail address will result in the same subscription towards the same user.

@todo: Add more information about how we deal with the subscription id, after people merge there accounts.
@todo: Add more information about how we deal with the passed along first and last names.

#### POST subscription [by phone/email]

```javascript
    # by phone number
    {
        "object": {
            "object_type": "event",
            "id": "17171771717171717717171_2a98898b9892",
        }

        "subscriber": {
            'first_name': 'Jaap',
            'last_name': 'de Vries',
            'phone_number' '0031612345678',
        }

        "is_invitation": true,
        "permission": "invited_read",
    }
    # by mail
    {
        "object": {
            "object_type": "event",
            "id": "17171771717171717717171_2a98898b9892",
        }

        "subscriber": {
            'first_name': 'Jaap',
            'last_name': 'de Vries',
            'email': 'devries@example.com',
        }

        "is_invitation": true,
        "permission": "invited_read",
    }
```

#### The JSON response

```javascript
{
    "data": [
        {
            "id": "2j3lk324b34kjn334n3ln4ljkn34kn3",

            "object": {
                "object_type": "event",
                "id": "17171771717171717717171_2a98898b9892",
            }

            "creator": {
                "id": "slkdjfln22l3219h3b32",
                "first_name": "Service API",
                "last_name": "User name",
            }

            "subscriber": {
                "id": "34jnlk45j44bn2",
                'first_name': 'Jaap',
                'last_name': 'de Vries',
                'email': 'devries@example.com',
                'phonenumber': null,
            }

            "is_invitation": true,
            "rsvp_status": "not_replied",
            "permission": "invited_read",
        },
        {
            "id": "2lkj3ln34lkjm34bn4lnm34n34",

            "object": {
                "object_type": "event",
                "id": "17171771717171717717171_2a98898b9892",
            }

            "creator": {
                "id": "slkdjfln22l3219h3b32",
                "first_name": "Service API",
                "last_name": "User name",
            }

            "subscriber": {
                "id": "sdlkjflsndfkbnkj2",
                'first_name': 'Jaap',
                'last_name': 'de Vries',
                'email': null,
                'phonenumber': '0031612345678',
            }

            "is_invitation": true,
            "rsvp_status": "not_replied",
            "permission": "invited_read",
        }        
    ],
    "meta_data": {}
}
```


## Merged user/subscription after the user has verified his phonenumber and email-address:

When the user verified his email and phonenumber the subscriptions will be merged and result in a single subscription.

### Subscription object after email and phonenumber vefification
```javascript
{
    "data": [
        {
            "id": "2j3lk324b34kjn334n3ln4ljkn34kn3",

            "object": {
                "object_type": "event",
                "id": "17171771717171717717171_2a98898b9892",
            }

            "creator": {
                "id": "slkdjfln22l3219h3b32",
                "first_name": "Service API",
                "last_name": "User name",
            }

            "subscriber": {
                "id": "34jnlk45j44bn2",
                'first_name': 'Jaap',
                'last_name': 'de Vries',
                'email': 'devries@example.com',
                'phonenumber': 0031612345678,
            }

            "is_invitation": true,
            "rsvp_status": "attending",
            "permission": "invited_read",
        }   
    ],
    "meta_data": {}
}
```