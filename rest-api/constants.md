This chapter describes the different constants that are used, both in paramaters as in the models.

# General Constants

## Permission

``invited_read``

* Invited with read-only permission

``subscribed_read``

* Subscribed with read-only permission

``invited_write`` 

* Invited with read-write permission

``subscribed_write``

* Subscribed with read-write permission

``removed``

* Removed


# Event Constants

## Event Type

``normal``

* A normal event: has one location and both start & end time that can be freely set

``arrive_by``

* A trip: has extra (end-) location. The start-time is read-only and follows the duration needed to travel between start & end locations based on the end-time

``depart_from``

* A trip: has extra (end-) location. The end-time is read-only and follows the duration needed to travel between start & end locations based on the start-time

``route``

* A trip: has extra (end-) location. Both start and end-time are not set.

**@todo:** ``todo``, ``tracked_tentative``, ``tracked_event`` & ``tracked_arrive_by``

## RSVP Status

``not_replied``

* You cant set attendance to this number this is the default, is interpreted as not-attending

``attending``

* Indicating you're attending the event

``not_attending``

* Indicating you're not attending the event

## Transport mode

``car``

* Travel by car

``public_transport``

* Travel by public transport

``bicycle``

* Travel by bicycle


# Calendar Constants

## Calendar Type

**@todo:** ``private``, ``webdav``, ``ics`` & ``google``


# Location Constants

## Location type

**@todo:** ``favorite``, ``home`` & ``work``

