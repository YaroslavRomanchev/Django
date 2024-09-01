from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self): # чтобы мы видели сигналы и они работали корректно надо написать именно эту функцию
        import users.signals