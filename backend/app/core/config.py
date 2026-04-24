from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Read from environment first, then from .env file (extra="ignore")
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db_secret: str  # injected JSON from AWS
    db_endpoint: str
    db_name: str
    redis_host_port: str
    redis_secret: str
    jwt_secret: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"

    # We use this format so that we can autogenerate creds through Terraform / AWS
    @property
    def database_url(self) -> str:
        import json
        from urllib.parse import quote_plus

        db = json.loads(self.db_secret)

        # We HAVE to have proper quoting because generated pword can have symbols
        username = quote_plus(db["username"])
        password = quote_plus(db["password"])

        return (
            f"postgresql://{username}:{password}" f"@{self.db_endpoint}/{self.db_name}"
        )

    @property
    def secret_key(self) -> str:
        import json

        secret_dict = json.loads(self.jwt_secret)
        # This should FAIL if not loaded.
        return secret_dict["secret_key"]

    @property
    def redis_url(self) -> str:
        import json

        redis_secret_dict = json.loads(self.redis_secret)
        key = redis_secret_dict["secret_key"]
        return f"redis://:{key}@{self.redis_host_port}"


settings = Settings()
