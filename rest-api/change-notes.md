## 2015-08-15

**FEATURES**

* New event type `time_block` ([docs]((/rest-api/objects/#eventevent_type)))
* New event field `due` ([docs]((/rest-api/objects/#event)))
* New event GET paramater `order_by` option `due` ([docs]((/rest-api/endpoints/events/#get-events)))
* New event GET paramater `order_asc`: true (default) / false ([docs]((/rest-api/endpoints/events/#get-events)))

**BUGFIXES**

* GET events endpoint now correctly returns the ordering when combined with pagination (limit & offset)