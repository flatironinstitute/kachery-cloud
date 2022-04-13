from typing import Union
from .Feed import Feed


def create_feed(*, project_id: Union[str, None]=None):
    return Feed.create(project_id=project_id)