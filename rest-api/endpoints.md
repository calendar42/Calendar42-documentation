# REST API Endpoints

This chapter describes the actual endpoints ot the Calendar42 API.

---------------------------------------

## /events/

Support methods:

* GET

### GET: /events/

* Returns a default response object with a list of [Event](/rest-api/objects/#event) objects inside the data object.

#### parameters

Parameter | Value | Required | Description
:--- | :--- | :--- | :---
ids | `[<event_id>]` | false | Allows to retrieve or filter specific events
sync_token | `<sync_token>` | false | [See Sync Token for more info](/rest-api/guidelines/#sync-token)
service_ids | `[<service_id>]` | false | 
calendar_ids | `[<calendar_id>]` | false | 
event_types | `[<event_type>]` | false | [Event Types](/rest-api/constants/#event-type)
geo_circles | `[<geo_circle>]` | false | [Geo Circle](#geo-circle)
length | `<length>` | false | length in meters of event types arrive_by, depart_from and route. Supports lt and gt operators
order_by | `"distance"` | false | Can only be set when exactly 1 geo_circle is passed along
<br>

### Example usages

Get events belonging to a certain calendar within a certain geographic range, orderder by distance:

* ``/events/?calendar_ids=[abc123]&geo_circles=[(52.28297176 5.27424839 5000)]&order_by=distance``

Get journeys longer than 15km

* ``/events/?event_types=[arrive_by,depart_from]&length__gt=15000``

Get events that changed since last retrieval

* ``/events/?sync_token=128973981273``

---------------------------------------

## /events/`<event_id>`/

Supported methods

* GET
* PATCH

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


## /events/suggestions/

Supported methods

* GET

### GET /events/suggestions/

* Returns a default response object with a list containing [Event](/rest-api/objects/#event) objects inside the data object.
* Note that the returned event objects are considered suggestions and have no id related to it yet. In order to store the event and perform other actions, the event needs to be published to the server

#### Parameters

Parameter | Value | Required | Description
--- | --- | --- | ---
event_type | `<event_type>` | true | Journey subset of [Event Type](/rest-api/constants/#event-type)
transport_modes | `[<transport_mode>]` | true | Array of [Transport Modes](/rest-api/constants/#transport-mode)
from_location | `position` | true | Tuple with lat lon
to_location | `position` | true | Tuple with lat lon
time | `date-time` | false (if event_type equals 'route') | [Date time](/rest-api/objects/#date-time)

#### Example usage

Get a journey from point A to arrive at a certain time at point B

* ``/events/suggestions?event_type=arrive_by&transport_modes=[bicycle]&from_location=(42.1 4.5)&to_location=(42.5 4.6)&time=2015-03-24T14%3A29%3A47.613Z``

## /calendars/

Supported methods:

* GET
* POST
* PATCH

### GET /calendars/

Returns a default response object with a list of [Calendar](/rest-api/objects/#calendar) objects inside the data object.

#### parameters

Parameter | Value | Required | Description
--- | --- | --- | ---
ids | `[<calendar_id>]` | false | Allows to retrieve or filter specific calendars
sync_token | `<sync_token>` | false | [See Sync Token for more info](/rest-api/guidelines/#sync-token)
service_ids | `[<service_id>]` | false
categories | `[<calendar_category>]` | false | [Calendar Category](/rest-api/objects/#calendar)

#### POST parameters

All required attributes of a [calendar](/rest-api/objects/#calendar) should be sent, and all editable params can be sent as a param

#### PATCH parameters

All editable params of a [calendar](/rest-api/objects/#calendar) can be sent as a param and it will be replaced with the new value

## Subscriptions

### /subscriptions/

Subscriptions are resources describing the relationship between events and users (the 'event subscribers).

#### Supported methods

* GET

Parameter | Value | Required | Description
--- | --- | --- | ---
- | - | - | -

#### Response

Returns a default response object with a list of [Subscription](/rest-api/objects/#subscription) objects inside the data object.

#### GET parameters

Parameter | Value | Required | Description
--- | --- | --- | --- 
object_type | `[<object_type (event || calendar)>` | true | Only get subscriptions related to a certain type ex. events
sync_token | `<sync_token>` | false | [See Sync Token for more info](/rest-api/guidelines/#sync-token)
service_ids | `[<service_id>]` | false
calendar_ids | `[<calendar_id>]` | false | only use calendar_ids or event_ids, they can't be used together in the same request
event_ids | `[<calendar_id>]` | false | only use calendar_ids or event_ids, they can't be used together in the same request

### /subscriptions/`<subscription_id>`/

#### Supported methods

* GET Same as [/subscriptions/](#subscriptions) but getting a list containing the single subscription based on the subscription id.
* POST
* PATCH

#### GET parameters

Same as [/subscriptions/](#subscriptions) GET call

#### POST parameters

All required attributes of a [subscription](/rest-api/objects/#subscription) should be sent, and all editable params can be sent as a param

#### PATCH parameters

All editable params of a [subscription](/rest-api/objects/#subscription) can be sent as a param and it will be replaced with the new value

## Locations

### /locations/

#### Supported methods

* GET
* PUT
* PATCH
* POST
* DELETE

#### Response

Returns a default response object with a list of [Location](/rest-api/objects/#location) objects inside the data object.

As depicted, [Location](/rest-api/objects/#location) objects may contain one or more labels that add extra details to the location. These labels add extra context for a user or a service. It may for instance mark the location as a work location for the requesting user, or contain service specific details.

When requesting the `/locations/` without any parameters, it will return all locations available in the system, ordered by most used by the requesting user.

#### GET parameters

Parameter | Value | Required | Description
--- | --- | --- | ---
ids | `[<location_id>]` | false | Allows to retrieve or filter specific locations
sync_token | `<sync_token>` | false | [See Sync Token for more info](/rest-api/guidelines/#sync-token)
user_ids | `[<user_id>]` | false
service_ids | `[<service_id>]` | false | Only return locations that have labels in relation to the service
search_pattern | `<string>` | false
location_types | `[<location_type>]` | false | [Location Type](/rest-api/constants/#location-type)
geo_circles | `[<geo_circle>]` | false | [Geo Circle](#geo-circle)


### /locations/`<location_id>`/

#### Supported methods

* GET

Same as [/locations/](/rest-api/objects/#location) but getting a list containing the single location based on the location id.

## Positions

### /positions
<!-- *TODO* -->

#### Supported methods

* POST

### Request Body

See [Position](/rest-api/objects/#position) model.

