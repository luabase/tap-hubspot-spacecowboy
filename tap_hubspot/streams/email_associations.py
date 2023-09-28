from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hubspot.client import HubSpotStream


class EmailAssociationsStream(HubSpotStream):
    """Email's associations."""

    def get_properties(self):
        return []

    request_limit = 50

    name = "email_associations"
    path = (
        "/crm/v4/objects/email/?associations=contacts"
        "&propertiesWithHistory=hubspot_owner_id"
    )
    properties_object_type = "emails"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
        ),
        th.Property(
            "updatedAt",
            th.DateTimeType,
        ),
        th.Property(
            "archived",
            th.BooleanType,
        ),
        th.Property(
            "associations",
            th.ObjectType(),
        ),
        th.Property(
            "propertiesWithHistory",
            th.ObjectType(),
        ),
    ).to_dict()