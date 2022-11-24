from django.contrib.auth.forms import UserCreationForm

from users.models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User

<<<<<<< HEAD
        fields = {"username","password1", "password2"}
=======
        fields = {"username", "password1", "password2"}
>>>>>>> b526357 (back)

