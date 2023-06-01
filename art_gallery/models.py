from django.db import models
from PIL import Image, ImageFile
from math import isclose
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.core.files.base import ContentFile
from sys import getsizeof
from os.path import splitext
from pathlib import Path
from django.db.models.functions import Lower

class ArtPiece(models.Model):
    title = models.CharField(blank=True, max_length=64)
    description = models.CharField(blank=True, max_length=512)
    dimensions = models.CharField(blank=True, max_length=128)
    materials = models.CharField(blank=True, max_length=256)
    price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def is_available(self):
        if self.available:
            return 'Yes'
        else:
            return 'No'
    
    def featured_image(self):
        for art_image in self.artimage_set.all():
            if art_image.featured:
                return art_image

class Category(models.Model):
    title = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    art_pieces = models.ManyToManyField(ArtPiece, through='Categorized', related_name='categories')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(Lower('title'), name='unique_lower_title_category')
        ]

# Junction Table
class Categorized(models.Model):
    art_piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ArtImage(models.Model):
    art_piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE)
    featured = models.BooleanField()

    large = models.ImageField(upload_to='images')
    display = models.ImageField(upload_to='images/thumbnails', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.art_piece.title
    
    def save(self, *args, **kwargs):
        update_thumbnail = True

        try:
            old_image = ArtImage.objects.get(id=self.id)
            if old_image.large == self.large:
                update_thumbnail = False
            elif old_image.display != self.display: # Else if display has been updated
                update_thumbnail = False
        except: pass # when new photo then we do nothing, normal case

        if update_thumbnail == True:
            self.large.file.seek(0)
            # Should this be self.large or self.large.file?
            with Image.open(self.large.file) as image:
                resized_img = MyImageOps.fit(image, 480, 640)
                img_info = image.info

                large_filename = Path(self.large.name)
                thumb_filename = large_filename.with_stem(large_filename.stem + '_thumb').name

                ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, resized_img.size[0] * resized_img.size[1])
                temp_thumb = BytesIO()
                resized_img.save(temp_thumb, format=image.format, quality=99, **img_info)
                temp_thumb.seek(0)
                
                self.display.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)         
                temp_thumb.close()
        
        super(ArtImage, self).save(*args, **kwargs)
    
    # # Return an image scaled to a new width while retaining aspect ratio
    # def get_scaled_image(img, new_width):
    #     width_percent = (new_width/float(img.size[0]))
    #     new_height = int((float(img.size[1])*float(width_percent)))
    #     return img.resize((new_width, new_height), Image.BICUBIC)

class MyImageOps():
    # If this fails I should try PIL.ImageOps.fit
    def fit(image, new_width, new_height):
        cropped_img = MyImageOps.get_cropped_image(image, new_width/new_height)
        return cropped_img.resize((new_width, new_height), Image.BICUBIC)
    
    # Crop image to aspect ratio
    def get_cropped_image(img, aspect_ratio):
        width, height = img.size
        if isclose(aspect_ratio, (width/height), abs_tol=0.01):
            return img
        elif (aspect_ratio < (width/height)):
            width = round(height*aspect_ratio) # set new width
        else:
            height = round(width/aspect_ratio) # set new height

        # Crop from center
        left = int(img.size[0]/2-width/2)
        upper = int(img.size[1]/2-height/2)
        right = left + width
        lower = upper + height
        return img.crop((left, upper, right, lower))