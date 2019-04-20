from django.shortcuts import render
import re

def mobile(request):
    """Return True if the request comes from a mobile device."""

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


def check_if_mobile(request):
    if mobile(request):
        is_mobile = True
    else:
        is_mobile = False

    return is_mobile