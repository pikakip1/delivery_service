from pydantic import BaseModel, ConfigDict


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        ser_json_timedelta="iso8601",
        extra="forbid",
    )


class BaseStrictSchemaModel(BaseSchemaModel):
    model_config = ConfigDict(strict=True)
