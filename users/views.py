from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

from common.constants import USERS_PER_PAGE
from common.services import paginate_queryset

from .forms import LoginForm, ProfileForm, RegisterForm, UserPasswordChangeForm


User = get_user_model()


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("projects:project_list")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None, request=request)

    if form.is_valid():
        login(request, form.user)
        return redirect("projects:project_list")

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def profile_detail(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id, is_active=True)
    return render(request, "users/user-details.html", {"user": profile_user})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)

    if form.is_valid():
        form.save()
        return redirect("users:profile_detail", user_id=request.user.id)

    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password(request):
    form = UserPasswordChangeForm(request.user, request.POST or None)

    if form.is_valid():
        form.save()
        update_session_auth_hash(request, request.user)
        return redirect("users:profile_detail", user_id=request.user.id)

    return render(request, "users/change_password.html", {"form": form})


def participants(request):
    queryset = User.objects.filter(is_active=True).order_by("-date_joined")
    active_filter = request.GET.get("filter") if request.user.is_authenticated else None

    if active_filter == "owners-of-favorite-projects":
        queryset = queryset.filter(owned_projects__interested_users=request.user)
    elif active_filter == "owners-of-participating-projects":
        queryset = queryset.filter(owned_projects__participants=request.user)
    elif active_filter == "interested-in-my-projects":
        queryset = queryset.filter(favorites__owner=request.user)
    elif active_filter == "participants-of-my-projects":
        queryset = queryset.filter(participated_projects__owner=request.user)
    else:
        active_filter = None

    page = paginate_queryset(request, queryset.distinct(), USERS_PER_PAGE)
    return render(
        request,
        "users/participants.html",
        {"participants": page, "active_filter": active_filter},
    )

