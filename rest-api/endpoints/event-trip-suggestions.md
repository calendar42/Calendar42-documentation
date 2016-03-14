# Introduction

Provides of trip suggestions towards the provided event.

**Supported methods:**

* GET `acceptation`

### GET /events/trip-suggestions/

* Returns a default response object with a list containing [Event](/rest-api/objects/#event) objects inside the data object.
* Note that the returned event objects are considered suggestions and have no id related to it yet. In order to store the event and perform other actions, the event needs to be published to the server

#### Parameters

Parameter | Required | Description
--- | --- | ---
`event_type` | true | [Event Type](/rest-api/constants/#event-type) (currently only supports `arrive_by` & `depart_from`)
`transport_modes` | true | Array of [Transport Modes](/rest-api/constants/#transport-mode)
`from_location` | true | Tuple with lat lon
`to_location` | true | Tuple with lat lon
`time` | true | [Date time](/rest-api/usage/#date-time) (not required if event_type equals 'route')
<br>

#### Example

Get a trip from point A to arrive at a certain time at point B

``/events/trip-suggestions?event_type=arrive_by&transport_modes=[bicycle]&from_location=(42.1 4.5)&to_location=(42.5 4.6)&time=2015-03-24T14%3A29%3A47.613Z``

#### Error responses

Even when the parameters are valid a trip suggestion request might still result in an error due to multiple other reasons. The trip planner might not support the locations send (the case when sending points in the middle of the sea), or the time might be too far in the future or history to be able to route for (in the case of public transport requests). When such cases occur an error message will be returned similar to:

	{
	  "error": {
	    "status_code": 500,
	    "message": "Trip is not possible.  You might be trying to plan a trip outside the map data boundary.",
	    "code": "GENERAL_SYSTEM_ERROR"
	  }
	}
