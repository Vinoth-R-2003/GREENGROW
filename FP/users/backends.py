from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CaseInsensitiveModelBackend(ModelBackend):
    """
    Custom authentication backend to make username matching case-insensitive
    (e.g., VINOTHR, vinothr, and Vinothr will all match the same account).
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if not username or not password:
            return None

        try:
            try:
                user = UserModel._default_manager.get(**{
                    f"{UserModel.USERNAME_FIELD}__iexact": username
                })
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
                return None
            except UserModel.MultipleObjectsReturned:
                user = UserModel._default_manager.filter(**{
                    f"{UserModel.USERNAME_FIELD}__iexact": username
                }).first()

            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return super().authenticate(request, username=username, password=password, **kwargs)
        return None
