from .Feed import Feed


def load_feed(feed_id: str):
    return Feed.load(feed_id=feed_id)
