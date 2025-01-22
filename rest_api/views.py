"""
Views for handling IP-based tag lookups.

These views provide functionality for retrieving tags associated with a given IP address.
They offer two formats: JSON and HTML.
"""

import logging
from ipaddress import ip_address
from django.apps import apps
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest


app_config = apps.get_app_config("rest_api")
kb = app_config.knowledge_base
logger = logging.getLogger('rest_api')


def get_ip_tags_json(request: HttpRequest, ip: str) -> JsonResponse:
    """
    Retrieve tags associated with a given IP address in JSON format.

    URL:
        GET /ip-tags/<ip>

    Args:
        request (HttpRequest): The HTTP request object.
        ip (str): The IP address to look up.

    Returns:
        JsonResponse: A JSON object containing the tags associated with the given IP address.

    Examples:
        Successful Response:
            HTTP 200 OK
            [
                "tag1",
                "tag2",
                "tag3"
            ]

        Error Response:
            HTTP 400 Bad Request
            {
                "error": "Invalid IP address."
            }
    """
    try:
        user_ip = ip_address(ip)
        tags = kb.retrieve_tags_using_ip(str(user_ip))
        logger.info("Successfully retrieved tags for IP address: %s", ip)
        return JsonResponse(tags, safe=False)
    except ValueError:
        logger.warning("Invalid IP address received: %s", ip)
        return JsonResponse({"error": "Invalid IP address."}, status=400)

def get_ip_tags_report(request: HttpRequest, ip: str) -> HttpResponse:
    """
    Retrieve tags associated with a given IP address in HTML format.

    URL:
        GET /ip-tags-report/<ip>

    Args:
        request (HttpRequest): The HTTP request object.
        ip (str): The IP address to look up.

    Returns:
        HttpResponse: An HTML page containing the tags associated with the given IP address.

    Examples:
        Successful Response:
            HTTP 200 OK
            An HTML page displaying the IP and its tags.

        Error Response:
            HTTP 400 Bad Request
            An HTML page with the message "Invalid IP address".
    """
    try:
        user_ip = ip_address(ip)
        tags = kb.retrieve_tags_using_ip(str(user_ip))
        logger.info("Successfully retrieved tags for IP address: %s", ip)
    except ValueError:
        logger.warning("Invalid IP address received: %s", ip)
        return render(request, "invalid_ip_address.html", status=400)

    context = {
        "ip": ip,
        "tags": tags
    }
    return render(request, "ip_tags_report.html", context)
