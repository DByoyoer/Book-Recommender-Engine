from datetime import datetime, timezone

from typing_extensions import Annotated
from pydantic.functional_serializers import PlainSerializer

DateTimeWithoutTZ = Annotated[datetime, PlainSerializer(lambda dt: dt.astimezone(timezone.utc).replace(tzinfo=None))]