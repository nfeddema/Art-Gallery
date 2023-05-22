from django.db import models
from PIL import Image
from math import isclose

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
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)

    #squareImage = ResizedImageField(size=[1000, 1000], crop=['middle', 'center'], default='default_square.jpg', upload_to='square')
    #landImage = ResizedImageField(size=[2878, 1618], crop=['middle', 'center'], default='default_land.jpg', upload_to='landscape')
    #tallImage = ResizedImageField(size=[1618, 2878], crop=['middle', 'center'], default='default_tall.jpg', upload_to='tall')

    large = models.ImageField(upload_to='images')
    display = models.ImageField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.art_piece.title
    
    def save(self, *args, **kwargs):
        #self.display = self.large
        #self.display.name = '/media/images/{0}.....'.format(self.large.file.name)
        #super().save(*args, **kwargs)        
        img = Image.open(self.large)
        resized_img = ImageOps.fit(img, 640, 480)
        #self.display.delete(save=False) #We need to delete the old self.display
        resized_img.save(self.display.path, quality=100)

        #img.close()
        #self.large = get_large_image(self.large, <allowed file size>)
        #self.display = get_thumbnail(self.large, '640x480', quality=90, format='JPEG')
        #self.large = get_thumbnail(self.large, '2680x2010', quality=90, format='JPEG')
        
        super(ArtImage, self).save(*args, **kwargs)
    
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