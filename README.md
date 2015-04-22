# The Calendar42 documentation

_Note: This documentation is a work in progress. There may be errors and inconsistencies and things will change. However, you’ll be able to gain insight into our roadmap, ask questions, give suggestions and even help shape the development._

This documentation is currently divided into two different categories:

1. **API documentation**
..* [REST](/rest-api/introduction.md)
..* [XMPP](/xmpp-api/introduction.md)
2. **[Application frameworks documentation](/application-frameworks/introduction.md)** 
..* c42.js 
..* native components
3. **[Calendar42 services](/services/introduction.md)**

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

