from django.shortcuts import render, redirect
from .models import File, Shared
from django.contrib.auth.decorators import login_required
from .forms import FileForm, ShareForm
from django.contrib.auth.models import User
from users.models import Profile
from users.views import profiles

# Create your views here.

def myFiles(request):
    profile = request.user.profile
    files = profile.file_set.all()
    context = {'files': files}
    return render(request, 'files/my-files.html', context)

def sharedFiles(request):
    profile = request.user.profile
    shared = profile.shared_set.all()
    context = {'shared': shared}
    return render(request, 'files/shared-files.html', context)

@login_required(login_url="login")
def share(request):
    profile = request.user.profile
    form = ShareForm()
    form.fields["files"].queryset = File.objects.filter(owner=profile)
    form.fields["share_with"].queryset = Profile.objects.exclude(username=profile)
    if request.method == 'POST':
        print(request.POST)
        form = ShareForm(request.POST)
        if form.is_valid():
            share = form.save()
            share.save()
            return redirect('shared_files')
    context = {'form': form}
    return render(request, 'files/share-form.html', context)
    

@login_required(login_url="login")
def uploadFile(request):
    profile = request.user.profile
    form = FileForm()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.save(commit=False)
            files.owner = profile
            files.save()
            return redirect('files')
    context = {'form': form}
    return render(request, 'files/file-form.html', context)
