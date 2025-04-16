# app/api/routes/api.py
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Header, HTTPException

# from app.services.grpc_service import GrpcService
from app.services.rest_service import RestService

router = APIRouter()


def get_rest_service(authorization: Optional[str] = Header(None)) -> RestService:
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    return RestService(auth_token=token)


# def get_grpc_service():
#     return GrpcService()


endpoints = {
    "users": "api/users/",
    "login": "api/auth/login/email",
    "register": "api/auth/register",
}


@router.get("/users")
async def get_users(
    rest_service: RestService = Depends(get_rest_service),
):
    try:
        rest_data = await rest_service.get_data(endpoints.get("users"))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"REST service error: {str(e)}")

    return rest_data


@router.post("/login")
async def login(
    credentials: Dict[str, Any],
    rest_service: RestService = Depends(get_rest_service),
):
    try:
        rest_result = await rest_service.post_data(
            endpoints.get("login"), data=credentials
        )
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"REST service error: {str(e)}")

    return rest_result
