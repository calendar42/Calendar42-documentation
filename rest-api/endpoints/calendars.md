## • /calendars/

Supported methods:

* GET `acceptation`
* POST `development`

### GET /calendars/

Returns a default response object with a list of [Calendar](/rest-api/objects/#calendar) objects inside the data object.

#### parameters

Parameter | Required | 
--- | --- | --- 
`ids` | false | Array of calendar ids. To filter on specific events (response is not equally ordered)
`service_ids` | false | Array of service ids
`categories` | false | Array of [Calendar Category](/rest-api/objects/#calendar)
`sync_token` | false | [Sync Token](/rest-api/usage/#sync-token)
<br>

#### POST parameters

All required attributes of a [calendar](/rest-api/objects/#calendar) should be sent, and all editable params can be sent as a param

#### PATCH parameters

All editable params of a [calendar](/rest-api/objects/#calendar) can be sent as a param and it will be replaced with the new value

---------------------------------------

## • /calendars/`<calendar_id>`/

Supported methods:

* GET `acceptation`

### GET: /calendars/`<calendar_id>`/

* Returns a default response object with a list containing the requested [Calendar](/rest-api/objects/#calendar) object inside the data object.