import uuid
import os
from django.db import models
from django.contrib.auth.models import User
#from django.urls import reverse
from django.utils.translation import gettext as _
#from datetime import datetime
from django.conf import settings
from django.utils import timezone

DEFAULT_PATH = os.path.join(settings.MEDIA_ROOT, "images")
UPLOAD_PATH = getattr(settings, "IMAGE_PASSWORD_PATH", DEFAULT_PATH)

class Document(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    name = models.CharField(_("Title"), max_length=100)
    uuid = models.CharField(_('Unique Identifier'), max_length=36)
    document_url = models.URLField(_("Document_Url"))
    date_uploaded = models.DateTimeField()
    key1 = models.CharField(_("key1"),max_length=300)
    key2 = models.CharField(_("key2"),max_length=300)
    key3 = models.CharField(_("key3"),max_length=300)
    size1= models.IntegerField()
    size2= models.IntegerField()
    size3= models.IntegerField()

    def save(self, **kwargs):
        self.date_uploaded = timezone.now()
        if self.id is None:
            self.uuid = str(uuid.uuid4())
        models.Model.save(self)


    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')


class CoverImages(models.Model):
    img = models.ImageField(upload_to=UPLOAD_PATH)