from storages.backends.azure_storage import AzureStorage
from settings import MEDIAFILES_LOCATION, STATICFILES_LOCATION


class AzureStaticStorage(AzureStorage):
    location = STATICFILES_LOCATION
    file_overwrite = False

class AzureMediaStorage(AzureStorage):
    location = MEDIAFILES_LOCATION
    file_overwrite = False