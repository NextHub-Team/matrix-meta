from django.apps import AppConfig


class BaseAppConfig(AppConfig):
    """_summary_
    The `BaseAppConfig` class is used to set the name attribute based on the current module's name.
    """
    name = ".".join(__name__.split(".")[:-1])
