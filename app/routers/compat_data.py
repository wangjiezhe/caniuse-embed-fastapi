from functools import lru_cache
from typing import Any, Dict, List, Optional

import requests

from app.constants import MDN_DATA_URL
from app.utils.formatters import format_mdn_feature_title


@lru_cache(maxsize=1)
def get_bcd_data() -> Dict[str, Any]:
    response: requests.Response = requests.get(MDN_DATA_URL)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def get_mdn_browser_compat_data(feature: str) -> Optional[Dict[str, Any]]:
    bcd: Dict[str, Any] = get_bcd_data()
    if not feature:
        return bcd

    path: List[str] = feature.split("mdn-")[1].split("__")

    obj: Dict[str, Any] = bcd
    parent: Optional[Dict[str, Any]] = None
    for i in range(len(path)):
        parent = obj
        next_obj = obj.get(path[i])
        if next_obj is None or not isinstance(next_obj, dict):
            return None
        obj = next_obj

    compat: Optional[Dict[str, Any]] = obj.get("__compat")
    if not compat:
        return None

    compat["title"] = format_mdn_feature_title(path)

    if (
        not compat.get("mdn_url")
        and parent
        and parent.get("__compat", {}).get("mdn_url")
    ):
        compat["mdn_url"] = parent["__compat"]["mdn_url"] + f"#{path[-1]}"

    return compat
