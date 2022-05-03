from .Feed import Feed


def load_feed(feed_id_or_uri: str) -> Feed:
    return Feed.load(feed_id_or_uri)
