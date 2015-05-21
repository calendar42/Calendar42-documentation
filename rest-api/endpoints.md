# General introduction

This chapter describes the actual endpoints of the Calendar42 API.

---------------------------------------

## • /events/

Supported methods:

* GET `acceptation`
* POST `development`

### GET: /events/

* Returns a default response object with a list of [Event](/rest-api/objects/#event) objects inside the data object.

#### Parameters

Parameter | Required | 
:--- | :--- | :---
`ids` | false | Array of event ids. To filter on specific events (reponse is not equally ordered)
`service_ids` | false | Array of service ids
`calendar_ids` | false | Array of calendar ids <br> Supports the `or` operator
`event_types` | false | Array of [Event Types](/rest-api/constants/#event-type)
`geo_circles` | false | Array of [Geo Circles](#geo-circle)
`length` | false | Length in meters of event types arrive_by, depart_from and route. <br>Supports `lt` and `gt` operators
`order_by` | false | Can be set to "distance" when exactly one geo_circle is passed along
`sync_token` | false | [Sync Token](/rest-api/usage/#sync-token)
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
# Request Payload
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
                "created": "2015-02-12T15:19:21:00.000Z",
                "modified": "2015-02-12T15:19:21:00.000Z",
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

This example shows a regular usecase, where an event is created in one of the accesible calendars, together with a title and a description.

* The `event_type` will default to `normal`
* `normal` events require `start` and `end` to be set
* These dates require their timezones to be set with `start_timezone` and `end_timezone`

```javascript
# Request Payload
    {
        "calendar_ids": ["42b42b42b42b42b42b42b42b42b42b42b42b42b4"],
        "start": "2015-02-12T15:00:00:00.000Z",
        "start_timezone": "Europe/Amsterdam",
        "end": "2015-02-12T15:30:00:00.000Z",
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
                "start": "2015-02-12T15:00:00:00.000Z",
                "start_timezone": "Europe/Amsterdam",
                "end": "2015-02-12T15:30:00:00.000Z",
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
            "meta_data": {
                "sync_token": 143
            }
        }
    }
```

##### Special case: Event creation with location id

Prefered way of posting locations in events.

```javascript
# Request Payload (partial)
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
# Request Payload (partial)
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
# Request Payload (partial)
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

---------------------------------------

## • /events/trip-suggestions/

Supported methods:

* GET `acceptation`

### GET /events/trip-suggestions/

* Returns a default response object with a list containing [Event](/rest-api/objects/#event) objects inside the data object.
* Note that the returned event objects are considered suggestions and have no id related to it yet. In order to store the event and perform other actions, the event needs to be published to the server

#### Parameters

Parameter | Required | 
--- | --- | --- 
`event_type` | true | [Event Type](/rest-api/constants/#event-type) (currently only supports `arrive_by` & `depart_from`)
`transport_modes` | true | Array of [Transport Modes](/rest-api/constants/#transport-mode)
`from_location` | true | Tuple with lat lon
`to_location` | true | Tuple with lat lon
`time` | true | [Date time](/rest-api/usage/#date-time) (not required if event_type equals 'route')
<br>

#### Example

Get a trip from point A to arrive at a certain time at point B

* ``/events/trip-suggestions?event_type=arrive_by&transport_modes=[bicycle]&from_location=(42.1 4.5)&to_location=(42.5 4.6)&time=2015-03-24T14%3A29%3A47.613Z``

#### Error responses

Even when the parameters are valid a trip suggestion request might still result in an error due to multiple other reasons. The trip planner might not support the locations send (the case when sending points in the middle of the sea), or the time might be too far in the future or history to be able to route for (in the case of public transport requests). When such cases occur an error message will be returned similar to:

	{
	  "error": {
	    "status_code": 500,
	    "message": "Trip is not possible.  You might be trying to plan a trip outside the map data boundary.",
	    "code": "GENERAL_SYSTEM_ERROR"
	  }
	}


---------------------------------------

## • /calendars/

Supported methods:

* GET `acceptation`
* POST `development`

### GET /calendars/

Returns a default response object with a list of [Calendar](/rest-api/objects/#calendar) objects inside the data object.

#### parameters

Parameter | Required | 
--- | --- | --- 
`ids` | false | Array of calendar ids. To filter on specific events (response is not equally ordered)
`service_ids` | false | Array of service ids
`categories` | false | Array of [Calendar Category](/rest-api/objects/#calendar)
`sync_token` | false | [Sync Token](/rest-api/usage/#sync-token)
<br>

#### POST parameters

All required attributes of a [calendar](/rest-api/objects/#calendar) should be sent, and all editable params can be sent as a param

#### PATCH parameters

All editable params of a [calendar](/rest-api/objects/#calendar) can be sent as a param and it will be replaced with the new value

---------------------------------------

## • /calendars/`<calendar_id>`/

Supported methods:

* GET `acceptation`

### GET: /calendars/`<calendar_id>`/

* Returns a default response object with a list containing the requested [Calendar](/rest-api/objects/#calendar) object inside the data object.

---------------------------------------

## • /locations/

Supported methods:

* GET `acceptation`

### GET /locations/

Returns a default response object with a list of [Location](/rest-api/objects/#location) objects inside the data object.

As depicted, [Location](/rest-api/objects/#location) objects may contain one or more labels that add extra details to the location. These labels add extra context for a user or a service. It may for instance mark the location as a work location for the requesting user, or contain service specific details.

When requesting the `/locations/` without any parameters, it will return all locations available in the system, ordered by most used by the requesting user.

#### Parameters

Parameter | Required | Description
--- | --- | --- 
`ids` | false | Array of location ids. To filter on specific locations (reponse is not equally ordered)
`sync_token` | false | [Sync Token](/rest-api/usage/#sync-token)
`user_ids` | false | Array of service ids. Only return locations that have labels in relation to user
`service_ids` | false | Array of service ids. Only return locations that have labels in relation to the service
`search_pattern` | false | String to match on in location text, address, city and label
`location_types` | false | Array of [Location Type](/rest-api/constants/#location-type)
`geo_circles` | false | Array of [Geo Circle]
`geo_polylines` | false | Array of [GeoPolyline](https://developers.google.com/maps/documentation/utilities/polylinealgorithm)
<br>

Note: doesn't support order_by=distance yet

#### Example 

**@todo:** Add example usage

---------------------------------------

## • /locations/`<location_id>`/

Supported methods:

* GET `acceptation`

### GET: /locations/`<location_id>`/

* Returns a default response object with a list containing the requested [Location](/rest-api/objects/#location) object inside the data object


---------------------------------------

Below API's are still in early development

---------------------------------------

## • /subscriptions/

Subscriptions are resources describing the relationship between events and users (the 'event subscribers).

Supported methods:

* GET `development`

Parameter | Required | Description
--- | --- | --- 
- | - | - | -
<br>

Response

Returns a default response object with a list of [Subscription](/rest-api/objects/#subscription) objects inside the data object.

GET parameters

Parameter | Required | Description
--- | --- | --- 
`object_type` | true | Only get subscriptions related to a certain type ex. events (event || calendar)
`sync_token` | false | [Sync Token](/rest-api/usage/#sync-token)
`service_ids` | false | 
`calendar_ids` | false | only use calendar_ids or event_ids, they can't be used together in the same request
`event_ids` | false | only use calendar_ids or event_ids, they can't be used together in the same request
<br>

---------------------------------------

## • /subscriptions/`<subscription_id>`/

Supported methods:

* GET `development`
* POST `development`
* PATCH `development`

GET parameters

Same as [/subscriptions/](#subscriptions) GET call

POST parameters

All required attributes of a [subscription](/rest-api/objects/#subscription) should be sent, and all editable params can be sent as a param

PATCH parameters

All editable params of a [subscription](/rest-api/objects/#subscription) can be sent as a param and it will be replaced with the new value


---------------------------------------

## • /positions/
<!-- *TODO* -->

Supported methods:

* POST `development`

 Request Body

See [Position](/rest-api/objects/#position) model.

