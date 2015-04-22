This chapter describes the actual endpoints ot the Calendar42 API.

# /events/

**Supported methods**

* GET

**Response**

Returns a default response object with a list of [Event](#event) objects inside the data object.

**GET parameters**

Parameter | Value | Required | Description
--- | --- | --- | --- 
sync_token | `<sync_token>` | false | [See Sync Token for more info](#sync-token)
service_ids | `[<service_id>]` | false
calendar_ids | `[<calendar_id>]` | false
event_types | `[<event_type>]` | false | [Event Types](#event-types)
geo_circles | `[<geo_circle>]` | false | [Geo Circle](#geo-circle)

# /events/`<event_id>`/

**Supported methods**

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


# /calendars/

**Supported methods**

* GET
* POST
* PATCH

**Response**

Returns a default response object with a list of [Calendar](#calendar) objects inside the data object.

**GET parameters**

Parameter | Value | Required | Description
--- | --- | --- | ---
sync_token | `<sync_token>` | false | [See Sync Token for more info](#sync-token)
service_ids | `[<service_id>]` | false
calendar_categories | `[<calendar_category>]` | false | [Calendar Category](#calendar-category)

**POST parameters**

All required attributes of a [calendar](#calendar) should be sent, and all editable params can be sent as a param

**PATCH parameters**

All editable params of a [calendar](#calendar) can be sent as a param and it will be replaced with the new value

# /subscriptions/

Subscriptions are resources describing the relationship between events and users (the 'event subscribers).

**Supported methods**

* GET

Parameter | Value | Required | Description
--- | --- | --- | ---

**Response**

Returns a default response object with a list of [Subscription](#subscription) objects inside the data object.

**GET parameters**

Parameter | Value | Required | Description
--- | --- | --- | --- 
object_type | `[<object_type (event || calendar)>` | true | Only get subscriptions related to a certain type ex. events
sync_token | `<sync_token>` | false | [See Sync Token for more info](#sync-token)
service_ids | `[<service_id>]` | false
calendar_ids | `[<calendar_id>]` | false | only use calendar_ids or event_ids, they can't be used together in the same request
event_ids | `[<calendar_id>]` | false | only use calendar_ids or event_ids, they can't be used together in the same request

# /subscriptions/`<subscription_id>`/

**Supported methods**

* GET Same as [/subscriptions/](#subscriptions) but getting a list containing the single subscription based on the subscription id.
* POST
* PATCH

**GET parameters**

Same as [/subscriptions/](#subscriptions) GET call

**POST parameters**

All required attributes of a [subscription](#subscription) should be sent, and all editable params can be sent as a param

**PATCH parameters**

All editable params of a [subscription](#subscription) can be sent as a param and it will be replaced with the new value

# /locations/

**Supported methods**

* GET
* PUT
* PATCH
* POST
* DELETE

**Response**

Returns a default response object with a list of [Location](#location) objects inside the data object.

As depicted, [Location](#location) objects may contain one or more labels that add extra details to the location. These labels add extra context for a user or a service. It may for instance mark the location as a work location for the requesting user, or contain service specific details.

When requesting the `/locations/` without any parameters, it will return all locations available in the system, ordered by most used by the requesting user.

**GET parameters**

Parameter | Value | Required | Description
--- | --- | --- | ---
sync_token | `<sync_token>` | false | [See Sync Token for more info](#sync-token)
user_ids | `[<user_id>]` | false
service_ids | `[<service_id>]` | false | Only return locations that have labels in relation to the service
search_pattern | `<string>` | false
location_types | `[<location_type>]` | false | [Location Type](#location-type)
geo_circles | `[<geo_circle>]` | false | [Geo Circle](#geo-circle)


# /locations/`<location_id>`/

**Supported methods**

* GET

Same as [/locations/](#location) but getting a list containing the single location based on the location id.

# /positions
<!-- *TODO* -->

**Supported methods**

* POST

## Request Body

See [Position](#position) model.

