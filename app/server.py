from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from routers.compat_data import get_bcd_data, get_mdn_browser_compat_data
from routers.features import (
    get_caniuse_feature_list,
    get_feature_list,
    get_mdn_feature_list,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


class FeatureRequest(BaseModel):
    feature: str


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/caniuse-features")
async def read_caniuse_features() -> JSONResponse:
    features: List[Dict[str, str]] = get_caniuse_feature_list()
    return JSONResponse(content=features)


@app.get("/mdn-features")
async def read_mdn_features() -> JSONResponse:
    features: List[Dict[str, str]] = get_mdn_feature_list()
    return JSONResponse(content=features)


@app.get("/mdn-raw")
async def read_mdn_raw() -> JSONResponse:
    features: Dict[str, Any] = get_bcd_data()
    return JSONResponse(content=features)


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
