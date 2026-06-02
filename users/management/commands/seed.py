from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from projects.models import Project


class Command(BaseCommand):
    help = "Creates demo users and projects for local testing."

    def handle(self, *args, **options):
        User = get_user_model()
        demo_users = [
            {
                "email": "maria@yandex.ru",
                "password": "password",
                "name": "Мария",
                "surname": "Иванова",
                "phone": "+79000000001",
                "about": "Backend-разработчик, люблю Django и pet-проекты.",
                "github_url": "https://github.com/maria",
            },
            {
                "email": "pavel@yandex.ru",
                "password": "password",
                "name": "Павел",
                "surname": "Смирнов",
                "phone": "+79000000002",
                "about": "Frontend-разработчик, собираю удобные интерфейсы.",
                "github_url": "https://github.com/pavel",
            },
            {
                "email": "anna@yandex.ru",
                "password": "password",
                "name": "Анна",
                "surname": "Кузнецова",
                "phone": "+79000000003",
                "about": "UI/UX дизайнер, ищу команды для учебных проектов.",
                "github_url": "",
            },
        ]

        users = []
        for data in demo_users:
            user_data = data.copy()
            password = user_data.pop("password")
            user, created = User.objects.update_or_create(
                email=user_data["email"],
                defaults=user_data,
            )
            if created or not user.has_usable_password():
                user.set_password(password)
                user.save(update_fields=["password"])
            users.append(user)

        project_data = [
            {
                "owner": users[0],
                "name": "Планировщик учебных задач",
                "description": "Сервис для студентов: расписание, дедлайны и командные списки задач.",
                "github_url": "https://github.com/maria/student-planner",
            },
            {
                "owner": users[1],
                "name": "Биржа pet-проектов",
                "description": "Каталог идей, где разработчики могут быстро найти команду.",
                "github_url": "https://github.com/pavel/pet-market",
            },
            {
                "owner": users[2],
                "name": "Галерея дизайн-концептов",
                "description": "Портфолио-конструктор для дизайнеров с подборками экранов и ссылками.",
                "github_url": "",
            },
        ]

        for data in project_data:
            project, _ = Project.objects.update_or_create(
                owner=data["owner"],
                name=data["name"],
                defaults=data,
            )
            project.participants.add(data["owner"])

        users[0].favorites.add(Project.objects.get(name="Биржа pet-проектов"))
        users[1].favorites.add(Project.objects.get(name="Планировщик учебных задач"))
        Project.objects.get(name="Планировщик учебных задач").participants.add(users[1])

        self.stdout.write(self.style.SUCCESS("Demo data is ready."))

