from django.apps import AppConfig


class BaseAppConfig(AppConfig):
    name = ".".join(__name__.split(".")[:-1])
