import wrapt


def set_name(cls):
    """
    Decorator to set the 'name' attribute of an AppConfig subclass
    to the parent package's name plus the app's name.
    """
    # Get the module path where the AppConfig class is defined
    module_name = cls.__module__  # e.g., 'services.core.apps'

    # Remove the last part (the 'apps' module) to get the parent package
    parent_package = module_name.rpartition(".")[0]  # e.g., 'services.core'

    # Set the 'name' attribute of the AppConfig subclass
    cls.name = parent_package  # e.g., 'services.core'

    return cls


# Use wrapt to create a class decorator
def appconfig_decorator(decorator):
    """
    Converts a simple function into a class decorator compatible with wrapt.
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):  # pylint: disable=W0613
        return decorator(wrapped)

    return wrapper
