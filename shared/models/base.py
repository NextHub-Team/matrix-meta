from django.apps import AppConfig


class BaseAppConfig(AppConfig):
    """
    A base configuration class that sets the name attribute dynamically
    and overrides global `print` behavior based on the DEBUG setting.
    """

    name = ".".join(__name__.split(".")[:-1])
