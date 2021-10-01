# MeowCat2

**MeowCat** is a Python web application that will implement a federated 
blogging, microblogging, and social networking platform using the 
ActivityPub protocol.

## MeowCat's goals

To be a **blogging** and **microblogging** platform (similar to Wordpress or 
Twitter).

The ability to Meowcat to post long posts makes it most useful for more thoughtful
intellectual people -- the opposite of Twitter and Instagram in a way. This is good 
because I'm aiming at an under-served audience. The Fediverse already has 
microblogging software (Mastodon), so MeowCat will carve out a new ecological 
niche. 

MeowCat uses a varient of **Markdown** markup, with extensions for hashtags and 
wiki links. Code highlighting is enabled, making it attractive to programmers 
(another under-served audience).

MeowCat will allow **polls** on posts so users can get feedback. Each poll 
question can allow multiple answers or only one. 

Each user will be able to **upload images** which they can embed in their 
posts, replies, and wiki pages. They will also be able to embed images from 
PixelFed and videos from PeerTube. Legacy non-federated platfroms such as YouTube 
will also be supported.

MeowCat will be part of the **Fediverse** with Meowcat instances talking to each 
other and other Fediverse services using **ActivityPub**.

Each user will have their own **wiki**, their own personal web space in which 
they can create pages on whatever they want (similar to Geocities).

MeowCat will allow people to group posts based on **topics** (similar to Reddit's
subreddits). Each topic will have its own **topic-based wiki**, where users can
collaboratively create content.

Wikis can optionally be linked together on multiple instances so that any change
to the wiki on one instance is automatically copied (perhaps using a flood-fill 
algorithm) to other other instances. This would then be a distributed wiki
which would be resilient so that if one instance went down, the wiki would 
still be there.

MeowCat will allow users to send **private posts** to other users (similar to email).
When private posts travel over the internet they will be encrypted.

A long term goal of MeowCat is to allow users to get a Raspberry Pi, download 
the MeowCat software onto the Pi, spend 10 minutes configuring it though a web
interface, and then attaching the Pi to their home oureter to act as their
own social media server that thery and their friends can use, connected to
all other federated servers using ActivityPub.



## Where MeowCat is now

The current implementation is written in Python, with some client-side JavaScript.

It currently does blogging and wikis,  although you can't upload images yet. 

Connection to the Fediverse is not yet implemented.


## License

![AGPL logo](app/static/agplv3-155x51.png)

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU Affero General Public License** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the [GNU Affero General Public License](LICENSE.md) for more details.


