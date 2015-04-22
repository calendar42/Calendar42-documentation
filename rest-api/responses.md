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

**Date format**

    The date format that should be used is ISO-8601  2012-04-23T18:25:43.511Z extended.
    
    So the expected format will be: "YYYY-MM-DDThh:hh:mm:ss.sss"
    
    An example of valid date format:
    
    "2004-02-12T15:19:21+00:00" // URL ENCODED: 2015-03-24T14%3A29%3A47.613Z
    
**Timezone format**

For timezones the standard olson timezone definitions should be used (see: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

    
# Sync token
To make it easy to just request for resources updated since your last request you can use a `sync_token`. Within each request the `sync_token` is added to the `meta_data` object of the response. When making the next request the `sync_token` can be added to the query-parameters to request for all changes since the previous request.

**Example:**

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

**Example:**

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

