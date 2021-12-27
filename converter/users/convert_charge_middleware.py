from django.contrib.auth import get_user_model

User = get_user_model()


class ConvertChargeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Adds the authenticated user's remaining conversion charge to all responses
        if request.user.is_anonymous:
            return response
        else:
            charge_left = User.objects.get(
                username=request.user.username
            ).convert_min_left
            response["Charge-Left"] = charge_left
            return response
