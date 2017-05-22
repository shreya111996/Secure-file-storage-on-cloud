
from boto.s3.connection import S3Connection
from django.conf import settings
from boto.s3.key import Key
import mimetypes
import os
from emailtut2 import mail
import random
from .models import CoverImages
from .algorithms import fs_n,decryption,steg



DEFAULT_PATH = os.path.join(settings.MEDIA_ROOT, "downloads")
DOWNLOAD_PATH = getattr(settings, "DOWNLOAD_PATH", DEFAULT_PATH)
TEMP_PATH=os.path.join(settings.MEDIA_ROOT, "temp")
TEMP_DIR=getattr(settings, "TEMP_PATH", TEMP_PATH)

def process_file(doc,file):
    f=fs_n.split(file, TEMP_DIR,doc)
    doc.document_url =upload(doc,f,settings.BUCKET_NAME1)
    this_id=random.randint(1, 4)
    image=CoverImages.objects.get(pk=this_id)
    text=doc.key1+"$$DELIMITER$$"+doc.key2+"$$DELIMITER$$"+doc.key3
    image_path=TEMP_DIR+"\\"+"output.jpg"
    steg.Steganography.encode(image.img.path,image_path , text)
    mail(image,image_path,doc.user)

def retrieve_file(doc):
    filename=doc.name
    conn = S3Connection(settings.AWS_KEY, settings.AWS_SECRET_KEY, host=settings.REGION_HOST)
    b = conn.get_bucket(settings.BUCKET_NAME1)
    k = Key(b,filename)
    k.get_contents_to_filename(DOWNLOAD_PATH+"\\"+filename)
    conn.close()
    #f=open(DOWNLOAD_PATH+"\\"+filename,'rb')
    f=decryption.split(DOWNLOAD_PATH+"\\"+filename,TEMP_DIR,doc)
    return upload(doc,f,settings.BUCKET_NAME2)

def upload(doc,file,bucket):
    conn = S3Connection(settings.AWS_KEY, settings.AWS_SECRET_KEY, host=settings.REGION_HOST)
    b = conn.get_bucket(bucket)
    if(bucket==settings.BUCKET_NAME2):
        empty(b)
    mime = mimetypes.guess_type(doc.name)[0]
    k = Key(b)
    key = '%s' % doc.name
    k.key = key
    k.set_metadata("Content-Type", mime)
    f= open(file,'rb')
    k.set_contents_from_file(f)
    k.set_acl("public-read")
    k.make_public()
    return 'https://s3.ap-south-1.amazonaws.com/%s/%s' % (k.bucket.name, k.key)

def empty(b):
    k=Key(b)
    for key in b.list():
        k.key=key
        b.delete_key(k)