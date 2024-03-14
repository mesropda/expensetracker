from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterUserForm
from .models import Contact
from .models import UserProfile
# Create your views here.


# def index_reset(request):
#     records = UserProfile.objects.all()
#     index = 1
#     for record in records:
#         old_record = UserProfile.objects.get(id=record.id)
#         record.id = index
#         record.save()
#         old_record.delete()
#         index = index + 1
#     return redirect("/")


def home_page(request):

    return render(request, "home.html", {})


def privacy_policy(request):
    return render(request, "privacy_policy.html", {})


def reset_password_sent(request):
    return render(request, "reset_password_sent.html", {})


def reset_password_complete(request):
    return render(request, "reset_password_complete.html", {})


def about_us(request):
    return render(request, "about_us.html", {})


def check_if_user_loggedin(request):
    if request.session.has_key('is_logged'):
        user_id = request.session['user_id']
        if user_id == 36:
            user = User.objects.get(id=user_id)
        else:
            user = UserProfile.objects.get(id=user_id-34)
        return user


def contact_us(request):
    if request.method == "POST":
        new_contact = Contact.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            emial=request.POST['email'],
            message=request.POST['message'],
        )
        messages.success(
            request, "Your message has been successfully received. We will get back to you as soon as poosble!")

    return render(request, "contact_us.html", {})


def user_profile(request):
    if request.session.has_key('is_logged'):
        user_id = request.session['user_id']
        '''"User" table starts with ID #36, it is the ID of admin(registrtations with lower ID have been deleted). Standard users 
        in this table start form ID #37. 
        In UserProfile table the IDs start with #3, so to compensate for this difference we check the ID to know who is logged in.
        If it is not the admin, we do "user_id-37-3" to get the right user ID in UserProfile table. Without this the 
        program fails to properly relate the user table wuth UserProfile table'''
        if user_id == 36:
            user = User.objects.get(id=user_id)
            context = {'userProfile': user}
        else:
            user = UserProfile.objects.get(id=user_id-34)
            context = {'userProfile': user}

            '''If there is a post, updat ethe user infor in and save both "User" table abd "UserProfile table" '''
            if request.method == "POST":
                user.user.username = request.POST['username']
                user.user.first_name = request.POST['first_name']
                user.user.last_name = request.POST['last_name']
                user.user.email = request.POST['email']
                try:
                    user.profession = request.POST['profession']
                except MultiValueDictKeyError:
                    pass
                user.savings = request.POST['savings']
                user.income = request.POST['income']
                user.user.save()
                user.save()
                messages.success(
                    request, "The profile has been updated successfully!")
        return render(request, "profile.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['is_logged'] = True
            user_id = request.user.id
            print(f"The login IDDDDDD is {user_id}")
            request.session['user_id'] = user_id
            return redirect('expenses:index')
        else:
            messages.success(
                request, ("There was an error logging in, try again!"))
            return redirect('tracker:log-in')
    else:
        return render(request, "login_user.html", {})


def logout_user(request):
    request.session['is_logged'] = False
    logout(request)
    if request.session.has_key('is_logged'):
        user_id = request.session['user_id']
        del (request.session['user_id'])
    messages.success(request, 'Successfully logged out')
    return redirect('tracker:home')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            '''Save the new user and assign it to new_user'''
            new_user = form.save()

            '''Craete new UserProfile for the new user and save it'''
            new_profile = UserProfile(
                savings=form.cleaned_data['savings'], income=form.cleaned_data['income'], profession=form.cleaned_data['profession'])
            new_profile.user = new_user
            new_profile.save()

            '''Login the newly ceated user'''
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,
                                password=password)

            send_mail(
                'Registration confirmation',
                f'Thank you {
                    user.first_name} for registergin in expense tracker',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            login(request, user)
            request.session['is_logged'] = True
            user_id = request.user.id
            print(f"The login ID is {user_id}")
            request.session['user_id'] = user_id
            # messages.success(request, ("Welcome to expense tracker"))
            return redirect('expenses:index')
    else:
        form = RegisterUserForm()

    return render(request, "register_user.html", {'form': form})


# def user_home_page(request):
#     return render(request, "user_home_page.html", {})
