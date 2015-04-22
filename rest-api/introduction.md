Calendar42 REST API
===================

<!-- # TODO:
* Set the limit 'pagination' default value -->

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

