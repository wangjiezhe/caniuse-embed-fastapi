from typing import Any, Dict, List

import requests

from app.utils.formatters import format_mdn_feature_title


def get_mdn_data() -> List[Dict[str, str]]:
    MDN_DATA_URL: str = "https://unpkg.com/@mdn/browser-compat-data/data.json"
    response: requests.Response = requests.get(MDN_DATA_URL)
    response.raise_for_status()  # Raise an exception for HTTP errors
    bcd_data: Dict[str, Any] = response.json()

    final_paths: List[List[str]] = []

    def traverse_object(obj: Dict[str, Any], obj_path: List[str]) -> None:
        for key, value in obj.items():
            new_path: List[str] = obj_path + [key]
            if "__compat" in value:
                final_paths.append(new_path)
            else:
                traverse_object(value, new_path)

    excluded_categories: List[str] = ["__meta", "browsers", "webdriver", "webassembly"]

    for category, data in bcd_data.items():
        if category in excluded_categories:
            continue
        traverse_object(data, [category])

    features: List[Dict[str, str]] = []
    for path in final_paths:
        feature: Dict[str, str] = {
            "id": "mdn-" + "__".join(path),
            "title": format_mdn_feature_title(path),
            "dataSource": "mdn",
        }
        features.append(feature)

    return features


def get_can_i_use_data() -> List[Dict[str, str]]:
    CAN_I_USE_URL: str = "https://cdn.jsdelivr.net/gh/Fyrd/caniuse@master/fulldata-json/data-2.0.json"
    response: requests.Response = requests.get(CAN_I_USE_URL)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data: Dict[str, Any] = response.json()

    features: List[Dict[str, str]] = []
    for key, value in data["data"].items():
        feature: Dict[str, str] = {
            "id": key,
            "title": value["title"].capitalize(),
            "dataSource": "caniuse",
        }
        features.append(feature)

    return features


def get_feature_list() -> List[Dict[str, str]]:
    mdn_features: List[Dict[str, str]] = get_mdn_data()
    ciu_features: List[Dict[str, str]] = get_can_i_use_data()
    features: List[Dict[str, str]] = mdn_features + ciu_features
    features.sort(key=lambda x: x["title"])
    return features
