# The Calendar42 documentation

_Note: This documentation is a work in progress. There may be errors and inconsistencies and things will change. However, you’ll be able to gain insight into our roadmap, ask questions, give suggestions and even help shape the development._

This documentation is currently divided into two different categories:

1. **API documentation** (including REST and XMPP)
2. **Application frameworks documentation** (including c42.js and our native components)

## Introduction to Calendar42 

The planning hub of Calendar42 is an information funnel that distributes, enriches and profiles time related information. This information will be communicated, in real-time, to end-users on a publish/subscription base through a browser- or native applications as well as through one of our other communication channels. We offer SMS text (not everyone one has a smartphone), transactional mail (nothing wrong with good old fashioned mailboxes) & native push notifications including custom templates & notification masks.

The Calendar42 platform and technologies provide a fundament to create services for end users and organisations. Our technology stack is mainly build with the following elements: python, xmpp, zeromq, postgresql, django, ejabberd, javascript, elasticsearch, objective-c & java.

The platform can be divided into three separate layers. 
* C42 Applications/frameworks
* C42 Platform
* C42 Data integrations & Add-ons 

Data owners (including the end users) have full control over the accessibility of their data, can enjoy the system services (enrichments, subscriptions, notifications) and are able to monitor historic, real-time and expected usage of this data and the events they represent. 

The Calendar42 platform has an open character on all three levels, enabling third parties to develop their own solutions within the ecosystem of Calendar42: 

1. Creation of alternative or tailor-made applications to access the data within the platform with the Calendar42 hybrid & javascript application frameworks
2. Creation of extensions to the platform, like specific enrichment processes or interfaces to use information generated within the Calendar42 platform as input for other processes. Using our API, you can make Calendar42 do pretty much anything planning related you want with the Calendar42 REST API. To make sure you never miss a beat, developers can go all the way with our real-time publish/subscribe API. 
3. Creation of interfaces to allow their own data to become consumable through the Calendar42 platform.

With our non-profit initiative [Plannerstack](http://plannerstack.org) we developed and open, multimodal, real-time travel information ‘toolbox’; including real-time trip planners, high quality linked geo-coders and subscription services. The purpose of this tool box is to enable any and all interested parties to develop and offer plug & play, dynamic and multimodal travel information services and applications. The idea is that collaboration makes innovative developments possible. Co-creation is an important factor to make new solutions possible.

## Calendar42 services

On top of the full platform experience, you might want to use specific parts of the Calendar42 platform, such as:

### Chat bots
XMPP (jabber) based chat bots, extended to support set_items in order to chat with the different resources within Calendar42 (events, users, groups, services, ...)

### Activity stream
This is an endpoint where clients can sync all the activities they missed when they were offline.

### Async notifier
Custom bots based on IFTTT (IF This, Then That) business rules.

### Calendaring
* Google calendar sync: two-way sync system between Google Calendar and Calendar42.
* ICS importer including timezone normaliser
* WebDAV storage

### Spatial enricher
It's a service that both translates addresses into geo_positions (geocoding) and geo_positions into addresses (reverse geocoding).

### Tripplanning
It's a real-time trip planning service that "smartly" creates trips (car, public transport, etc.) based on where Calendar42 thinks you want to come from/go to either by using your events that explicitly state it or by fetching it from your current position or home/work locations. Trips are actively monitored for real-time updates.

### Position tracking
Position interpreter: This bot interprets user locations in real-time in order to know where the user might be. The objective is to automatically create events for users based on 
* planned events
* favourite locations
* events of peers (social network)
* favourite locations of peers (social network)

