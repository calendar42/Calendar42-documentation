# search

Search provides smart search functionality to the C42 authorized user. Currently it only searches for events in events and related locations and users for words, postal codes, etc. It supports AND and OR as keywords (but not NOT yet). Results are returned including the objects where matches are found and the search term resulting in the match (for e.g. highlighting purposes).

###endpoint

```
GET /v2/search/events/
```
### Authorization

Server side *API Token* or *Authentication Action Token*

### Query Parameters

Name | Type | Description
:--- | :--- | :---
`q` | string |  search terms to be searched for.  
`from_time` | datetime string | lower bound for the end time of the event
`to_time` | datetime string | upper bound for the start time of the event
`limit` | int | number of results returned; currently maxed out at 10 
`offset` | int | offset inside entire set of results (default: 0)

**Operators**

The 'q' parameter allows for AND and OR; which will be evealuated in order. AND is the default (space means AND).

**Notes**

 - events partially in the from_time/to_time interval will be included in the search result.

### Results

**fields searched**
 - In the event: 'title' and 'description' 
 - In the event related 'start_location' (the only location of a normal event): 'text', 'address', 'city', 'postcode' 
 - In the users subscribed to the event: 'first_name' and 'last_name' 

**format**

```
{
  "meta_data": {
    "count": 8
  },
  "data": [
  {
    {
      "object_type": "event",
      "object": { # see GET events docs
        ...,
        "title": "Dinner at Charlie's",
        ...
        "start_location": { # see GET location docs
          ...,
          "city": "Laren",
          ...
        },
      },
      "matches": [
        {
          "key": "title"
          "values": [
            "Dinner"
          ],
        },
        {
          "key": "start_location.city",
          "values": [
            "Laren"
          ]
        }
      ],
      "matched_related_objects": [
        {
          "object_type": "event-subscription",
          "object": { # see GET event-subscription docs
            ...,
            "first_name": "John",
            ...
          },
          "matches": [
            {
              "key": "subscriber.first_name"
              "values": [
                "John"
              ],
            }
          ]
        }
      ]
    }
  ]
}
```

**Search-specific fields**
 - `object_type`: type of the object returned
 - `object`: the object where a match was found, either directly or through some queried relation
 - `matched_related_objects`: list of objects in which matched to the search terms were found
 - `matches`: list of keys and value lists described below
 - `key`: relative point separated location of the field in which yhe match was found
 - `values`: value of the match the fields, corresponing to one og the search terms.

Other parts of the results can be found in the corresponding docs for get events, get location, get event-subscription.

### example

```
GET: /search/events/?q=John OR Eric&from_time=2015-03-24T14:29:47.613Z&to_time=2015-03-26T14:29:47.613Z&limit=5&offset=0
```
