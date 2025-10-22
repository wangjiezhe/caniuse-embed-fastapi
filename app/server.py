from typing import Any, Dict, List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from routers.compat_data import get_bcd_data, get_mdn_browser_compat_data
from routers.features import (
    get_caniuse_feature_list,
    get_feature_list,
    get_mdn_feature_list,
)
from utils.formatters import format_mdn_feature_title

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FeatureRequest(BaseModel):
    feature: str


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/caniuse-features")
async def read_caniuse_features() -> JSONResponse:
    features: List[Dict[str, str]] = get_caniuse_feature_list()
    return JSONResponse(content=features)


@app.get("/caniuse-raw-local")
async def read_caniuse_raw_local(req: Request) -> JSONResponse:
    env = req.scope["env"]
    response = await env.ASSETS.fetch("https://assets.local/caniuse-data.json")
    features: Dict[str, Any] = await response.json()
    return JSONResponse(content=features)


@app.get("/caniuse-raw-local-headers")
async def read_caniuse_raw_local_headers(req: Request) -> JSONResponse:
    env = req.scope["env"]
    response = await env.ASSETS.fetch("https://assets.local/caniuse-data.json")
    return response.headers


@app.get("/mdn-features")
async def read_mdn_features() -> JSONResponse:
    features: List[Dict[str, str]] = get_mdn_feature_list()
    return JSONResponse(content=features)


@app.get("/mdn-features-local")
async def read_mdn_features_local(req: Request) -> JSONResponse:
    env = req.scope["env"]
    response = await env.ASSETS.fetch("https://assets.local/mdn-data.json")
    bcd_data: Dict[str, Any] = await response.json()

    final_paths: List[List[str]] = []

    def traverse_object(obj: Dict[str, Any], obj_path: List[str]) -> None:
        for key, value in obj.items():
            new_path: List[str] = obj_path + [key]
            if "__compat" in key:
                final_paths.append(obj_path)
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

    return JSONResponse(content=features)


@app.get("/mdn-css-features-local")
async def read_mdn_css_features_local(req: Request) -> JSONResponse:
    env = req.scope["env"]
    response = await env.ASSETS.fetch("https://assets.local/mdn-css.json")
    bcd_data: Dict[str, Any] = await response.json()

    final_paths: List[List[str]] = []

    def traverse_object(obj: Dict[str, Any], obj_path: List[str]) -> None:
        for key, value in obj.items():
            new_path: List[str] = obj_path + [key]
            if "__compat" in key:
                final_paths.append(obj_path)
            else:
                traverse_object(value, new_path)

    for category, data in bcd_data.items():
        traverse_object(data, [category])

    features: List[Dict[str, str]] = []
    for path in final_paths:
        feature: Dict[str, str] = {
            "id": "mdn-" + "__".join(path),
            "title": format_mdn_feature_title(path),
            "dataSource": "mdn",
        }
        features.append(feature)

    features.sort(key=lambda x: x["title"])

    return JSONResponse(content=features)


@app.get("/mdn-raw")
async def read_mdn_raw() -> JSONResponse:
    bcd_data: Dict[str, Any] = get_bcd_data()
    return JSONResponse(content=bcd_data)


@app.get("/mdn-css")
async def read_mdn_css() -> JSONResponse:
    bcd_data: Dict[str, Any] = get_bcd_data()
    return JSONResponse(content=bcd_data["css"])


## Worker exceeded memory limit.
@app.get("/mdn-raw-local")
async def read_mdn_raw_local(req: Request) -> JSONResponse:
    env = req.scope["env"]
    response = await env.ASSETS.fetch("https://assets.local/mdn-data.json")
    mdn_data: Dict[str, Any] = await response.json()
    return JSONResponse(content=mdn_data)


@app.get("/mdn-css-local")
async def read_mdn_css_local(req: Request) -> JSONResponse:
    env = req.scope["env"]
    response = await env.ASSETS.fetch("https://assets.local/mdn-data.json")
    mdn_data: Dict[str, Any] = await response.json()
    return JSONResponse(content=mdn_data["css"])


@app.get("/mdn-css-only")
async def read_mdn_css_only(req: Request) -> JSONResponse:
    env = req.scope["env"]
    response = await env.ASSETS.fetch("https://assets.local/mdn-css.json")
    mdn_data: Dict[str, Any] = await response.json()
    return JSONResponse(content=mdn_data)


@app.get("/features")
async def read_features() -> JSONResponse:
    features: List[Dict[str, str]] = get_feature_list()
    return JSONResponse(content=features)


@app.post("/mdn-browser-compat-data")
async def read_mdn_browser_compat_data(request: FeatureRequest) -> JSONResponse:
    data: Dict[str, Any] | None = get_mdn_browser_compat_data(request.feature)
    if data:
        return JSONResponse(content=data)
    return JSONResponse(content={"error": "Feature not found"}, status_code=404)
