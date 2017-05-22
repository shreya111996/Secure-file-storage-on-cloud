
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,HttpResponseRedirect
from .forms import UserForm, UploadFileForm, DecryptForm
from .file_handler import process_file,retrieve_file
from django.core.urlresolvers import reverse
from signup.models import Document
from django.conf import settings
from CheckKeys import check

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'signup/userpage.html')
    context = {
        "form": form,
    }
    return render(request, 'signup/sign.html', context)


def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                doc = Document.objects.filter(user=request.user)
                return render(request, 'signup/userpage.html',{'documents':doc})
            else:
                return render(request, 'signup/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'signup/login.html', {'error_message': 'Invalid login'})
    return render(request, 'signup/login.html')

def logout_user(request):
    logout(request)

    return HttpResponseRedirect('/page/login')

def user_page(request):
    doc = Document.objects.filter(user=request.user)
    return render(request, 'signup/userpage.html',{'documents':doc})

def upload(request):
    return render(request, 'signup/upload.html')

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST ,request.FILES)
        if form.is_valid():
            doc=form.save(commit=False)
            doc.user=request.user
            doc.name=request.FILES['file'].name
            f=request.FILES['file']
            process_file(doc,f)
            doc.save()
            return HttpResponseRedirect('/page/userpage/')
    else:

        form = UploadFileForm()
    return render(request, 'signup/upload.html', {'form': form})

def doc_detail(request, uuid):
    doc=Document.objects.get(uuid=uuid)
    return render(request,'signup/detail.html',{'docs': doc})

def doc_decrypt(request, uuid):
    doc = Document.objects.get(uuid=uuid)
    text=""
    if request.method=="POST":
        form = DecryptForm(request.POST ,request.FILES)
        text="Invalid Image Password!!Try again"
        if form.is_valid():
            image=request.FILES['image']
            test=check(doc,image)
            if(test==1):
                file_path=retrieve_file(doc)
                return render(request,'signup/success.html',{'docs':doc,'file_path':file_path})

    else:
        form = DecryptForm()
    return render(request,'signup/decrypt.html',{'docs': doc,'form':form,'text':text})











































































































































































































































































































































































































