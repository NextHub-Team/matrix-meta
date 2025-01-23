from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.cache import cache_page


@cache_page(60 * 10)
def sample_api(request):
    """ "tets api view"""
    cached_data = cache.get("expensive_data")
    if not cached_data:
        data = {"message": "Hello! This is a cached API response."}
        cache.set("expensive_data", data, timeout=60 * 10)
    else:
        data = cached_data
    return JsonResponse(data)


def health_check(request):
    return JsonResponse({"healthy": True})