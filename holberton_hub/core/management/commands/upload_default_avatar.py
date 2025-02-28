from django.core.management.base import BaseCommand
import cloudinary.uploader
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Upload default avatar to Cloudinary'

    def handle(self, *args, **kwargs):
        image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'default_avatar.png')

        if not os.path.exists(image_path):
            self.stdout.write(self.style.ERROR(f'Image not found at: {image_path}'))
            return

        try:
            result = cloudinary.uploader.upload(
                image_path,
                public_id='profile_pictures/default_avatar',
                overwrite=True,
                resource_type="image"
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully uploaded default avatar: {result["secure_url"]}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error uploading image: {str(e)}'))
