from django.contrib import admin
from .models import ArtPiece
from .models import Category
from .models import ArtImage

admin.site.register(ArtPiece)
admin.site.register(Category)
admin.site.register(ArtImage)
