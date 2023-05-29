from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request, category=None):
    categories = Category.objects.all()
    context = {}
    context['categories'] = categories
    art_piece_list = []

    art_pieces = ArtPiece.objects.all()

    for art_piece in art_pieces:
        if art_piece.featured_image:
            art_piece.short_description = art_piece.description[:128]
            art_piece_list.append(art_piece)

    context['art_pieces'] = art_piece_list

    return render(request, 'main/index.html', context)

def category(request, category):
    categories = Category.objects.all()
    context = {}
    context['categories'] = categories
    art_piece_list = []

    category = Category.objects.get(title=category)
    art_pieces = ArtPiece.objects.filter(categories=category)

    for art_piece in art_pieces:
        if art_piece.featured_image:
            art_piece.short_description = art_piece.description[:128]
            art_piece_list.append(art_piece)

    context['art_pieces'] = art_piece_list
    context['category'] = category

    return render(request, 'main/category.html', context)

def artPiecePage(request, art_piece_id):
    art_piece = ArtPiece.objects.get(id=art_piece_id)
    
    context = {}
    context['art_piece'] = art_piece

    return render(request, 'main/art_piece.html', context)