from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    WAIT_FOR_MOST_PROFIT_UPGRADES: bool = True

    AUTO_UPGRADE: bool = True

    AUTO_CLICKER: bool = True

    APPLY_DAILY_ENERGY: bool = True

    USE_PROXY_FROM_FILE: bool = False

    MIN_BALANCE: int = 1_000

    MIN_TAPS_FOR_CLICKER_IN_PERCENT: int = 60

    SLEEP_INTERVAL_BEFORE_UPGRADE: list[int] = [10, 40]

    CHECK_DAILY_COMBO: bool = True


settings = Settings()
