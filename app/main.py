from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from typing import Dict, Any, List

from app.routers.compat_data import get_mdn_browser_compat_data
from app.routers.features import get_feature_list

app = FastAPI()


class FeatureRequest(BaseModel):
    feature: str


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/features")
def read_features() -> JSONResponse:
    features: List[Dict[str, str]] = get_feature_list()
    return JSONResponse(content=features)


@app.post("/mdn-browser-compat-data")
def read_mdn_browser_compat_data(request: FeatureRequest) -> JSONResponse:
    data: Dict[str, Any] | None = get_mdn_browser_compat_data(request.feature)
    if data:
        return JSONResponse(content=data)
    return JSONResponse(content={"error": "Feature not found"}, status_code=404)
