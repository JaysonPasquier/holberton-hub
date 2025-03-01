from django.apps import AppConfig
import cloudinary

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Initialize Cloudinary when the app is ready
        cloudinary.config(
            cloud_name = "dsvolcznm",
            api_key = "445719466135631",
            api_secret = "6e_FbbsVgoZi8SyybxHPfzgL8nE",
            secure = True
        )
