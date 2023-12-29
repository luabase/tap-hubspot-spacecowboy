from dateutil import parser
from singer_sdk.exceptions import InvalidStreamSortException
from singer_sdk.helpers._typing import to_json_compatible
PROGRESS_MARKERS = "progress_markers"
PROGRESS_MARKER_NOTE = "Note"

def increment_state(
    stream_or_partition_state: dict,
    *,
    latest_record: dict,
    replication_key: str,
    is_sorted: bool,
    check_sorted: bool,
) -> None:
    """Update the state using data from the latest record.

    Raises InvalidStreamSortException if is_sorted=True, check_sorted=True and unsorted
    data is detected in the stream.
    """
    progress_dict = stream_or_partition_state
    if not is_sorted:
        if PROGRESS_MARKERS not in stream_or_partition_state:
            stream_or_partition_state[PROGRESS_MARKERS] = {
                PROGRESS_MARKER_NOTE: "Progress is not resumable if interrupted.",
            }
        progress_dict = stream_or_partition_state[PROGRESS_MARKERS]
    old_rk_value = to_json_compatible(progress_dict.get("replication_key_value"))
    new_rk_value = to_json_compatible(latest_record[replication_key])

    """ 
    truncate states to minute, hubspot api occasionally returns records out of order by a few seconds
    despite sorting in the request. This is a workaround to compare state timestamps at the minute level
    to avoid the InvalidStreamSortException
    """
    
    if (
        old_rk_value is None
        or not check_sorted
        or parser.parse(new_rk_value).strftime("%Y-%m-%d %H:%M")
        >= parser.parse(old_rk_value).strftime("%Y-%m-%d %H:%M")
    ):
        progress_dict["replication_key"] = replication_key
        progress_dict["replication_key_value"] = new_rk_value
        return

    if is_sorted:
        msg = (
            f"Unsorted data detected in stream. Latest value '{new_rk_value}' is "
            f"smaller than previous max '{old_rk_value}'."
        )
        raise InvalidStreamSortException(msg)