from defender import utils
from defender.models import AccessAttempt
# import models
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login

# init user model
User = get_user_model()


class APIService:

    @staticmethod
    def get_access_attempts(request):
        # init attempt
        attempt_left = settings.DEFENDER_LOGIN_FAILURE_LIMIT

        # init counter
        # get user
        user_request_ip = utils.get_ip(request)

        # init failed attempt counter
        attempt_counter = 0

        # get last successful login
        if AccessAttempt.objects.filter(ip_address=user_request_ip, login_valid=True).exists():
            last_successful_login = AccessAttempt.objects.order_by('-attempt_time').filter(
                ip_address=user_request_ip, login_valid=True
            )[0]

            # total failed login since last success login
            total_failed_attempts_success_login = AccessAttempt.objects.filter(
                ip_address=user_request_ip, login_valid=False, attempt_time__gt=last_successful_login.attempt_time
            )

            # set counter
            attempt_counter = len(total_failed_attempts_success_login)

        elif AccessAttempt.objects.filter(ip_address=user_request_ip, login_valid=False).exists():
            # total failed login since last success login
            total_failed_attempts_success_login = AccessAttempt.objects.filter(
                ip_address=user_request_ip, login_valid=False
            )

            # set counter
            attempt_counter = len(total_failed_attempts_success_login) + 1

        # get attempts left
        attempt_left = attempt_left - attempt_counter if attempt_counter <= 3 else 0

        # return updated count
        return attempt_left

    @staticmethod
    def auth_login_user(request, email, password):

        # authenticate user credentials
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # reset defender if user is blocked already
            if utils.is_already_locked(request, username=email):
                # get the user ip using defender
                defender_user_ip = utils.get_ip(request=request)
                # reset
                utils.reset_failed_attempts(ip_address=defender_user_ip, username=email)
                utils.unblock_username(username=email)
                utils.unblock_ip(ip_address=defender_user_ip)

            # login is successful, login user
            login(request, user)

            # add login attempt
            utils.add_login_attempt_to_db(request, username=email, login_valid=True)
        else:
            # add login attempt
            utils.add_login_attempt_to_db(request, username=email, login_valid=False)

        # return login message
        return user

    @staticmethod
    def get_current_user(request):
        # get current user
        found_user = None

        if request.user.is_authenticated:
            found_user = User.objects.get(email=request.user.email)
        return found_user
