Calendar42 REST API
===================

# TODO:
* Set the limit 'pagination' default value

# Applied API Design guidelines

## Public requests don't use header parameters

Because we want to keep any public request linkable (e.g. on a web page or in an email) we will not use HTTP headers to provide request meta-data such as accepted content type.

## Endpoint URI syntax and specification

### API versioning

Every endpoint starts with /v`<x>` where x is the version



### Interpretation of HTTP methods

This is how different HTTP methods are interpreted and used in the API

Action | HTTP method | Example
--- | --- | --- |
**C**reate new resource | POST | `POST /events`
**R**etrieve resource  | GET | `GET /events/<event_id>` 
Partially **U**pdate resource  | PATCH | `PATCH /events/<event_id>`
**D**elete resource  | DELETE | `DELETE /events/<event_id>`
Replace complete resource | PUT | `PUT /events/<event_id>`

### Endpoints only use lower case characters and dashes

Good:
```
    /super-trip
``` 
Bad:
```
    /SuperTrip
    /super_trip
```

### Query parameters use lower case characters and underscores

Good:
```
    GET /super-trip/?modality_types=["spaceship"]
```    
Bad:
```
    GET /super-trip/?modality-types=["spaceship"]
    GET /super_trip/?ModalityTypes=["spaceship"]
```


### A query parameter value that could be an array is always an array

If a value for a query parameter could be an array, it is _always_ send as an array.
This is done to keep the URI endpoint syntax uniform. For instance:
```
    /events/?calendar_ids=[<resource_id>,..]
```

We do this even if we only need to specify one value. So, for instance, we do:
```
    GET /events/?calendar_ids=[<resource_id>]
```

And thus not:
```
    GET /events/?calendar_ids=<resource_id>   
```

Query parameters that can not have an array as value, such as sync_token, of course don't use a list syntax.

### A query parameter name is always plural when its value could be an array

Query parameters that could have an array as value will always have a name in plural form, calendar_id**s** instead of calendar_id.

Example:
```
    /events/?calendar_ids=[<resource_id>,..]
```

### Constants are represented by there semantic definition

Sometimes values of query parameters are enumeration values. For example imagine `event_type` is one of the following constants:

    NORMAL = 0
    TRIP   = 1
    WEIRD  = 2

When event_type is used as a query parameter the value is always represented by the semantic definition. For instance, "normal" is used instead of "0". 

**Note that** the semantic representation is always based on lower-case characters to comply to **Query parameters use lower case characters and underscores**.

Thus a request for weird events might look like this:

    GET /events?event_types=["weird"]
   
## Queries are evaluated using the AND operator

When querying resources using GET requests with query parameters, the query is interpreted by concatenating the query predicates with AND operators.

Thus the following query

    GET /tags/?service_ids=[<serviceA>]&calendar_ids=[<calendarX>,<calendarY>]
    
is interpreted as

    GET tags that belong to <serviceA> AND <calendarX> AND <calendarY>

The user of the API must use multiple API calls to simulate queries that require OR operators. E.g. the following query

    GET tags that belong to <serviceA> AND (<calendarX> OR <calendarY>)

Needs two API calls as follows

    GET /tags/?service_ids=[<serviceA>]&calendar_ids=[<calendarX>]
    GET /tags/?service_ids=[<serviceA>]&calendar_ids=[<calendarY>]
    
The responses of the two requests are then combined to get the full query result.

## Objects are encoded as tuples

In some cases a query parameter value is actually a collection of values. For instance a circular area is normally represented as follows:

    {
        latitude : <latitude value>,
        longitude : <longitude value>,
        radius : <radius in meters>
    }
    
To encode this in as a query parameter value the collection of values are converted in to a tuple representation as follows:
    
    GET /events?geo_circles=[(<lat value1>, <lon value 1>, <radius 1>), …, (<lat valueN>, <lon value N>, <radius N>)]

# JSON API Responses

## General structure of a JSON response

### In case of success

When a request was successful (e.g. status code is 2xx) the generally expected structure of the response body is as follows:

    {
        data : [
        <results item 1>,
        …
        <results item N>
        ],
        
        meta_data : {
            //… meta data fields …
            //contents depends on request            
        }
    }
    
Note that the results data is always in the form of an array. This is to make the structure uniform for all the possible responses.

### In case of error

When a request was NOT successful (e.g. status code is 4xx or 5xx) the response body can contain an "error" field with an error object.

Response with an error object

    {
        error : {
            message : <Error message string>,
            code : <OPTIONAL. code string representing the error>,
            original_error : <Nested error object | string represention>
        }
    }
    
## Field names use underscore notation

Field names in response bodies use underscore notation, for instance :

    {
        company_name : "calendar42",
        is_awesome : true
    }    
    
## Representation of related resources

In a representation of a resource, related resources are represented by a list of resource IDs. For example, with each event a list of related calendars is given as follows: 

    {
        //…
        
        type : "event",
        
        
        //…
        calendar_ids : [
        	<calendar_id1>,
        	
        	...
        	
        	<calendar_idN>
        ] 
        
    }

## Date Time

### Date format

    The date format that should be used is ISO-8601  2012-04-23T18:25:43.511Z extended.
    
    So the expected format will be: "YYYY-MM-DDThh:hh:mm:ss.sss"
    
    An example of valid date format:
    
    "2004-02-12T15:19:21+00:00" // URL ENCODED: 2015-03-24T14%3A29%3A47.613Z
    
### Timezone format

For timezones the standard olson timezone definitions should be used (see: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

    
# Sync token
To make it easy to just request for resources updated since your last request you can use a `sync_token`. Within each request the `sync_token` is added to the `meta_data` object of the response. When making the next request the `sync_token` can be added to the query-parameters to request for all changes since the previous request.

### Example:

*Step 1:*
GET /api/v1/events/ 

All of the events are returned and the current sync_token.

    {
        "data": [<event object 1>, <event object 2>],
        "meta_data": {
            "sync_token": 142
        }
    }

*Step 2:*
GET /api/v1/events/?sync_token=142


Only the event changed between Step 1, and Step 2 are returned, so in this case event1 is changed, and event3 was added.

    {
        "data": [<event object 1>, <event object 3>],
        "meta_data": {
            "sync_token": 144
        }
    }

# Pagination

To allow to request a limited amount of rows, is required to send the limit and offset params 

Parameter | Type | Required | Default |Description
--- | --- | --- | --- | --- 
limit | INT | False |  | Tells to the API the amount of rows that are being requested
offset | INT | False |  | Tells the API where to start returning records from the entire set of results. If you don't include this parameter, the default is to start at record number 0 and then return the number of records specified with the 'limit' parameter.

### Example:

GET /api/v1/events/?limit=10&offset=0

    {
        "data": [<event object i_0>, ..., <event object i_9>],
        "meta_data": {
            "sync_token": 142,
            "count": 42,
            "offset": 0
        }
    }

GET /api/v1/events/?limit=10&offset=10

    {
        "data": [<event object i_10>, ..., <event object i_19>],
        "meta_data": {
            "sync_token": 142,
            "count": 42,
            "offset": 10
        }
    }

#Calendar42 API endpoints
This chapter describes the actual endpoints ot the Calendar42 API.

## /events/

### Supported methods
* GET

### Response

Returns a default response object with a list of [Event](#event) objects inside the data object.

### GET parameters

Parameter | Value | Required | Description
--- | --- | --- | --- 
sync_token | `<sync_token>` | false | [See Sync Token for more info](#sync-token)
service_ids | `[<service_id>]` | false
calendar_ids | `[<calendar_id>]` | false
event_types | `[<event_type>]` | false | [Event Types](#event-types)
geo_circles | `[<geo_circle>]` | false | [Geo Circle](#geo-circle)



## /events/`<event_id>`/

### Supported methods
* GET

Same as [/events/](#events) but getting a list containing the single event based on the event id.

* PATCH

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


## /calendars/

### Supported methods
* GET
* POST
* PATCH

### Response

Returns a default response object with a list of [Calendar](#calendar) objects inside the data object.

### GET parameters

Parameter | Value | Required | Description
--- | --- | --- | ---
sync_token | `<sync_token>` | false | [See Sync Token for more info](#sync-token)
service_ids | `[<service_id>]` | false
calendar_categories | `[<calendar_category>]` | false | [Calendar Category](#calendar-category)

### POST parameters

All required attributes of a [calendar](#calendar) should be sent, and all editable params can be sent as a param

### PATCH parameters

All editable params of a [calendar](#calendar) can be sent as a param and it will be replaced with the new value

## /subscriptions/

Subscriptions are resources describing the relationship between events and users (the 'event subscribers).

### Supported methods
* GET

Parameter | Value | Required | Description
--- | --- | --- | ---

### Response

Returns a default response object with a list of [Subscription](#subscription) objects inside the data object.

### GET parameters

Parameter | Value | Required | Description
--- | --- | --- | --- 
object_type | `[<object_type (event || calendar)>` | true | Only get subscriptions related to a certain type ex. events
sync_token | `<sync_token>` | false | [See Sync Token for more info](#sync-token)
service_ids | `[<service_id>]` | false
calendar_ids | `[<calendar_id>]` | false | only use calendar_ids or event_ids, they can't be used together in the same request
event_ids | `[<calendar_id>]` | false | only use calendar_ids or event_ids, they can't be used together in the same request

## /subscriptions/`<subscription_id>`/

### Supported methods
* GET
Same as [/subscriptions/](#subscriptions) but getting a list containing the single subscription based on the subscription id.
* POST
* PATCH

### GET parameters

Same as [/subscriptions/](#subscriptions) GET call

### POST parameters

All required attributes of a [subscription](#subscription) should be sent, and all editable params can be sent as a param

### PATCH parameters

All editable params of a [subscription](#subscription) can be sent as a param and it will be replaced with the new value

## /locations/

### Supported methods
* GET
* PUT
* PATCH
* POST
* DELETE

### Response

Returns a default response object with a list of [Location](#location) objects inside the data object.

As depicted, [Location](#location) objects may contain one or more labels that add extra details to the location. These labels add extra context for a user or a service. It may for instance mark the location as a work location for the requesting user, or contain service specific details.

When requesting the `/locations/` without any parameters, it will return all locations available in the system, ordered by most used by the requesting user.

### GET parameters

Parameter | Value | Required | Description
--- | --- | --- | ---
sync_token | `<sync_token>` | false | [See Sync Token for more info](#sync-token)
user_ids | `[<user_id>]` | false
service_ids | `[<service_id>]` | false | Only return locations that have labels in relation to the service
search_pattern | `<string>` | false
location_types | `[<location_type>]` | false | [Location Type](#location-type)
geo_circles | `[<geo_circle>]` | false | [Geo Circle](#geo-circle)


## /locations/`<location_id>`/

### Supported methods
* GET

Same as [/locations/](#location) but getting a list containing the single location based on the location id.

## /positions
*TODO*

### Supported methods
* POST

### Request Body

See [Position](#position) model.

# Constants

## Event Type

Type | Description
--- | ---
normal | Normal events
arrive_by | -
depart_from | -
todo | -
tracked_tentative | -
tracked_event | -
tracked_arrive_by | -
route | -

## Calendar Type

@todo

Type | Description
--- | ---

## RSVP Status

Type | Description
--- | ---
not_replied | You cant set attendance to this number this is the default, is interpreted as not-attending
attending | -
not_attending | -

## Location type

Type | Description
--- | ---
favorite | -
home | -
work | -

## Transport mode

Type | Description
--- | ---
car | -
public_transport | -

## Permission

Type | Description
--- | ---
invited_read | Invited with read-only permission
subscribed_read | Subscribed with read-only permission
invited_write | Invited with read-write permission
subscribed_write | Subscribed with read-write permission
removed | Removed

# Objects

## Person

```javascript
    {
        "id": "<string>",
        "first_name": "<string>",
        "last_name": "<string>",
        "photo": "<url>",
        "email": "<email>",
        "phonenumber": "<phonenumber>",
    }
```

## Subscription

```javascript
    {
        "id": "<string>",

        "object": {
            "object_type": "<event || calendar>",
            "id": "<string>",
        }

        "subscriber": "<person>", // Person that has the subscription
        "creator": "<person>", // Person created the subscription

        "is_invitation": "<boolean>",
        "rsvp_status": "<rsvp-status>",
        "permission": "<permission>",
    }
```

## Event

Attribute name | Type | Mandatory | Editable | Default | Description | Valid value/s |
--- | --- | --- | --- | --- | --- | --- |
id | String | false | false | true | Unique id that identifies the event | |
event_type | String | true | false | 'event' | Type of the event | [event type](#event-type) |
is_suggestion | Boolean | true | true | false | If the event is autogenerated by the system, so it is a suggestion based on the preferences of the user |  |
creator | Object | true | false | [Person](#person) | [Person object](#person) that created that event |  |
modified | [Date](#date-format) | false | false | "YYYY-MM-DDThh:hh:mm:ss" | Date of the last modification of the event | |
is_invitation | Boolean | false | true | false | If the event is an invitation. This is an user related value | |
invitation | Object | false | true | [Invitation](#invitation) | In the case that this event is an invitation, this attribute will contain some meta information about the invitation | [Invitation object](#invitation) |
rsvp_status | String | true | true | 'not_replied' | String that defines the rsvp status of the user at this event. This is an user related attribute | [RSVP](#rsvp-status) |
calendar_ids | Array | true | true |  | List of ID's of subscribed calendars | |
start | [Date](#date-format) | true | true |  | Start time of the event | |
end | [Date](#date-format) | true | true |  | End time of the event | |
start_timezone | String | true | true |  | Time zone of the start time of this event | [Timezone](#timezone-format) |
end_timezone | String | true | true |  | Time zone of the end time of this event | [Timezone](#timezone-format) |
all_day | Boolean | true | true | false | If the event is an all day event this should have a true as a vaule | |
title | String | true | true |  | The title of the event  | |
description | String | false | true |  | Description of the event | |
color | String | false | true |  | Events can have a color related, this color should be in hsla format | |
image | String | false | true |  | the url where to reach the event image | |
source_url | String | false | false | Url source of the event | If the event is imported from an external service (ics) this attribute contains the URL where to reach the event information from the source | |
start_location | Object | false | true |  | The location where the event starts | [Location](#location) |
end_location | Object | false | true |  | The location where the event ends | [Location](#location) |
recurrence | Boolean | false | true | false | If the event is a recurrence event |  |
recurrence_parent | String | false | true |  | The ID of the related recurrence event |  |
related_event | Array | false | true | [] | List of events ID's related to this event |  |
sync_token | Integer | false | false |  | The [sync token](#sync-token) |  |
permissions | String | true | true | 'subscribed_write' | The string that defines the permission that the user have over this event. This is an user related attribute | [Permission](#permission) |
previous_permission | String | false | false |  | The previous permission that the user had over this event. This is an user related attribute | [Permission](#permission) |
trip | Object | false | true |  | If the event is actually a trip, this attribute will contain all the meta data related with the trip | [Trip](#trip) |

```javascript
    {
        "id": "<string>",
        "event_type": "<event-type>",
        "is_suggestion": "<bool>",

        "creator": "<person>", // Person created the event
        "created": "<date>",
        "modified": "<date>",

        "is_invitation": "<bool>",
        "invitation": <invitation>,

        "rsvp_status": "<rsvp-status>", // See rsvp list

        "calendar_ids": [ <calendar-id>, <calendar-id>, <calendar-id> ],

        "start": "<date>",
        "end": "<date>",
        "start_timezone": "<string>",
        "end_timezone": "<string>",
        "all_day": "<bool>",

        "title": "<string>",
        "description": "<string>",
        "color": "<string>",
        "image": "<url>",
        "source_url": "<url>",
        
        "start_location": "<location>",
        "end_location": "<location>",

        "recurrence": "<bool>",
        "recurrence_parent": "<string>",
        
        "related_event": ["<event_id>"], // For now always only contains one

        "sync_token": "<int>",
    
        // Permission over the event
        "permission": "<permission>",
        "previous_permission": "<permission>",

        "trip": {
            "query_parameters": {
                "transport_mode": "<transport-mode>",
                "time_buffer": "<int>", // Seconds
            },
            "data": {
                "distance": "<int>", // Meters
                "duration": "<int>", // Seconds
                "legs": [],
            }
        }
    }
```

## Calendar

Attribute name | Type | Mandatory | Editable | Default | Description | Valid value/s |
--- | --- | --- | --- | --- | --- | --- |
id | String | false | false | true | Unique id that identifies the calendar | |
created | [Date](#date-format) | false | false |  | Date were the calendar was created | |
modified | [Date](#date-format) | false | false |  | Date of the last modification of the calendar | |
creator | Object | true | false | [Person](#person) | [Person object](#person) that created that event |  |
inviter | Object | true | false | [Person](#person) | [Person object](#person) that invited to this event |  |
permission | String | false | false |  | Type of [permission](#permission) that the user have in this calenda. This is an used related attribute | [Permission](#permission) |
name | String | true | true |  | Name of the calendar | |
description | String | false | true |  | Description of the event | |
category | String | false | true |  | Category of the event | |
color | String | false | true |  | Calendars can have a color related, this color should be in hsla format | |
image | String | false | true |  | the url where to reach the calendar image | |
sync_token | Integer | false | false |  | The [sync token](#sync-token) |  |
url| String | false | false |  | The url where to reach the calendar information | |
calendar_type | String | false | false |  | The type of the calendar | [Calendar type](#calenda-type) |
first_import | [Date](#date-format) | false | false |  | Date of first successfull import, not send if never imported | |
import_failed | [Date](#date-format) | false |  | true | Date of last failure, not send if imported successfull afterwards | |


```javascript
    {
        "id": "<string>",

        "created": "<date>",
        "modified": "<date>",

        "creator": "<person>",
        "inviter": "<person>",

        "permission": "<permission>",
        "previous_permission": "<permission>",

        "name": "<string>",
        "description": "<string>",
        "category": "<string>",
        "color": "<string>",
        "image": "<url>",

        "sync_token": "<int>",

        "url": "<string>",
        "calendar_type": "<calendar-type>",

        "first_import": "<date>",

        "import_failed": "<date>" 
    }
```

## Location
    
```javascript
    {
        "id": "<string>",
        "text": "<string>",
        "address": "<string>",
        "postcode": "<string>",
        "city": "<string>",
        "country": "<string>",
        "geo": {
            "latitude": "<float>",
            "longitude": "<float>"
        },
        "labels": [
            {
                "id": "<string>",
                "name": "<string>",
                "location_type": "<location-type>",
                "service_id": "<string>",  // null if not a service related place
                "description": "<string>",
                "weight": "<int>"
            }
        ]
    }
```
    
## Position
*TODO : further explain fields*

```javascript
    {
	    //META DATA
        "source"        : "<the client app name>",
	    "type"          : "<normal || forced>",
	    "timestamp"     : "<string representation of date and time>",
	    "user_info"     : "<An object containing information of user>",

	    //LOCATION DATA
	    "latitude"      : "<string representation of latitude value (double)>",
	    "longitude"     : "<string representation of longitude value (double)>",
	    "accuracy"      : "<string representation of accurracy value (double)>",
	    "heading"       : "<string representation of heading value (double)>",
	    "speed"         : "<string representation of speed value (double)>",
	
	    //Currently not used for checkin detection
	    "altitude"      : "<string representation of altitude value (double)>",
	    "altitude_accuracy": "<string representation of altitude_accuracy value (double)>"
    }
```
## Invitation
```javascript
	{
	    "actor": "<person>",
	    "message": "<string>",
	    "created": "<date>",
	}
```

## Trip

```javascript
	{
		"query_parameters": {
			"transport_mode": "<transport-mode>",
			"time_buffer": "<int>", // Seconds
		},
		"data": {
			"distance": "<int>", // Meters
			"duration": "<int>", // Seconds
			"legs": [],
		}
	}
```
