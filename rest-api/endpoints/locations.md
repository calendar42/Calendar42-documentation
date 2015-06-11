## • /locations/

Supported methods:

* GET `acceptation`

### GET /locations/

Returns a default response object with a list of [Location](/rest-api/objects/#location) objects inside the data object.

As depicted, [Location](/rest-api/objects/#location) objects may contain one or more labels that add extra details to the location. These labels add extra context for a user or a service. It may for instance mark the location as a work location for the requesting user, or contain service specific details.

When requesting the `/locations/` without any parameters, it will return all locations available in the system, ordered by most used by the requesting user.

#### Parameters

Parameter | Required | Description
--- | --- | --- 
`ids` | false | Array of location ids. To filter on specific locations (reponse is not equally ordered)
`sync_token` | false | [Sync Token](/rest-api/usage/#sync-token)
`user_ids` | false | Array of service ids. Only return locations that have labels in relation to user
`service_ids` | false | Array of service ids. Only return locations that have labels in relation to the service
`search_pattern` | false | String to match on in location text, address, city and label
`location_types` | false | Array of [Location Type](/rest-api/constants/#location-type)
`geo_circles` | false | Array of [Geo Circle]
`geo_polylines` | false | Array of [GeoPolyline](https://developers.google.com/maps/documentation/utilities/polylinealgorithm)
<br>

Note: doesn't support order_by=distance yet

#### Example 

**@todo:** Add example usage

---------------------------------------

## • /locations/`<location_id>`/

Supported methods:

* GET `acceptation`

### GET: /locations/`<location_id>`/

* Returns a default response object with a list containing the requested [Location](/rest-api/objects/#location) object inside the data object