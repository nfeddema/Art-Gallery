from django.contrib import admin
from .models import ArtPiece, Category, ArtImage, Categorized

class CategorizedInline(admin.StackedInline):
    model = Categorized
    extra = 1

class ArtImageInline(admin.TabularInline):
    model = ArtImage
    extra = 1
    fields = ('art_piece', 'featured', 'large')

class ArtPieceAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'dimensions', 'materials', 'price', 'available')
    inlines = [CategorizedInline, ArtImageInline]

class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategorizedInline]
    #filter_horizontal = ('art_pieces',)

#class ArtImageAdmin(admin.ModelAdmin):

admin.site.register(ArtPiece, ArtPieceAdmin)
admin.site.register(Category, CategoryAdmin)
#admin.site.register(ArtImage)
