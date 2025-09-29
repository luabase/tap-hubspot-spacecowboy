from typing import Optional, Any, Dict

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hubspot.client import HubSpotStream


class ArchivedCompaniesStream(HubSpotStream):
    """Archived Companies."""

    name = "archived_companies"
    full_path = "/crm/v3/objects/companies"  # full table replication, we can use the non-search endpoint
    properties_object_type = "companies"
    primary_keys = ["id"]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = {
            "archived": True,
            "limit": 100,
        }
        if next_page_token:
            params["after"] = next_page_token
        return params

    @property
    def schema(self):
        props = th.PropertiesList(
            th.Property(
                "id",
                th.StringType,
            ),
            th.Property(
                "properties",
                th.ObjectType(),
            ),
            th.Property(
                "createdAt",
                th.DateTimeType,
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
                "archivedAt",
                th.DateTimeType,
            ),
            th.Property(
                "associations",
                th.ObjectType(),
            ),
        )

        if self.replication_key:
            props.append(
                th.Property(
                    self.replication_key,
                    th.DateTimeType,
                )
            )
        else:
            props.append(
                th.Property(
                    "hs_lastmodifieddate",
                    th.DateTimeType,
                )
            )

        return props.to_dict()

    @property
    def replication_key(self) -> Optional[str]:
        # incremental replication is not supported for archived companies
        return None

    @replication_key.setter
    def replication_key(self, _):
        "Just to shut Lint up"
        pass

    @property
    def path(self) -> str:
        return self.full_path

    @path.setter
    def path(self, _):
        "Just to shut Lint up"
        pass
