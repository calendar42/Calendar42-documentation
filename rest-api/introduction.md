<!-- # TODO:
* Set the limit 'pagination' default value -->
Using our [REST](http://en.wikipedia.org/wiki/Representational_state_transfer) API, you can make Calendar42 do pretty much anything planning related you want. The only thing left to do for you is showing up! 


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


