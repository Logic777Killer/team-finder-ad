from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from .forms import ProfileForm
from .models import User


class AdminUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "name", "surname")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdminUserChangeForm(ProfileForm):
    password = ReadOnlyPasswordHashField(label="Пароль")

    class Meta(ProfileForm.Meta):
        fields = ProfileForm.Meta.fields + ["email", "password", "is_active", "is_staff", "is_superuser", "groups", "user_permissions", "favorites"]


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    list_display = ("email", "name", "surname", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "name", "surname")
    ordering = ("id",)
    filter_horizontal = ("groups", "user_permissions", "favorites")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Профиль", {"fields": ("name", "surname", "avatar", "phone", "github_url", "about", "favorites")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "surname", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ("date_joined", "last_login")

