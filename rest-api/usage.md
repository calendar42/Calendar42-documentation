# General Implementation Notes

## API versioning

Every endpoint starts with /v`<x>` in which x is the version.


## Rate-limits

* The number of API calls is limited on an hour basis accross the API
* The amount of calls differ between anonymous users and users with an [API Token](/rest-api/api-tokens/)


## Special Field Types

### Permission Field

Value | Description
:--- |  :---
``invited_read`` | Invited with read-only permission
``subscribed_read`` | Subscribed with read-only permission
``invited_write``  | Invited with read-write permission
``subscribed_write`` | Subscribed with read-write permission
``removed`` | Removed


### Transport Mode Field

Value | Description
:--- |  :---
``car`` | Travel by car
``transit`` | Travel by transit/ public transport
``bicycle`` | Travel by bicycle
``walk`` | Travel by foot

Inside trip requests combinations of several transport modes may also occur, `[transit,walk]` is for instance often used to serve door-to-door trips by public transport.

### Calendar Type Field

``private``, ``webdav``, ``ics`` & ``google``


### Location Type Field

``favorite``, ``home`` & ``work``

### Date Time Field

**Date format**

The date format that should be used is ISO-8601 extended, formatted as `YYYY-MM-DDThh:mm:ss.ssssssZ`.

An example of valid date format:

```
"2004-02-12T15:19:21:00.000000Z" // URL ENCODED: 2004-02-12T15%3A19%3A21%3A00.000000Z
```

**Timezone format**

For timezones the standard olson timezone definitions should be used (see: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

### image-URL Field

In order to cope with images being served over both secure (https) and insecure (http) connections, URL fields are expected to begin with `"://"` instead of "http://" or "https://".


## Pagination

To allow to request a limited amount of rows, it is required to send the limit and offset params 

Parameter | Type | Required | Default |Description
:--- | :--- | :--- | :--- | :--- 
limit | INT | False | 10 | Tells to the API the amount of rows that are being requested
offset | INT | False | 0 | Tells the API where to start returning records from the entire set of results. If you don't include this parameter, the default is to start at record number 0 and then return the number of records specified with the 'limit' parameter.
<br/>

### Offset, limit and count

When requesting an endpoint that supports `offset` and `limit`, the response will also contain a `count` that specifies the total amount of items that could be returned. This `count` can be used to determine whether all items have been returned, and the amount of necessary pagination needed.

By sending `offset=0&limit=0` the `count` will still be returned, allowing to only request the `count` for usecases in which the item details are not needed.

#### Max-limit

Currently the maximum value that can be set for `limit` is 100, meaning that any endpoint can only be paginated by 100 at the time. Setting the limit to any higher value will return an error.

### A note on default offset and limit

As described above, requests will default to repsonding with the first 10 items when no offset or limit are specified. To find out whether all items are returned, the count can be checked inside the meta-data send along with the request.

Furthermore, even when specifying for a specific set of items with for instance the `ids` parameter, the limit will still default to 10. If you for example retrieve `/events/ids=[01,02,03,04,05,06,07,08,08,10,11]`, only the first 10 items will be returned.

### Example:

GET /api/v1/events/?limit=42&offset=0

    {
        "data": [<event object i_0>, ..., <event object i_9>],
        "meta_data": {
            "sync_token": 142,
            "count": 42,
            "offset": 0
        }
    }

GET /api/v1/events/?limit=42&offset=10

    {
        "data": [<event object i_10>, ..., <event object i_19>],
        "meta_data": {
            "sync_token": 142,
            "count": 42,
            "offset": 10
        }
    }


## Synchronization

To make it easy to just request for resources updated since your last request you can use a `sync_token`. Within each request the `sync_token` is added to the `meta_data` object of the response. When making the next request the `sync_token` can be added to the query-parameters to request for all changes since the previous request.

Note that the `sync_token` returned is related to the current state of all the data, it's the responsibility of the client to have requested all the (paginated) data beforehand.

Also note that GET requests will return deleted resources (see [Representation of deleted resources](#representation-of-deleted-resources)), this will allow clients to know which resources have been deleted since the last request.

**Example**

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

## Query evaluation
   
### Query param format

Query parameters are automatically transformed into the specified format. So for example strings should not be surounded by quotes.

### Query evaluation

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


## Representation of deleted resources

Deleting a resource (e.g. DELETE /events/`event_id`) will only make its content inaccessible, its relationships (e.g. with users) will remain intact. This results in the resource still being returned on GET requests, but only containing its permission and id.

As the deleted resource is still returned, clients can use the information for synchronization purposes (by sending along the [Sync token](#sync-token)) or use the information to undo a deletion (if allowed).

Deleting a subscription related to a resource instead of the resource itself (e.g. DELETE /subscriptions/`subscription_id`) will result in making the content inaccessible to the user (or users, in the case of a calendar-event subscription) related to that subscription. Deleting all subscriptions related to a resource will result in the same as deleting the resource itself.

## PUT and PATCH Definitions

### PUT

A PUT call is a request to replace an object in the server. To perform this action, it is required to send (at least) all required fields having in mind the field type, the field dependencies ( e.g: start < end ). If any of these conditions are not accomplished, the request will return 400 Bad request. All non required fields that are not sent in the call won't be modified at all, leaving the previous value as it is.

### PATCH

A PATCH call is a request to change certain fields of the object in the server. To perform this action is required to send only the fields that will change it's value, having in mind the field type and the field dependencies ( e.g: start < end ). Note that setting the value of certain fields can require to send another value because the dependecy between them. ( e.g: start required the start_timezone ). All non required fields that are not sent in the call won't be modified at all, leaving the previous value as it is.
