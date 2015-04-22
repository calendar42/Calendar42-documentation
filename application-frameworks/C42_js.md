# C42.js

C42.js is a classical inheritance javascript [MVC](http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) framework for easy creation of web & hybrid native applications on top of the C42 platform & APIs. Both the desktop and mobile application are developed on the same set of tools bundled under name of C42.js. This library glues together certain smaller javascript tools like persistence.js for websql, stativus.js for statechart logic and strophe.js for XMPP comunication. Plus offers the logic to authenticate and synchronise with the Calendar42 platform easily. Next to this, it contains javascript abstractions for native mobile features, such as: foreground and background tracking, calendar storage, push notifications & camera storage (iOS & Android) 

## MVC model

* (Offline) synchronizer & storage (WebSQL)
* Model
* Controller
* View
* Application state manager

## UI components

Encapsulates code to add dynamics to statically rendered HTML

Such as: 

* Modal, tab, pane, map, grid views
* Autocompletes (calendar, favourite location, members, availability, etc.)
* Date (select, change, relate, etc.), date-pickers, event-time-editors
* Activity streams (global updates)
* Event streams (personal updates)

