from typing import Optional

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hubspot.client import HubSpotStream


class CompaniesStream(HubSpotStream):
    """Companies."""

    name = "companies"
    search_path = "/crm/v3/objects/companies/search"
    # search_path = "/crm/v3/objects/companies"
    full_path = "/crm/v3/objects/companies"
    properties_object_type = "companies"
    primary_keys = ["id"]

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
        return None if self.config.get("no_search", False) else "hs_lastmodifieddate"

    @replication_key.setter
    def replication_key(self, _):
        "Just to shut Lint up"
        pass

    @property
    def path(self) -> str:
        return (
            self.full_path if self.config.get("no_search", False) else self.search_path
        )

    @path.setter
    def path(self, _):
        "Just to shut Lint up"
        pass

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        """As needed, append or transform raw data to match expected structure."""
        # Need to copy the replication key to top level so that meltano can read it
        if self.replication_key:
            row[self.replication_key] = self.get_replication_key_value(row)
        else:
            row["hs_lastmodifieddate"] = row['updatedAt']
        return row

    # def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
    #     """Return a context dictionary for child streams."""
    #     return {
    #         "id": record["id"],
    #     }
