# BUILTIN modules
from typing import List

from fastapi.openapi.models import Schema


# Third party modules


class ResourceSchema(Schema):
    """Representation of a  health resources response.

    :ivar name: Resource name.
    :ivar status: Resource status
    """

    name: str
    status: bool


class HealthSchema(Schema):
    """Representation of a  health response.

    :ivar name: Service name.
    :ivar status: Overall health status
    :ivar version: Service version.
    :ivar resources: Status for individual resources..
    """

    status: bool
    # version: str
    # name: str
    resources: List[ResourceSchema]
