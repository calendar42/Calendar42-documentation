# positions

The *Positions* endpoint allows to store positions related with the requestor.

The position object is an abstraction of the position the user smartphone took in a certain time. This abstraction allows to provide of the information about speed, accuracy, the point_type, etc. without distinction between devices type. (Android/iOS)

###endpoint

```
POST /v2/positions/
```
### Authorization

Server side *API Token* or *Authentication Action Token*

### Parameters

**Mandatory parameters**

Name | Type | Description
:--- | :--- | :---
`latitude` | float | Latitude of the position
`longitude` | float | Longitude of the endpoint
`timestamp` | datetime | The string representing the moment
`source` | string | Label to define which source is providing of the information. Currentlu only `arthur`, `marvin` or `tracker` values are accepted

**Optional parameters**

Name | Type | Description
:--- | :--- | :---
`accuracy` | integer | Accuracy in which the position was taken (**Meters**)
`speed` | integer | Speed provided by the device (**meters/second**)
`altitude` | float | Altitude provided by the device (**Meters**)
`point_type` | string | Label provided to specify the type of point we are save

**Implementation notes**

* Currently this is a closed endpoint only accessible under specific request to the C42 team.

### Response

```
Status-Code: 200 OK
```

```
{{
  "meta_data": {},
  "data": {
    "success": true
  }
}
```
