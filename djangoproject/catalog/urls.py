from django.conf.urls import url
from . import views


urlpatterns = [
	url('', views.index, name='index'),
	#url(r'^photo/$', views.photo, name='photo'),
	#url(r'^photo/(?P<pk>\d+)$', views.PhotoDetailView.as_view(), name='photo-detail'),
]

urlpatterns += [  
    url(r'^album/create/', views.AlbumCreate.as_view(), name='album_create'),
    url(r'^album/<int:pk>/delete/', views.AlbumDelete.as_view(), name='album_delete'),
]