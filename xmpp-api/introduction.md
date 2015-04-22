# XMPP

To make sure you never miss a beat, go all the way with our real-time publish/subscribe API. 


## Introduction to XMPP

At the base of the real-time API of Calendar42 lies XMPP (the Extensible Messaging and Presence Protocol). This is a communications protocol for message-oriented middleware based on XML (Extensible Markup Language). The protocol was originally named Jabber, and was developed by the Jabber open-source community in 1999 for near real-time, instant messaging (IM), presence information, and contact list maintenance.

The core of XMPP is the exchange of small, structured chunks of information. Like HTTP, XMPP is a client-server protocol, but it differs from HTTP by allowing either side to send data to the other asynchronously. XMPP connections are long lived, and data is pushed instead of pulled.

Calendar42 implements several standard XEP's (XMPP Extension Protocol) to provide its calendar services over XMPP, these standards are developed by the XMPP Standards Foundation and can be found [online](xmpp.org/xmpp-protocols/xmpp-extensions/)

## Strengths of XMPP

* Decentralisation: The architecture of the XMPP network is similar to email; anyone can run their own XMPP server and there is no central master server.
* Open standards: The Internet Engineering Task Force has formalised XMPP as an approved instant messaging and presence technology under the name of XMPP (the latest specifications are RFC 6120 and RFC 6121). No royalties are required to implement support of these specifications and their development is not tied to a single vendor.
* History: XMPP technologies have been in use since 1999. Multiple implementations of the XMPP standards exist for clients, servers, components, and code libraries.
* Security: XMPP servers can be isolated from the public XMPP network (e.g., on a company intranet), and strong security (via SASL and TLS) has been built into the core XMPP specifications.
* Flexibility: Custom functionality can be built on top of XMPP; to maintain interoperability, common extensions are managed by the XMPP Standards Foundation. XMPP applications beyond IM include group-chat, network management, content syndication, collaboration tools, file sharing, gaming, remote systems control and monitoring, geolocation, middleware and cloud computing, VoIP and Identity services.
* Pushing Data: Instead of inefficient polling for updates, applications can instead receive notifications when new information is available. Not only does this result in many fewer requests, it also makes the latency between the time new information is available and the time the client is aware of this information nearly zero.
* Pleasing Firewalls: XMPP connections are firewall and NAT friendly because the client initiates the connection on which server-to-client communication takes place. Once a connection is established, the server can push all the data it needs to the client, just as it can in the response to an HTTP request.

## Weaknesses of XMPP

* In-band binary data transfer is inefficient: Binary data must be first base64 encoded before it can be transmitted in-band. Therefore any significant amount of binary data (e.g., file transfers) is best transmitted out-of-band, using in-band messages to coordinate.
* Stateful protocol
* More overhead than HTTP for short-lived sessions or simple requests

## XMPP over BOSH
While XMPP connections live for arbitrarily long periods of time, HTTP requests are quite short lived. In order to enable HTTP clients to also receive the data once available, XMPP takes advantage of so-called long-polling requests. This bridge is called BOSH, for Bidirectional streams Over Synchronous HTTP, which is handled by a connection manager. Essentially, BOSH helps an HTTP client establish a new XMPP session, then transports stanzas back and forth over HTTP wrapped in a special `<body>` element. It also provides some security features to make sure that XMPP sessions can’t be easily hijacked. The connection manager communicates with an XMPP server as if it were a normal client.

Sources: 

* http://en.wikipedia.org/wiki/XMPP 
* http://xmpp.org
* "Professional XMPP Programming with JavaScript and jQuery"

## Documentation

XMPP documentation [upon request](mailto:support@calendar42.com)
