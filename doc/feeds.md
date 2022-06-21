# Feeds (append-only logs)

> :warning: This project is in BETA.

> **IMPORTANT**: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

You can create a feed, append messages to it, and listen for those messages in real time on a different computer.

## Basic usage

```python
import kachery_cloud as kcl

# Create a feed in the cloud
feed = kcl.create_feed()

# get the feed URI for loading later or on a different device
uri = feed.uri
print(uri)
kcl.set_mutable_local('test/feed_uri', uri)

# Append a message to the feed
feed.append_message({'message': 1})

# Or append multiple messages
feed.append_messages([{'message': 2}, {'message': 3}])

# Load the feed
feed2 = kcl.load_feed(uri)

# Get the messages
messages = feed2.get_next_messages()
# [{'message': 1}, {'message': 2}, {'message': 3}]

# You can also listen for new messages
# even on a different computer
while True:
    messages = feed2.get_next_messages(timeout_sec=30)
    print(messages)
```

Leave this program running. Open a new terminal and append a message to this feed

```python
import kachery_cloud as kcl

uri = kcl.get_mutable_local('test/feed_uri')
feed = kcl.load_feed(uri)

feed.append_message({'test': 'message'})
```

You should see the message appear on the first terminal.

Of course this works on remote computers, but you will need to communicate the feed URI, since the remote machine will not have access to the local mutable.