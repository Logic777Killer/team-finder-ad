from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import Project


def project_list(request):
    queryset = Project.objects.select_related("owner").prefetch_related("participants")
    page = Paginator(queryset, 12).get_page(request.GET.get("page"))
    return render(request, "projects/project_list.html", {"projects": page})


@login_required
def favorite_projects(request):
    queryset = request.user.favorites.select_related("owner").prefetch_related("participants")
    page = Paginator(queryset, 12).get_page(request.GET.get("page"))
    return render(request, "projects/favorite_projects.html", {"projects": page})


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=project_id,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect(f"/projects/{project.id}/")

    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id and not request.user.is_staff:
        return redirect(f"/projects/{project.id}/")

    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(f"/projects/{project.id}/")

    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )


@login_required
@require_POST
def complete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    allowed = project.owner_id == request.user.id or request.user.is_staff

    if not allowed or project.status != Project.OPEN:
        return JsonResponse({"status": "error"}, status=403)

    project.status = Project.CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": Project.CLOSED})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        participant = False
    else:
        project.participants.add(request.user)
        participant = True

    return JsonResponse({"status": "ok", "participant": participant})


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True

    return JsonResponse({"status": "ok", "favorited": favorited})

