from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hubspot.client import HubSpotStream
from tap_hubspot.streams.tickets import TicketsStream

class TicketsAssociationsStream(HubSpotStream):
    """Ticket's associations."""
    parent_stream_type = TicketsStream
    records_jsonpath = "$[*]"

    def get_properties(self):
        return []

    request_limit = 50

    name = "tickets_associations"
    path = (
        "/crm/v4/objects/tickets/{id}/?associations=companies,contacts"
        "&propertiesWithHistory=hubspot_owner_id"
    )
    properties_object_type = "tickets"
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
