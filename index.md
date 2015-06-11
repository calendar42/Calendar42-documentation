# Calendar42 documentation

_Note: This documentation is a work in progress, meaning things might change and you may come across some inconsistencies (or even errors). That being said, it gives direct insight in our roadmap and offers the opportunity to ask questions, give suggestions and help shape the development._

## Getting started

1. Get started with our [REST API](/rest-api/introduction/) 
2. Get started with our real-time [XMPP API](/xmpp-api/introduction/) 
3. Learn more about our [Application frameworks](/application-frameworks/introduction/)
4. Learn more about our [Services](/services/introduction/)

## About Calendar42 

Calendar42 is a planning ecosystem that distributes, enriches and profiles time related information. It communicates in real-time with end-users through our browser- & native apps, as well as our our other communication channels. We offer SMS text (not everyone one has a smartphone), transactional mail (nothing wrong with good old fashioned mailboxes) & native push notifications including custom templates & notification masks.

### The ecosystem

The Calendar42 ecosystem can be divided into three seperate layers:

* C42 Platform - accesible through our [REST API](/rest-api/introduction/) and [XMPP API](/xmpp-api/introduction/)
* C42 Applications and frameworks
* C42 Data integrations & Add-ons

Our technology stack is mainly build using: python, xmpp, zeromq, postgresql, django, ejabberd, javascript, elasticsearch, objective-c & java.

### Enabling third parties

Calendar42 has an open character on all layers and provides a fundament to create services for end-users and organisations that can do pretty much anything planning related.

1. Create custom apps to access the data within the platform.
2. Create extensions on the platform, like specific enrichment processes or interfaces to use information generated within the Calendar42 platform as input for other processes. 
3. Create interfaces to enrich your own data and allow them to become consumable through the Calendar42 apps.

### Privacy & Control

Data owners (including the end users) have full control over the accessibility of their data, can enjoy the system services (enrichments, subscriptions, notifications) and are able to monitor historic, real-time and expected usage of this data and the events they represent. 

## Plannerstack

With our non-profit initiative [Plannerstack](http://plannerstack.org) we developed and open, multimodal, real-time travel information ‘toolbox’; including real-time trip planners, high quality linked geo-coders and subscription services.

The purpose of this tool box is to enable any and all interested parties to develop and offer plug & play, dynamic and multimodal travel information services and applications. The idea is that collaboration makes innovative developments possible. Co-creation is an important factor to make new solutions possible.