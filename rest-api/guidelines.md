# Applied API Design guidelines

## Header parameters

### Public requests don't use header parameters

Because we want to keep any public request linkable (e.g. on a web page or in an email) we will not use HTTP headers to provide request meta-data such as accepted content type.

## Endpoint URI syntax and specification

### API versioning

Every endpoint starts with /v`<x>` where x is the version

### Interpretation of HTTP methods

This is how different HTTP methods are interpreted and used in the API

Action | HTTP method | Example
:--- | :--- | :--- |
**C**reate new resource | POST | `POST /events`
**R**etrieve resource  | GET | `GET /events/<event_id>` 
Partially **U**pdate resource  | PATCH | `PATCH /events/<event_id>`
**D**elete resource  | DELETE | `DELETE /events/<event_id>`
Replace complete resource | PUT | `PUT /events/<event_id>`
<br/>

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

### Operaters upon query parameters use lower case characters and underscores and start with double underscores

Good:
```
    GET /super-trip/?modality_types=["spaceship"]&top_speed__gt=420000
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
   
### Queries are evaluated using the AND operator

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

### Objects are encoded as tuples

In some cases a query parameter value is actually a collection of values. For instance a circular area is normally represented as follows:

    {
        latitude : <latitude value>,
        longitude : <longitude value>,
        radius : <radius in meters>
    }
    
To encode this in as a query parameter value the collection of values are converted in to a tuple representation as follows:
    
    GET /events?geo_circles=[(<lat value1>, <lon value 1>, <radius 1>), …, (<lat valueN>, <lon value N>, <radius N>)]

## JSON API Responses

### General structure of a JSON response

#### In case of success

When a request was successful (e.g. status code is 2xx) the generally expected structure of the response body is as follows:

    {
        data : [
        <results item 1>,
        …
        <results item N>
        ],
        
        meta_data : {
            //… meta data fields …
        }
    }
    
Note that the results `data` is always in the form of an array. This is to make the structure uniform for all the possible responses.

The `meta_data` field may contain the following fields, depening on the request:

* `sync_token`: see [Sync token](#sync-token)
* `limit`: see [Pagination](#pagination)
* `offset`: see [Pagination](#pagination)
* `count`: The total count of the items that could be returned, also see [Offset, limit and count](#offset-limit-and-count)

#### In case of error

When a request was NOT successful (e.g. status code is 4xx or 5xx) the response body can contain an "error" field with an error object.

Response with an error object

    {
        error : {
            message : <Error message string>,
            code : <OPTIONAL. code string representing the error>,
            original_error : <Nested error object | string represention>
        }
    }
    
### Field names use underscore notation

Field names in response bodies use underscore notation, for instance :

    {
        company_name : "calendar42",
        is_awesome : true
    }    
    
### Representation of related resources

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

## URL Fields pointing to images

In order to cope with images being served over both secure (https) and insecure (http) connections, URL fields are expected to begin with `"://"` instead of "http://" or "https://".
    
## Sync token

To make it easy to just request for resources updated since your last request you can use a `sync_token`. Within each request the `sync_token` is added to the `meta_data` object of the response. When making the next request the `sync_token` can be added to the query-parameters to request for all changes since the previous request.

Note that the `sync_token` returned is related to the current state of all the data, it's the responsibility of the client to have requested all the (paginated) data beforehand.

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

## Pagination

To allow to request a limited amount of rows, is required to send the limit and offset params 

Parameter | Type | Required | Default |Description
:--- | :--- | :--- | :--- | :--- 
limit | INT | False | 10 | Tells to the API the amount of rows that are being requested
offset | INT | False | 0 | Tells the API where to start returning records from the entire set of results. If you don't include this parameter, the default is to start at record number 0 and then return the number of records specified with the 'limit' parameter.
<br/>

### Offset, limit and count

When requesting an endpoint that supports `offset` and `limit`, the response will also contain a `count` that specifies the total amount of items that could be returned. This `count` can be used to determine whether all items have been returned, and the amount of necessary pagination needed.

By sending `offset=0&limit=0` the `count` will still be returned, allowing to only request the `count` for usecases in which the item details are not needed.

### A note on default offset and limit

As described above, requests will default to repsonding with the first 10 items when no offset or limit are specified. To find out whether all items are returned, the count can be checked inside the meta-data send along with the request.

Furthermore, even when specifying for a specific set of items with for instance the `ids` parameter, the limit will still default to 10. If you for example retrieve `/events/ids=[01,02,03,04,05,06,07,08,08,10,11]`, only the first 10 items will be returned.

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

# Max-limit

Currently the maximum value that can be set for `limit` is 100, meaning that any endpoint can only be paginated by 100 at the time. Setting the limit to any higher value will return an error.

# Rate-limits

* The number of API calls is limited on an hour basis accross the API
* The amount of calls differ between anonymous users and users with an [API Token](/rest-api/api-tokens/)