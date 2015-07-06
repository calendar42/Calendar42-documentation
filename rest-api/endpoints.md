Within Calendar42 the data is organized in the following types:

* **[Service](#service)**
* **[Calendar](#calendar)** - ([REST API Endpoint](/rest-api/endpoints/calendars/))
* **[Event](#event)** - ([REST API Endpoint](/rest-api/endpoints/events/))
* **[Location](#location)** - ([REST API Endpoint](/rest-api/endpoints/locations/))
* **[User](#user)**
* **[Event-Subscription](#event-subscriptions)**
* **[Calendar-Subscription](#calendar-subscriptions)**
* **[Position](#positions)**

```
    @todo: create a diagram depicting the different relationships
```

## Detailed Data Types

### Service

**Encapsulated data within C42**

Within the platform of C42 services can be created that make use of a subset of data. This subset can contain:

* users
* calendars
* events
* locations

### Calendar

**A (shared) collection of events**

### Event

```
    @todo
```

### Location

```
    @todo
```

### User

```
    @todo
```

### Event-Subscription

```
    @todo
```

### Calendar-Subscription

```
    @todo
```

### Position

```
    @todo
```

## Endpoints overview

* In production
    * /calendars
		* GET - To retrieve a list of calendars
		* GET by id - To retrieve a specific calendar 
    * /events
		* GET - To retrieve a list of events
		* GET by id - To retrieve a specific event 
    * /event/trip-suggestions
		* GET - To retrieve trip suggestions from A to B
    * /locations
		* GET - To retrieve a list of locations
		* GET by id - To retrieve a specific location 
* In acceptation
    * /events
		* POST
		* PUT
		* PATCH
		* DELETE
* In development
    * /event-subscription
		* POST
		* PUT
		* PATCH
		* DELETE
		* GET
		* GET by id
    * /action-tokens
		* GET by id
    * /events/time-slot-suggestions
		* GET
		* PATCH
    * /services
		* GET by id - To retrieve the public assets related to a service
* In future
    * /positions
    * /users
    * /calendar-subscription
