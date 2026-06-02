import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

from common.forms import validate_github_url

from .models import User


PHONE_RE = re.compile(r"^(?:8|\+7)\d{10}$")


def normalize_phone(value):
    if not value:
        return None

    phone = value.strip().replace(" ", "").replace("-", "")
    if phone.startswith("8"):
        return "+7" + phone[1:]
    return phone


class RegisterForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=124)
    surname = forms.CharField(label="Фамилия", max_length=124)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self):
        return User.objects.create_user(**self.cleaned_data)


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(
                self.request,
                username=email.lower(),
                password=password,
            )
            if self.user is None:
                raise forms.ValidationError("Неверный имейл или пароль")

        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "avatar": "Аватар",
            "about": "О себе",
            "phone": "Телефон",
            "github_url": "GitHub",
        }
        widgets = {
            "about": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_phone(self):
        raw_phone = self.cleaned_data.get("phone")
        if not raw_phone:
            return None

        compact = raw_phone.strip().replace(" ", "").replace("-", "")
        if not PHONE_RE.match(compact):
            raise forms.ValidationError("Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX.")

        normalized = normalize_phone(compact)
        duplicate = User.objects.filter(phone=normalized)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)

        if duplicate.exists():
            raise forms.ValidationError("Пользователь с таким телефоном уже существует.")

        return normalized

    def clean_github_url(self):
        value = self.cleaned_data.get("github_url")
        validate_github_url(value)
        return value


class UserPasswordChangeForm(PasswordChangeForm):
    pass

