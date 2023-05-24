from django.db import models
from PIL import Image, ImageFile
from math import isclose
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.core.files.base import ContentFile
from sys import getsizeof
from os.path import splitext

class ArtPiece(models.Model):
    title = models.CharField(blank=True, max_length=64)
    description = models.CharField(blank=True, max_length=512)
    dimensions = models.CharField(blank=True, max_length=128)
    materials = models.CharField(blank=True, max_length=256)
    price = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    available = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Has_one image
    # Has_many secondary_images
    # unnecessary: categories = models.ManyToManyField(Category, through='Categorized', related_name='art_pieces')

    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    art_pieces = models.ManyToManyField(ArtPiece, through='Categorized', related_name='categories')

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
    #    return #reverse('category-detail', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name_plural = "categories"

# Junction Table
class Categorized(models.Model):
    art_piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ArtImage(models.Model):
    art_piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE)
    featured = models.BooleanField()

    #squareImage = ResizedImageField(size=[1000, 1000], crop=['middle', 'center'], default='default_square.jpg', upload_to='square')
    #landImage = ResizedImageField(size=[2878, 1618], crop=['middle', 'center'], default='default_land.jpg', upload_to='landscape')
    #tallImage = ResizedImageField(size=[1618, 2878], crop=['middle', 'center'], default='default_tall.jpg', upload_to='tall')

    large = models.ImageField(upload_to='images')
    display = models.ImageField(upload_to='images/thumbnails', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.art_piece.title
    
    def save(self, *args, **kwargs):
        self.large.file.seek(0)
        # Should this be self.large or self.large.file?
        with Image.open(self.large.file) as image:
            resized_img = ImageOps.fit(image, (640, 480))
            img_info = image.info

            ImageFile.MAXBLOCK = max(ImageFile.MAXBLOCK, resized_img.size[0] * resized_img.size[1])
            temp_thumb = BytesIO()
            resized_img.save(temp_thumb, format=image.format, quality=99, **img_info)
            temp_thumb.seek(0)
            
            self.display.save(self.large.file.name, ContentFile(temp_thumb.read()), save=False)
            
            temp_thumb.close()

            #temp_thumb = ContentFile(temp_thumb.getvalue())

            # Build InMemoryUploadedFile, which is self.large.file's type (large.file.file's type is BytesIO)
            # Assign this file to self.display

            # self.display = InMemoryUploadedFile(
            #     temp_thumb,                    # file
            #     'display',                      # field_name
            #     self.large.file.name,           # file name
            #     self.large.file.content_type,   # content_type
            #     getsizeof(temp_thumb),         # size
            #     None                            # charset
            # )

            #self.display.path = f'images/display/{self.large.name}'
            #resized_img.save(display_path, format=image.format, quality=99, **img_info)


            #super(ResizedImageFieldFile, self).save(name, new_content, save)
            #self.display...(f'images/display/display/{self.large.name}', new_content)
            super(ArtImage, self).save(*args, **kwargs)


            # if type(self.large.file) is io.BytesIO:
            #     # This part is questionable!
            #     img_byte_arr = io.BytesIO()
            #     resized_img.save(img_byte_arr, image.format)
            #     self.large.file = img_byte_arr
            # else:
            #     resized_img.save('/media/images/bobs/{0}'.format(self.large.file.name), image.format)

        # img = Image.open(self.large)
        # resized_img = ImageOps.fit(img, 640, 480)
        # bytesio_obj = BytesIO()

        # resized_img.save(bytesio_obj, 'JPEG')
        # #self.display.delete(save=False)
        # self.display.save('{0}_display'.format(self.large.name), File(resized_img))
        #self.large = get_large_image(self.large, <allowed file size>)
        #self.display = get_thumbnail(self.large, '640x480', quality=90, format='JPEG')
        #self.large = get_thumbnail(self.large, '2680x2010', quality=90, format='JPEG')
        
        
    
    # Return an image scaled to a new width while retaining aspect ratio
    # UNUSED
    def get_scaled_image(img, new_width):
        width_percent = (new_width/float(img.size[0]))
        new_height = int((float(img.size[1])*float(width_percent)))
        return img.resize((new_width, new_height), Image.BICUBIC)
    
    # Crop image to aspect ratio
    # def get_cropped_image(img, aspect_ratio):
    #     width, height = img.size
    #     if isclose(aspect_ratio, (width/height), abs_tol=0.01):
    #         return img
    #     elif (aspect_ratio < (width/height)):
    #         width = round(height*aspect_ratio) # set new width
    #     else:
    #         height = round(width/aspect_ratio) # set new height

    #     # Crop from center
    #     # Could separate this into a method if it is reused...
    #     left = int(img.size[0]/2-width/2)
    #     upper = int(img.size[1]/2-height/2)
    #     right = left + width
    #     lower = upper + height
    #     return img.crop((left, upper,right,lower))
    
    # # If this fails I should try PIL.ImageOps.fit
    # def get_resized_image(img, new_width, new_height):
    #     cropped_img = ArtImage.get_cropped_image(img, new_width/new_height)
    #     return cropped_img.resize((new_width, new_height), Image.BICUBIC)

# Do I need inheritance here?
class ImageOps():
    # If this fails I should try PIL.ImageOps.fit
    def fit(image, new_width, new_height):
        cropped_img = ImageOps.get_cropped_image(image, new_width/new_height)
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
        # Could separate this into a method if it is reused...
        left = int(img.size[0]/2-width/2)
        upper = int(img.size[1]/2-height/2)
        right = left + width
        lower = upper + height
        return img.crop((left, upper,right,lower))