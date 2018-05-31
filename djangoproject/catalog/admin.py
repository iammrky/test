from django.contrib import admin
from .models import Photo, Album
from imagekit.admin import AdminThumbnail

# Register your models here.

#admin.site.register(Item)#, ItemAdmin)

class PhotoAdmin(admin.ModelAdmin):
    admin.site.disable_action('delete_selected')
    def full_delete_selected(self, request, obj):
        for o in obj.all():
            o.delete()
    full_delete_selected.short_description = 'Удалить выбранные иллюстрации'
    actions = ['full_delete_selected']
    list_display = ('title', 'album', 'author', 'admin_thumbnail')
    admin_thumbnail = AdminThumbnail(image_field='image')
    readonly_fields = ['admin_thumbnail']



#class AlbumAdmin(admin.ModelAdmin):
#	inlines = [PhotoInline]

admin.site.register(Album)
admin.site.register(Photo, PhotoAdmin)

