from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request, category=None):
    categories = Category.objects.all()
    context = {}
    context['categories'] = categories
    images = []

    art_pieces = ArtPiece.objects.all()

    for art_piece in art_pieces:
        if art_piece.featured_image:
            images.append(art_piece.featured_image)

    context['images'] = images

    return render(request, 'main/index.html', context)

def category(request, category):
    categories = Category.objects.all()
    context = {}
    context['categories'] = categories
    images = []

    category = Category.objects.get(title=category)
    art_pieces = ArtPiece.objects.filter(category=category)

    for art_piece in art_pieces:
        if art_piece.featured_image:
            images.append(art_piece.featured_image)

    context['images'] = images
    context['category'] = category

    return render(request, '', context)