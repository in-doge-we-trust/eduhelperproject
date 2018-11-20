from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # post_save.connect(create_user_profile, sender=User)
        # post_save.connect(save_user_profile, sender=User)
        import api.signals
