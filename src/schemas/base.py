from pydantic import BaseModel, ConfigDict



class BaseSchemaModel(BaseModel):
    """
    Base class for all schema models.
    Contains common configuration for all schema models.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        ser_json_timedelta="iso8601",
        extra="forbid",
    )


class BaseStrictSchemaModel(BaseSchemaModel):
    model_config = ConfigDict(strict=True)
