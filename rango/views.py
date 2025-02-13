from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime, timedelta
from django.conf import settings


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    visitor_cookie_handler(request)
    
    response = render(request, 'rango/index.html', context=context_dict)
    return response



def about(request):
    
    visitor_cookie_handler(request)
    visits = request.session.get('visits', 1)
    print(visits)
    context_dict = {
        'message': "This tutorial has been put together by Karla Mihai",
        'MEDIA_URL': settings.MEDIA_URL,
        'visits': visits  
    }

    return render(request, 'rango/about.html', context=context_dict)



def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        
        
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


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect(reverse('rango:index'))  

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))  # ✅ Fixed reverse

        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
        
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html',
                    context={'user_form':user_form,
                             'profile_form':profile_form,
                              'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
            
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')




def user_logout(request):
    logout(request)
    return redirect('rango:index')


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
    
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


def visitor_cookie_handler(request):
   
    visits = request.session.get('visits', 0)
    last_visit_cookie = request.session.get('last_visit', str(datetime.now()- timedelta(days=1)))

    try:
        last_visit_time = datetime.strptime(last_visit_cookie, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        last_visit_time = datetime.now()


    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())

    request.session['visits'] = visits
    request.session.modified = True