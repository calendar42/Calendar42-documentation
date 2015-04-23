# Calendar42 services

On top of the full platform experience, you might want to use specific parts of the Calendar42 platform, such as:

## Chat bots

[XMPP](http://xmpp.org/) ([jabber](https://www.ejabberd.im/)) based chat bots, extended to support set_items in order to chat with the different [objects](/rest-api/objects/) within Calendar42 (events, users, groups, services, ...)

## Activity stream
This is an endpoint where clients can sync all the activities they missed when they were offline.

## Async notifier
Custom bots based on IFTTT (IF This, Then That) business rules.

## Calendaring
* Google calendar sync: two-way sync system between Google Calendar and Calendar42.
* ICS importer including timezone normaliser
* WebDAV storage

## Spatial enricher
It's a service that both translates addresses into geo_positions (geocoding) and geo_positions into addresses (reverse geocoding).

## Tripplanning
It's a real-time trip planning service that "smartly" creates trips (car, public transport, etc.) based on where Calendar42 thinks you want to come from/go to either by using your events that explicitly state it or by fetching it from your current position or home/work locations. Trips are actively monitored for real-time updates.

## Position tracking
Position interpreter: This bot interprets user locations in real-time in order to know where the user might be. The objective is to automatically create events for users based on 
* planned events
* favourite locations
* events of peers (social network)
* favourite locations of peers (social network)

## Notifications
So what are are notifications? Coming from a Calendar42 state of mind, you might simply think of it as "anything that isn’t bulk". Basically, it's a message sent to an individual based on a trigger or action.
 
We offer

* SMS text
* transactional mail  
* native push notifications 

All notifications come including custom templates & notification masks.