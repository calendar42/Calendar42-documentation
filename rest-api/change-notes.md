# Change Notes

<!-- MarkdownTOC -->

- [2015-09-07](#2015-09-07)
- [2015-08-15](#2015-08-15)

<!-- /MarkdownTOC -->


## 2015-09-07

**FEATURES**

* New endpoint to [get](/rest-api/endpoints/events/#get-eventsevent_idtime-block-suggestions) and [patch](/rest-api/endpoints/events/#patch-eventsevent_idtime-block-suggestions) time-block-suggestions
* Added authorization through ActionTokens, next to normal Tokens ([docs](/rest-api/introduction/#action-tokens-actiontoken))
* /event-subscriptions
	* Added filter on `service_ids`, returns subscriptions of events which are in calendars related to the given services (also returns the belonging tags of the subscribers)

**BUGFIXES**

* /events endpoint
	* Now correctly defaults the `modified` and `created` date to current date time
	* Now allows to actually set the `source_url`
* /event-subscriptions
	* Now correctly defaults to to subscribe_(read/write) when setting rsvp to `attending`


## 2015-08-15

**FEATURES**

* New event type `time_block` ([docs](/rest-api/objects/#eventevent_type))
* New event field `due` ([docs](/rest-api/objects/#event))
* New event GET parameter `order_by` option `due` ([docs](/rest-api/endpoints/events/#get-events))
* New event GET parameter `order_asc`: true (default) / false ([docs](/rest-api/endpoints/events/#get-events))

**BUGFIXES**

* GET events endpoint now correctly returns the ordering when combined with pagination (limit & offset)