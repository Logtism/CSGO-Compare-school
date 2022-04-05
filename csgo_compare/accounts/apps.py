from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from firebrick import settings
        
        import accounts.signals
        from django.contrib.auth.models import User
        post_save.connect(accounts.signals.create_profile, sender=User)
        post_save.connect(accounts.signals.save_profile, sender=User)