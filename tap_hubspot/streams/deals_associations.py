from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hubspot.client import HubSpotStream
from tap_hubspot.streams.deals import DealsStream


class DealsAssociationsStream(HubSpotStream):
    """Deal's associations"""
    # parent_stream_type = DealsStream
    # records_jsonpath = "$[*]"

    def get_properties(self):
        return []

    request_limit = 50

    name = "deals_associations"
    path = (
        # "/crm/v4/objects/deal/{id}/?associations=companies,contacts"
        "/crm/v4/objects/deal/?associations=companies,contacts"
        "&propertiesWithHistory=hubspot_owner_id,dealstage"
    )
    properties_object_type = "deals"
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
        th.Property(
            "properties",
            th.ObjectType(),
        ),
    ).to_dict()
