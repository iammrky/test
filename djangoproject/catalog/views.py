from django.shortcuts import render
from .models import Album, Photo
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.
def index(request):
	num_photo = Photo.objects.all()
	num_album = Album.objects.all().count()
	photo_all = Photo.objects.all().count()

	return render(request, 
		'index.html',
		context = {'num_photo':num_photo, 'num_album':num_album, 'photo_all':photo_all})


class AlbumCreate(CreateView):
	model = Album
	fields = '__all__'

class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('album')


class PhotoListView(generic.ListView):
    model = Photo

class PhotoDetailView(generic.DetailView):
    model = Photo    	