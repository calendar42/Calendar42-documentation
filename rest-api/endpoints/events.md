
Supported methods:

* GET `acceptation`
* POST `development`

### GET: /events/

* Returns a default response object with a list of [Event](/rest-api/objects/#event) objects inside the data object.

#### Parameters

Parameter | Required | 
:--- | :--- | :---
`ids` | false | Array of event ids. To filter on specific events (reponse is not equally ordered)
`service_ids` | false | Array of service ids to filter on. Note: still only returns events the requester has access to.
`calendar_ids` | false | Array of calendar ids <br> Supports the `or` operator
`event_types` | false | Array of [Event Types](/rest-api/constants/#event-type)
`geo_circles` | false | Array of [Geo Circles](#geo-circle)
`length` | false | Length in meters of event types arrive_by, depart_from and route. <br>Supports `lt` and `gt` operators
`order_by` | false |  "sync_token", "due", "distance" (only when exactly one geo_circle is passed along)
`sync_token` | false | [Sync Token](/rest-api/usage/#sync-token)
`order_asc` | false | true (default), false. Whether to order in ascending or descending order
<br>

#### Examples

**Ordering**: Get events belonging to a certain calendar within a certain geographic range, orderder by distance:

* ``/events/?calendar_ids=[abc123]&geo_circles=[(52.28297176 5.27424839 5000)]&order_by=distance``

**Operators**: Get trips longer than 15km, that are in either calendar 'abc1' or calendar 'abc2'

* ``/events/?event_types=[arrive_by,depart_from]&length__gt=15000&calendar_ids__or=[abc1,abc2]``

**Synchronisation**: Get events that changed since last retrieval

* ``/events/?sync_token=128973981273``

---------------------------------------

### POST: /events/

Editable attributes of the [Event Model](/rest-api/objects/#event) can be sent in as an object to create a new Event resource. 

Upon successful creation, the returned event resource **WILL** be modified:

1. It **WILL** contain a new generated id
2. It **WILL** be extended with several attributes and their default values
  * Examples here are `sync_token`, `event_type`, `permission`, `created`, `modified` & `creator`
3. Its location data **COULD** be enriched to contain more specific location data
  * **Geocoding**: The posted event contains one or more locations without geo-position. The geo-position **COULD** be added based on location text, city, address and postcode.
  * **Reverse geocoding**: The posted event contains one or more locations with only geo-positions. Location text, city, address and postcode **COULD** be added.

See [the interactive Swagger Event API documentation for supported fields](http://calendar42.com/app/django/api/docs/#!/v2/Event_Api)

#### Example

##### Most minimal creation in the form of a todo

The most minimal event consists of todo, as 'normal' events (the default event type) requires start, end, start_timezone and end_timezone to be set.

This example shows clearly which fields are being defaulted and which are being send back empty.

This todo will then off course will not have any context related to it, not in the form of content (eg. title or description), nor in the form of calendar relations.

```javascript
    // postdata
    {
        "event_type": "todo"
    }
```

```javascript
# Response (including automatically generated and defaulting fields)
    {
        "data": [
            {
              # ORIGINAL FIELD
                "event_type": "todo",
              # AUTOMATICALLY GENERATED FIELDS
                "id": "897dsah8789had897had873b4",
                "created": "2015-02-12T15:19:21:00.000000Z",
                "modified": "2015-02-12T15:19:21:00.000000Z",
                "sync_token": 142,
                "creator": {
                    "id": "987jbkhjasd7563ghjva78",
                    "first_name": "Your",
                    "last_name": "Name"
                },
              # AUTOMATICALLY DEFAULTING FIELDS
                "permission": "subscribed_write",
                "calendar_ids": [],
              # EMPTY FIELDS
                "previous_permission": null,
                "is_suggestion": null,
                "is_invitation": null,
                "invitation": null,
                "rsvp_status": null,
                "start": null,
                "end": null,
                "start_timezone": null,
                "end_timezone": null,
                "all_day": null,
                "title": null,
                "description": null,
                "color": null,
                "logo": null,
                "source_url": null,
                "start_location": null,
                "end_location": null,
                "recurrence": null,
                "recurrence_parent": null,
                "related_event": null,
                "trip": null,
                "length": null
            }
        ],
        "meta_data": {
            "sync_token": 142
        }
    }
```

##### Creating a simple event into a calendar

This example shows a regular usecase, where an event is created in one of the accessible calendars, together with a title and a description.

* The `event_type` will default to `normal`
* `normal` events require `start` and `end` to be set
* These dates require their timezones to be set with `start_timezone` and `end_timezone`

```javascript
    // postdata
    {
        "calendar_ids": ["42b42b42b42b42b42b42b42b42b42b42b42b42b4"],
        "start": "2015-02-12T15:00:00:00.000000Z",
        "start_timezone": "Europe/Amsterdam",
        "end": "2015-02-12T15:30:00:00.000000Z",
        "end_timezone": "Europe/Amsterdam",
        "title": "Nice title",
        "description": "A nice description",
    }
```

```javascript
# Response, including automatically generated and defaulting fields
    {
        "data": [
            {
              # ORIGINAL FIELDS
                "id": "897dsah8789had897had873b4",
                "calendar_ids": ["42b42b42b42b42b42b42b42b42b42b42b42b42b4"],
                "start": "2015-02-12T15:00:00:00.000000Z",
                "start_timezone": "Europe/Amsterdam",
                "end": "2015-02-12T15:30:00:00.000000Z",
                "end_timezone": "Europe/Amsterdam",
                "title": "Nice title",
                "description": "A nice description",
              # AUTOMATICALLY DEFAULTING FIELDS
                "event_type": "normal",
                "permission": "subscribed_write",
              # EMPTY FIELDS
                "previous_permission": null,
                "is_suggestion": null,
                "is_invitation": null,
                "invitation": null,
                "rsvp_status": null,
                "all_day": null,
                "color": null,
                "logo": null,
                "source_url": null,
                "start_location": null,
                "end_location": null,
                "recurrence": null,
                "recurrence_parent": null,
                "related_event": null,
                "trip": null,
                "length": null
            }
        ],
        "meta_data" : {
            "sync_token": 143
        }
    }
```

##### Special case: Event creation with location id

Prefered way of posting locations in events.

```javascript
    // postdata (partial)
    {
        ...
        "start_location": {
            "id": "789ash9d87a98sdh7987ads",
        }
        ...
    }
```

```javascript
# Response (partial), including id & extended location information
    {
        "data": [
            {
              ...
                "start_location": {
                    "id": "789ash9d87a98sdh7987ads",
                    "text": "Dorpstraat 1, 2600 AE",
                    "address": "Dorpstraat 1",
                    "postcode": "2600 AE",
                    "city": "Delft",
                    "geo": {
                        "latitude": 52.001,
                        "longitude": 4.3065
                    }
                }
              ...
            }
        ],
        "meta_data" : {
            ...
        }
    }
```

##### Special case: Event creation with automatic geocoding

The server will try to perform geocoding when an event is posted that contains a location (either `start_location` or `end_location`) that has no `geo` object. This missing latitude, longitude will then automatically be filled in based on the `text`, or based on the `city`, `address`, `postcode` fields.

```javascript
    // postdata (partial)
    {
        ...
        "start_location": {
            "text": "Dorpstraat 1, 2600 AE",
        }
        ...
    }
```

```javascript
# Response (partial), including id & enriched location
    {
        "data": [
            {
              ...
                "start_location": {
                    "text": "Dorpstraat 1, 2600 AE",
                    "address": "Dorpstraat 1",
                    "postcode": "2600 AE",
                    "city": "Delft",
                    "geo": {
                        "latitude": 52.001,
                        "longitude": 4.3065
                    }
                }
              ...
            }
        ],
        "meta_data" : {
            ...
        }
    }
```


##### Special case: Event creation with automatic reverse geocoding

The server will try to perform reverse geocoding when an event is posted that contains a location (either `start_location` or `end_location`) that has a `geo` object, but misses one of the fields for `text`, `address`, `postcode` or `city`. These missing fields will then automatically be filled in.

```javascript
    // postdata (partial)
    {
        ...
        "start_location": {
            "geo": {
                "latitude": 52.001,
                "longitude": 4.3065
            }
        }
        ...
    }
```

```javascript
# Response (partial), including id & enriched location
    {
        "data": [
            {
              ...
                "start_location": {
                    "text": "Dorpstraat 1, 2600 AE",
                    "address": "Dorpstraat 1",
                    "postcode": "2600 AE",
                    "city": "Delft",
                    "geo": {
                        "latitude": 52.001,
                        "longitude": 4.3065
                    }
                }
              ...
            }
        ],
        "meta_data" : {
            ...
        }
    }
```


## • /events/`<event_id>`/

Supported methods:

* GET `acceptation`
* PUT `development`
* PATCH `development`
* DELETE `development`

### GET: /events/`<event_id>`/

* Returns a default response object with a list containing the requested [Event](/rest-api/objects/#event) object inside the data object.

### PATCH: /events/`<event_id>`/

Any (#events)editable attribute can be sent as a param and it will be replaced with the sended param.

_Using PATCH to subscribe to calendars or unsubscribe from calendars_

    PATCH /events/`<event_id>`/ with the following body :

    {
    	calendar_ids : [calendar_id1, calendar_i2, new_calendar_id3, new_calendar_id4]
    }
    
will not only add the two new calendars to the list in the event resource, it will also subscribe the event to these new calendars.

Similarly, the following request

    PATCH /events/`<event_id>`/ with the following body :

    {
    	calendar_ids : [calendar_id1, calendar_id3, calendar_id4]
    }
    
will not only update the calendar_ids list of the specific event resource, it will also unsubscribe the specific event from the `calendar_id2` calendar.

**Interdependencies between fields in PATCH**

* `start` & `end`:
    * start should always be before end
* `start`, `end` & `event_type`:
    * When the event type is `normal`, start and end should always both be set 
* `start`, `end` and `all_day`:
    * When all_day is set to `true`, the start and end should only contain the date and no time, e.g. `2015-02-12T00:00:00:00.000000Z`
* `start` & `start_timezone`:
    * When start is set, start_timezone also always needs to be set. This holds true even if you are setting start_time to null (for todo events). 
* `end` & `end_timezone`:
    * When end is set, end_timezone also always needs to be set. This holds true even if you are setting start_time to null (for todo events). 
* `event_type` & `related_event_id`:
    * When the event type is not `arrive_by` or `depart_from`, related event can't be set
* `rsvp_status` & `calendar_ids`:
    * When you want to change your rsvp on a read-only event or add a read-only event to one of your calendars, make sure to pas ONLY one or both of these fields. Anythng else mentioned in the payload will result in a 'forbidden' error message.
