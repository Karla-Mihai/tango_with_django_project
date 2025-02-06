from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rango.models import Category
from rango.models import Page

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list
    }

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {
        'message': "This tutorial has been put together by Karla Mihai",
        'MEDIA_URL': settings.MEDIA_URL  
    }
    return render(request, 'rango/about.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        
        # Optionally, pass most liked categories and most viewed pages
        most_liked_categories = Category.objects.order_by('-likes')[:5]
        most_viewed_pages = Page.objects.order_by('-views')[:5]

        context_dict['category'] = category
        context_dict['pages'] = pages
        context_dict['most_liked_categories'] = most_liked_categories
        context_dict['most_viewed_pages'] = most_viewed_pages

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)