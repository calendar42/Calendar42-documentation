This chapter describes the different constants that are used, both in paramaters as in the models.

# General Constants

## • Permission

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

## • Event Type

* **todo** - an unplanned event.
* **timeblock** - a time block indication. `in development`
* **normal** - a regular planned in event.
* **arrive_by** - a trip planned with the end time set as arrival time. The start-time is read-only and follows the duration needed to travel between start & end locations based on the end-time.
* **depart_from** - a trip planned with the start time set as departure time. The end-time is read-only and follows the duration needed to travel between start & end locations based on the start-time
* **route** - a trip without a start or end time and duration. `in development`

### Event types and their field dependencies

* **√** = allowed
* **x** = not allowed
* **~** = read-only

|                   | todo          | timeblock       | normal        | depart_from                             | arrive_by                                 | route                                 |
|:-------------     |:------------- |:-------------   |:------------- |:--------------------------------------  |:--------------------------------------    |:--------------------------------------|
| **start**         | x             | √`Required`     | √`Required`   | √`Required`                             | ~`calculated departure time`              | x                                     |
| **end**           | x             | √`Required`     | √`Required`   | ~`calculated arrival time`              | √`Required`                               | x                                     |
| **due_date**      | √             | √               | √             | √                                       | √                                         | √                                     |
| **start_location**| √             | √               | √             | √`Required`                             | √`Required`                               | √`Required`                           |
| **end_location**  | x             | x               | x             | √`Required`                             | √`Required`                               | √`Required`                           |

**Note on the difference between timeblock and normal events**

Though the field dependencies are similar between timeblock and normal events, the objects do have different meaning: 

* the start and end times of the timeblock are only indicative, the actual event will happen somewhere in between these times
* one single timeblock will not result into user being marked busy for that period. 
    * Only if multiple timeblocks occur in the same period a person will be marked as busy
    * This number of timeblocks is determined on a per service basis, it defaults to: the time period divided through 30 minutes.

**@todo:** ``tracked_tentative``, ``tracked_event`` & ``tracked_arrive_by``

## • RSVP Status

``null``

* You can't set attendance to this status as this is the default.

``not_replied``

* Indicating you haven't replied.

``attending``

* Indicating you're attending the event

``not_attending``

* Indicating you're not attending the event

## • Transport mode

``car``

* Travel by car

``transit``

* Travel by transit/ public transport

``bicycle``

* Travel by bicycle

``walk``

* Travel by foot

### Combining transport modes

Inside trip requests combinations of several transport modes may also occur, `[transit,walk]` is for instance often used to serve door-to-door trips by public transport.

# Calendar Constants

## • Calendar Type

**@todo:** ``private``, ``webdav``, ``ics`` & ``google``


# Location Constants

## • Location type

**@todo:** ``favorite``, ``home`` & ``work``

