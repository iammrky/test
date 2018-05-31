from django.db import models
from django.contrib.auth.models import User
from PIL import Image 
import os
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.html import format_html


# Create your models here.

def _add_mini(s):
    parts = s.split(".")
    parts.insert(-1, "mini")
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)

# Удаление миниатюры с физического носителя.
def _del_mini(p):
    mini_path = _add_mini(p)
    if os.path.exists(mini_path):
        os.remove(mini_path)



class Album(models.Model):
	name = models.CharField(max_length = 200, help_text = "Enter a name album")
	description = models.TextField()

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class Photo(models.Model):
    album = models.ForeignKey(Album,on_delete = models.SET_NULL, null=True)
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = 'gallery')
    captions = models.CharField(max_length=250, blank=True)
	#genre = models.ManyToManyField(Genre, help_text = "Select a genre")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image_small = ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    class Meta:
	    ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id': self.id})

    def image_tag(self):
    	return format_html('<img src="{}" />'.format(self.image.url))
    image_tag.short_description = 'Image'    

    def get_mini_path(self):
    	return _add_mini(self.image.path)
    mini_path = property(get_mini_path)

    def get_mini_url(self):
    	return _add_mini(self.image.url)
    mini_url = property(get_mini_url)

    def get_thumbnail_html(self):
        img_resize_url = get_thumbnail(self.original_image, '100x100').url
        html = '<a class="image-picker" href="%s"><img src="%s" alt="%s"/></a>'
        return html % (self.image.url, img_resize_url)
    get_thumbnail_html.short_description = 'Изображение'
    get_thumbnail_html.allow_tags = True

    def save(self, force_insert = False, force_update=False, using = None):
    	super(Photo, self).save()
    	img = Image.open(self.image.path)
    	img.thumbnail((128,128), Image.ANTIALIAS)
    	img.save(self.mini_path, 'JPEG')

    def delete(self, using = None):
	    try:
	        obj = Photo.objects.get(id=self.id)
	        _del_mini(obj.image.path)
	        obj.image.delete()
	    except (Photo.DoesNotExist, ValueError):
	        pass
	    super(Photo, self).delete()        

	
#class PhotoInline(admin.StackedInline):
#	model = Photo
#
#class ItemAdmin(admin.ModelAdmin):
#	inlines = [PhotoInline]



