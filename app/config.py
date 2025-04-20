from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "BFF Web"
    APP_PORT: int = 8080
    DEBUG: bool = False

    # REST service settings
    REST_SERVICE_BASE_URL: str = "http://localhost:8000"
    REST_SERVICE_TIMEOUT: int = 60

    # gRPC service settings
    GRPC_SERVICE_HOST: str = "localhost"
    GRPC_SERVICE_PORT: int = 50051


settings = Settings()
