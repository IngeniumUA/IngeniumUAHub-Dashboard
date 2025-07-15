from app.settings import settings, EnvironmentEnum


async def ingress_on_startup():
    if settings.azure_dpu_storage_key is None:
        # If the storage key is none, we need to be in production environment
        if settings.running_environment.value != EnvironmentEnum.production.value:
            return
    # todo attempt to ingress parquet files

async def egress_on_shutdown():
    if settings.azure_dpu_storage_key is None:
        # If the storage key is none, we need to be in production environment
        if settings.running_environment.value != EnvironmentEnum.production.value:
            return
    # todo attempt egress to parquet files
