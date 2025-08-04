"""HubSpot tap class."""

from typing import List
import logging
import requests
from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers
from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.helpers.capabilities import (
    CapabilitiesEnum,
    PluginCapabilities,
    TapCapabilities,
)

from tap_hubspot.streams.archived_companies import ArchivedCompaniesStream
from tap_hubspot.streams.calls import CallsStream
from tap_hubspot.streams.companies import CompaniesStream
from tap_hubspot.streams.company_associations import CompanyAssociationsStream
from tap_hubspot.streams.contact_associations import ContactAssociationsStream
from tap_hubspot.streams.contacts import ContactsStream
from tap_hubspot.streams.deals import DealsStream
from tap_hubspot.streams.deals_associations import DealsAssociationsStream
from tap_hubspot.streams.deals_pipelines import DealsPipelinesStream
from tap_hubspot.streams.emails import EmailsStream
from tap_hubspot.streams.meetings import MeetingsStream
from tap_hubspot.streams.notes import NotesStream
from tap_hubspot.streams.owners import OwnersStream
from tap_hubspot.streams.task_associations import TaskAssociationsStream
from tap_hubspot.streams.tasks import TasksStream
from tap_hubspot.streams.tickets import TicketsStream
from tap_hubspot.streams.tickets_associations import TicketsAssociationsStream
from tap_hubspot.streams.tickets_pipelines import TicketsPipelinesStream
from tap_hubspot.streams.email_associations import EmailAssociationsStream

STREAM_TYPES = [
    ArchivedCompaniesStream,
    CompaniesStream,
    ContactsStream,
    DealsStream,
    DealsPipelinesStream,
    OwnersStream,
    TicketsStream,
    TicketsPipelinesStream,
    # Doing engagements last since
    # they are most likely to run into limits
    CallsStream,
    EmailsStream,
    MeetingsStream,
    TasksStream,
    NotesStream,
    # Associations
    DealsAssociationsStream,
    CompanyAssociationsStream,
    ContactAssociationsStream,
    TaskAssociationsStream,
    TicketsAssociationsStream,
    EmailAssociationsStream,
]


class TapHubSpot(Tap):
    """HubSpot tap class."""

    name = "tap-hubspot"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "hapikey",
            th.StringType,
            required=True,
            description="HubSpot private app token",
        ),
        th.Property(
            "start_from",
            th.DateTimeType,
            required=False,
            description="Starts incremental stream from this updated timestamp",
        ),
        th.Property(
            "no_search",
            th.BooleanType,
            required=False,
            default=False,
            description=(
                "Set to True to avoid using the search API"
                " - implies full table replication"
            ),
        ),
        th.Property(
            "batch_size",
            th.IntegerType,
            required=False,
            default=1_000_000,
            description="Size of batch files",
        ),
        th.Property(
            "batch_config",
            th.ObjectType(
                th.Property(
                    "encoding",
                    th.ObjectType(
                        th.Property("format", th.StringType, required=False),
                        th.Property("compression", th.StringType, required=False),
                    ),
                    required=False,
                ),
                th.Property(
                    "storage",
                    th.ObjectType(
                        th.Property("root", th.StringType, required=False),
                        th.Property(
                            "prefix",
                            th.StringType,
                            required=False,
                        ),
                    ),
                    required=False,
                ),
            ),
            required=False,
        ),
    ).to_dict()

    def test_stream_access(self, stream: Stream) -> bool:
        """Test if stream is accessible with API scopes.

        Args:
            stream (Stream): The stream to test.
        """
        stream_path = stream.full_path if hasattr(stream, "full_path") else stream.path
        url = stream.url_base + stream_path
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['hapikey']}",
        }
        response = requests.get(url, headers=headers)
        return response.status_code == 200

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        accessible_streams = []
        for stream_class in STREAM_TYPES:
            if self.test_stream_access(stream_class):
                logging.info(f"Stream {stream_class.name} is accessible")
                accessible_streams.append(stream_class(tap=self))
            else:
                logging.warning(
                    f"Stream {stream_class.name} is not accessible, skipping..."
                )
        if len(accessible_streams) == 0:
            raise Exception(
                "No accessible streams found, please check your API key and scopes."
            )
        logging.info(
            f"Discovered {len(accessible_streams)} accessible streams. Streams: {', '.join([stream.name for stream in accessible_streams])}"
        )
        return accessible_streams

    @classproperty
    def capabilities(self) -> List[CapabilitiesEnum]:
        """Get tap capabilities.

        Returns:
            A list of capabilities supported by this tap.
        """
        return [
            TapCapabilities.CATALOG,
            TapCapabilities.STATE,
            TapCapabilities.DISCOVER,
            PluginCapabilities.ABOUT,
            PluginCapabilities.STREAM_MAPS,
            PluginCapabilities.FLATTENING,
            PluginCapabilities.BATCH,
        ]
