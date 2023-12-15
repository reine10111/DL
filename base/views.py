from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import login


# Create your views here.

def main(request):
    return render(request, 'base/main.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, "base/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("view-rooms")
        else:
            messages.add_message(request, messages.ERROR, 'Incorrect login credential(s)')

    return render(request, "base/login.html")


def logout_view(request):
    logout(request)
    return redirect("main")


from .models import Admin, Room, Member
from helpers import random_str
from itertools import chain


def view_all_rooms(request):
    if request.user.is_authenticated:
        r = Member.objects.filter(user=request.user)
        a = Admin.objects.filter(user=request.user)
        rooms = list(chain(r, a))

        if not rooms:
            return render(request, "base/choose1.html")  # Redirect to choose.html if no rooms

        return render(request, "base/home.html", {"rooms": rooms})
    else:
        return redirect('login')
        return redirect('login')
def create_room(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        join_code = random_str()
        room = Room.objects.create(title=title, description=description, owner=request.user, join_code=join_code)
        Admin.objects.create(user=request.user, room=room)

        return redirect('dashboard', room_id=room.join_code)
    elif request.user.is_authenticated:
        return render(request, "base/createroom.html")
    else:
        return redirect('login')


def join_room(request):
    if request.method == "POST":
        code = request.POST["code"]
        try:
            room = Room.objects.get(join_code=code)
        except Room.DoesNotExist:
            return render(request, "base/join-classroom.html", {'error_message': 'Room not found'})

        Member.objects.create(user=request.user, room=room)
        return redirect(f"/room/{code}/")

    else:
        return render(request, "base/join-classroom.html")


from .models import Room, bills, Admin, Member, Submission, Task
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.template.defaultfilters import slugify
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MemberForm, AdminForm
from .models import Member, Admin


def home(request, room_id):
    return render(request, "base/dashboard.html", {
        "room": Room.objects.get(join_code=room_id)
    })


def post_bills(request, room_id):
    room = Room.objects.get(join_code=room_id)
    if request.method == "POST":
        date_time_obj = datetime.strptime(request.POST.get("due"), '%Y-%m-%dT%H:%M')
        new_bills = bills.objects.create(
            title=request.POST.get("title"),
            room=room,
            amount=request.POST.get("amount"),
            due=date_time_obj,
            slug=slugify(request.POST["title"])
        )
        return HttpResponse(new_bills.slug)
    else:
        return render(request, "base/post-bills.html", {"room": room})


@csrf_exempt
def delete_submission_api(request, room_id, bills_slug):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            room_id = data["roomId"]
            bills_slug = data["slug"]
            room = Room.objects.get(join_code=room_id)
            room_bills = bills.objects.filter(room=room, slug=bills_slug)
            room_bills.delete()
            return JsonResponse({"success": True})
        except (json.JSONDecodeError, Room.DoesNotExist, bills.DoesNotExist) as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


def view_submitted_proof(request, room_id, bills_slug, mem_id):
    room = Room.objects.get(join_code=room_id)
    room_bills = bills.objects.get(room=room, slug=bills_slug)
    user = User.objects.get(id=mem_id)

    submission = Submission.objects.get(user=user, bills=room_bills)

    return render(request, "base/view-member-submit.html", {
        "room": room,
        "room_bills": room_bills,
        "member": user,
        "submission": submission
    })


from django.http import HttpResponseBadRequest


@csrf_exempt
def view_member_bills(request, room_id, bills_slug):
    room = Room.objects.get(join_code=room_id)
    room_bills = bills.objects.get(room=room, slug=bills_slug)
    role = ""

    try:
        admin = Admin.objects.get(room=room, user=request.user)
        role = "admin"
    except Admin.DoesNotExist:
        member = Member.objects.get(room=room, user=request.user)
        role = "member"

    if request.method == "POST":
        proof_file = request.FILES.get('proof')
        Submission.objects.create(user=request.user, bills=room_bills, proof=proof_file)
        return redirect(f"/room/{room_id}/bills/{bills_slug}")
    else:
        submission = None

        try:
            submission = Submission.objects.get(user=request.user, bills=room_bills)
        except Submission.DoesNotExist:
            pass

        if role == "member":
            request.session["previous_room_code"] = room_id
            request.session["previous_bills_slug"] = bills_slug
            return render(request, "base/view-bills-member.html", {
                "room_bills": room_bills,
                "room": room,
                "role": role,
                "submission": submission,
            })
        else:
            submissions = Submission.objects.filter(bills=room_bills)
            submitted_members = [sub.user for sub in submissions]
            all_members = [mm.user for mm in Member.objects.filter(room=room)]
            did_not_submit = [mem for mem in all_members if mem not in submitted_members]

            return render(request, "base/view-bill-admin.html", {
                "room_bills": room_bills,
                "room": room,
                "submissions": submissions,
                "did_not_submit": did_not_submit,
            })


from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Room, bills, Admin, Submission
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone


@csrf_exempt
def view_bills(request, room_id):
    room = get_object_or_404(Room, join_code=room_id)
    room_bills = bills.objects.filter(room=room)
    role = ""

    if request.user.is_authenticated:  # Ensure user is authenticated
        try:
            admin = Admin.objects.get(room=room, user=request.user)
            role = "admin"
        except Admin.DoesNotExist:
            try:
                member = Member.objects.get(room=room, user=request.user)
                role = "member"
            except Member.DoesNotExist:
                pass

    context = {
        'room': room,
        'bills': room_bills,
        'role': role,
    }

    return render(request, 'base/bills.html', context)


from .models import Task
from .forms import TaskForm
from django.shortcuts import redirect


@csrf_exempt
def to_do_list(request, room_id):
    room = get_object_or_404(Room, join_code=room_id)
    user = request.user

    tasks = Task.objects.filter(room=room, user=user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.room = room  # Associate the Task with the Room
            task.user = user  # Associate the Task with the User
            task.save()
            return redirect('todolist', room_id=room.join_code)
    else:
        form = TaskForm()

    context = {
        'room': room,
        'user': user,
        'tasks': tasks,
        'form': form,
    }
    return render(request, 'base/toDo.html', context)

def updateTask(request, room_id, pk):
    room = get_object_or_404(Room, join_code=room_id)
    user = request.user

    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('todolist', room_id=room.join_code)

    context = {'form': form,
               'room': room,
               }
    return render(request, 'base/update_task.html', context)


def deleteTask(request, room_id, pk):
    room = get_object_or_404(Room, join_code=room_id)
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('todolist', room_id=room.join_code)
    context = {
        'item': item,
        'room': room
    }
    return render(request, 'base/deleteTask.html', context)




# from .models import Post

from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement, Comment
from .forms import AnnouncementForm, CommentForm




@csrf_exempt
def announcement_detail(request, room_id):
    room = get_object_or_404(Room, join_code=room_id)
    announcements = Announcement.objects.filter(room=room).order_by('-created_on')
    latest_announcement = announcements.first()

    comments = Comment.objects.filter(announcement=latest_announcement)
    comment_form = CommentForm()
    announcement_form = AnnouncementForm()

    new_announcement_id = None  # Initialize the variable outside the conditional blocks

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.author = request.user.member
                new_comment.announcement = latest_announcement
                new_comment.save()
                return redirect('announcement', room_id=room_id)
        elif 'announcement_submit' in request.POST:
            if request.user.is_authenticated and request.user.is_admin:
                announcement_form = AnnouncementForm(request.POST)
                if announcement_form.is_valid():
                    new_announcement = announcement_form.save(commit=False)
                    new_announcement.author = request.user.admin
                    new_announcement.room = room
                    new_announcement.save()

                    # Retrieve the ID of the new announcement
                    new_announcement_id = new_announcement.id

                    return redirect('announcement', room_id=room_id)
                else:
                    # Handle form errors if needed
                    pass
            else:
                return redirect('announcement', room_id=room_id)

    return render(request, 'base/announcement.html', {
        'announcements': announcements,
        'comment_form': comment_form,
        'announcement_form': announcement_form,
        'room': room,
        'latest_announcement': latest_announcement,
        'comments': comments,
        'new_announcement_id': new_announcement_id,  # Pass the new announcement ID to the template
    })




from django.http import HttpResponseForbidden


from django.contrib import messages


from django.shortcuts import redirect

def create_comment(request, room_id, announcement_id):
    room = Room.objects.get(join_code=room_id)
    announcement = get_object_or_404(Announcement, room=room, id=announcement_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            # Check if the user is authenticated
            if request.user.is_authenticated:
                new_comment.author = request.user
                new_comment.announcement = announcement
                new_comment.save()

                # Redirect to the announcement detail page
                return redirect('announcement_view', room_id=room_id, announcement_id=announcement_id)
            else:
                # Handle if the user is not authenticated
                # You might want to redirect them to login or show an error message
                pass
        else:
            # Handle invalid form data if needed
            # You might want to render the form again with error messages
            pass

    # Re-render the announcement detail page if the method is not POST
    return render(request, 'base/view_announcement.html', {
        'comment_form': CommentForm(),
        'room': room,
        'latest_announcement': announcement,
        'comments': announcement.comment_set.all(),
    })

def announcement_view(request, room_id, announcement_id):
    room = get_object_or_404(Room, join_code=room_id)
    announcement = get_object_or_404(Announcement, id=announcement_id, room=room)
    comments = Comment.objects.filter(announcement=announcement)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user if request.user.is_authenticated else None
            new_comment.announcement = announcement
            new_comment.save()
            return redirect('announcement_view', room_id=room_id, announcement_id=announcement_id)
    else:
        comment_form = CommentForm()

    return render(request, 'base/view_announcement.html', {
        'room': room,
        'announcement': announcement,
        'comments': comments,
        'comment_form': comment_form,
    })


from django.urls import reverse
from django.shortcuts import redirect


def create_announcement(request, room_id):
    room = get_object_or_404(Room, join_code=room_id)

    if not (request.user.is_authenticated and
            Admin.objects.filter(user=request.user, room=room).exists()):
        return HttpResponseForbidden("You do not have permission to create an announcement.")

    if request.method == 'POST':
        announcement_form = AnnouncementForm(request.POST)

        if announcement_form.is_valid():
            new_announcement = announcement_form.save(commit=False)

            admin_user = Admin.objects.get(user=request.user, room=room)
            new_announcement.author = admin_user
            new_announcement.room = room
            new_announcement.save()

            messages.success(request, 'Announcement created successfully.')
            return redirect('announcement', room_id=room_id)
        else:
            messages.error(request, 'Form submission failed. Please check your input.')

    return render(request, 'base/create_announcement.html', {
        'announcement_form': AnnouncementForm(),
        'room': room,
    })


from django.shortcuts import render, redirect
from .models import GroupContrib
from .forms import GroupContribForm

from django.shortcuts import render, get_object_or_404
from .models import Room, GroupContrib


# views.py

@csrf_exempt
def group_contrib_view(request, room_id):
    room = get_object_or_404(Room, join_code=room_id)

    # Assuming you have a way to get the currently logged-in user
    current_user = request.user  # Adjust this based on your authentication setup

    # Filter contributions for the current user and the selected users in the room
    contribs = GroupContrib.objects.filter(room=room, user=current_user)

    return render(request, 'base/groupcontrib.html', {
        'contribs': contribs,
        'room': room,
    })


def create_group_contrib(request, room_id):
    room = get_object_or_404(Room, join_code=room_id)

    if request.method == 'POST':
        form = GroupContribForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            selected_users = form.cleaned_data['selected_user_ids']

            # Calculate contribution per user
            contribution_per_user = amount / len(selected_users)

            # Save contributions for each selected user
            for user in selected_users:
                GroupContrib.objects.create(
                    room=room,
                    user=user,
                    amount=contribution_per_user,
                    title=form.cleaned_data['title'],
                    due=form.cleaned_data['due'],
                )

            # Redirect to the group_contrib_view with the selected users
            return redirect('groupcontrib', room_id=room.join_code)

    else:
        form = GroupContribForm()

    return render(request, 'base/create_group_contrib.html', {
        'form': form,
        'room': room,
    })


def dashboard(request, room_id):
    room = Room.objects.get(join_code=room_id)

    context = {
        "room": room,
    }
    return render(request, "base/dashboard.html", context)


def members(request, room_id):
    room = Room.objects.get(join_code=room_id)

    context = {
        "room": room,
    }
    return render(request, "base/member.html", context)


# views.py

from django.http import HttpResponseForbidden


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import MemberForm, AdminForm
from .models import Member, Admin, Room

@login_required
def profile_view(request, room_id, user_id):
    room = get_object_or_404(Room, join_code=room_id)
    form = None
    profile_type = None
    is_owner_or_user = False

    try:
        member = Member.objects.get(user__id=user_id)
        profile_type = 'member'

        if request.method == 'POST':
            form = MemberForm(request.POST, request.FILES, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile_view', room_id=room_id, user_id=user_id)
        else:
            form = MemberForm(instance=member)

    except Member.DoesNotExist:
        try:
            admin = Admin.objects.get(user__id=user_id)
            profile_type = 'admin'

            if request.method == 'POST':
                form = AdminForm(request.POST, request.FILES, instance=admin)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Profile updated successfully.')
                    return redirect('profile_view', room_id=room_id, user_id=user_id)
            else:
                form = AdminForm(instance=admin)

        except Admin.DoesNotExist:
            # If neither member nor admin exists, handle the scenario here
            messages.error(request, 'User profile not found.')
            return redirect('profile_view', room_id=room_id, user_id=request.user.id)

    if profile_type == 'member':
        is_owner_or_user = request.user == member.user
    elif profile_type == 'admin':
        is_owner_or_user = request.user == admin.user

    if not is_owner_or_user:
        for field in form.fields.values():
            field.widget.attrs['disabled'] = True

    return render(request, 'base/profile_view.html', {
        'form': form,
        'room': room,
        'profile_type': profile_type,
        'is_owner_or_user': is_owner_or_user,
    })



def aboutus(request):
    return render(request, 'base/aboutus.html')


def services(request):
    return render(request, 'base/services.html')

def dashboards(request, room_id):
    room = get_object_or_404(Room, join_code=room_id)
    room_members = Member.objects.filter(room=room)
    room_admins = Admin.objects.filter(room=room)

    room_announcement = Announcement.objects.filter(room=room)
    room_bills = bills.objects.filter(room=room).order_by('due')[:3]

    room_group_contrib = GroupContrib.objects.filter(user=request.user, room=room)

    context = {
        "room": room,
        "room_members": room_members,
        "room_admins": room_admins,
        "room_announcement": room_announcement,
        "room_bills": room_bills,
        "room_group_contrib": room_group_contrib,
    }
    return render(request, "base/dashboard.html", context)

def website_policy(request, room_id):
    room = get_object_or_404(Room, join_code=room_id)

    context = {
        "room": room,
    }
    return render(request, "base/policy1.html", context)

# transferadmin
# leavedorm