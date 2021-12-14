from django.shortcuts import redirect


class RedirectionUnauthorizedUsersMiddleware:
    """
    Если пользователь не выполнил вход в аккаунт - ему будут доступны
    ссылки лишь на регистрацию и авторизацию.
    По умолчанию будет редирект на регистрацию.
    """

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path not in ('/registration/', '/login/'):
                return redirect('registration')
        response = self._get_response(request)
        return response
