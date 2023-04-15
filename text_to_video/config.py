from pydantic import BaseSettings


class Settings(BaseSettings):
    artifact_dir: str = "video_artifacts"
    artifact_base_name: str = "vid"

    class Config:
        env_prefix: str = "APP_"


class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._settings = Settings()
        return cls._instance

    @property
    def settings(self) -> Settings:
        return self._settings
