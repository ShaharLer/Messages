# Messages

## Overview
A Rest API backend system that responsible of handling messages between users.
The API offers the following APIs:

* API #1) Write message
* API #2) Get all messages for a specific user
* API #3) Get all unread messages for a specific user
* API #4) Read message
* API #5) Delete message

#### The following rules are applied to the API:
* A user must be first created
* Each message must have a sender, a receiver, a non-empty subject and a non-empty message content
* A message can be deleted only by the sender or the receiver

## HTTP requests
The following HTTP methods are supported:

```POST``` **/users/**

  * **Target**: Create a user

  * **Usage**: Requires body request with the following fields: 
    - **name** (String)
    
  * **Example**:
    {"name" : "anonymus"}

```GET``` **/users/**

  * **Target**: Fetch all users

```GET``` **/users/{user_id}/**

  * **Target**: Fetch the user with the given id

```POST``` **/messages/**

  * **Target**: Create a message

  * **Usage**: Requires body request with the following fields: 
    - **sender** (id of an existed user)
    - **receiver** (id of an existed user)
    - **subject** (non-empty String)
    - **message** (non-empty String)
  
  * **Example**:
    {"sender" : 1, "receiver" : 2, "subject" : "Subject1", "message" : "Message1"}
    
```GET``` **/messages/**

  * **Target**: Fetch all users
  
```GET``` **/messages/{message_id}**

  * **Target**: Fetch the message with the given id
  
```DELETE``` **/messages/:message_id**

  * **Target**: Delete a message with the given id
  
  * **Usage**: Requires body request with the following fields: 
    - **user** (id of either the sender or the receiver of the message)
    
```GET``` **/all-messages/{user_id}**

  * **Target**: Returns all the messages that were sent for the user with the given id

```GET``` **/unread-messages/{user_id}**

  * **Target**: Returns all the unread messages that were sent for the user with the given id

```GET``` **/read-messages/{message_id}**

  * **Target**: Read the message with the given id (mark it as read in the DB)

  
    





