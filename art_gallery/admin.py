from django.contrib import admin
from .models import ArtPiece
from .models import Category
from .models import ArtImage

class ArtImageAdmin(admin.ModelAdmin):
    fields = ('art_piece', 'featured', 'large')

admin.site.register(ArtPiece)
admin.site.register(Category)
admin.site.register(ArtImage, ArtImageAdmin)
