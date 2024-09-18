"""
set permission callback in template for models

"""


def permission_callback(request):
    return request.user.has_perm('change_model')
