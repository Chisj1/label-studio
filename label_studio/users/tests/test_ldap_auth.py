import pytest
from django.contrib.auth import get_user_model
from django import forms

from users.forms import LoginForm

User = get_user_model()


@pytest.mark.django_db
def test_ldap_login_success(settings):
    """Successful login when LDAP authentication returns a user."""
    user = User.objects.create_user(username="ldapuser", email="ldap@example.com", password="pass")

    def fake_user_auth(user_model, username, password):
        if username == "ldapuser" and password == "pass":
            return user
        return None

    settings.USE_USERNAME_FOR_LOGIN = True
    settings.USER_AUTH = fake_user_auth

    form = LoginForm(data={"email": "ldapuser", "password": "pass"})
    cleaned = form.clean()
    assert cleaned["user"] == user


@pytest.mark.django_db
def test_ldap_role_mapping(settings):
    """LDAP auth can map roles onto the returned user."""
    user = User.objects.create_user(username="ldapuser", email="ldap@example.com", password="pass", is_staff=False)

    def fake_user_auth(user_model, username, password):
        user.is_staff = True
        return user

    settings.USE_USERNAME_FOR_LOGIN = True
    settings.USER_AUTH = fake_user_auth

    form = LoginForm(data={"email": "ldapuser", "password": "pass"})
    cleaned = form.clean()
    assert cleaned["user"].is_staff is True


@pytest.mark.django_db
def test_ldap_error_handling(settings):
    """LDAP errors surface as validation errors during login."""

    def fake_user_auth(user_model, username, password):
        raise forms.ValidationError("LDAP connection failed")

    settings.USE_USERNAME_FOR_LOGIN = True
    settings.USER_AUTH = fake_user_auth

    form = LoginForm(data={"email": "any", "password": "bad"})
    with pytest.raises(forms.ValidationError, match="LDAP connection failed"):
        form.clean()
