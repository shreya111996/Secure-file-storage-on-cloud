from django.conf import settings
import os

settings.configure()
DEFAULT_PATH = os.path.join(settings.MEDIA_ROOT, "uploads")
UPLOAD_PATH = getattr(settings, "PDF_UPLOAD_PATH", DEFAULT_PATH)
print(UPLOAD_PATH)