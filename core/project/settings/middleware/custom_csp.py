from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError


class CustomCSPMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the response corresponds to an error page
        if isinstance(response, HttpResponseServerError) or isinstance(response, HttpResponseNotFound) or isinstance(
            response, HttpResponseBadRequest
        ) or isinstance(response, HttpResponseForbidden) or response.status_code == 503:

            # Apply the relaxed CSP policy for error pages
            response['Content-Security-Policy'] = (
                "default-src 'self'; img-src 'self'; style-src 'self'; script-src 'self'; "
                "font-src 'self'; object-src 'none'; frame-src 'none'; base-uri 'self'; "
                "form-action 'self'; connect-src 'self'; manifest-src 'self'; worker-src 'self'; "
                "frame-ancestors 'self'; report-uri /csp-report;"
            )

        return response
