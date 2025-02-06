from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import models
from home.models import Booking, BookPc
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now  # Import the `now` function
import json

User = get_user_model()

def home(request):
    return render(request, "index.html")

# change func name 
def loginPage(request):
    return render(request, 'login.html') #chng file name 

def contactPage(request):
    return render(request, 'contact.html') #chng file name 

def rentalPage(request):
    return render(request, 'rental.html') #chng file name 

def searchUser(request):
    return render(request, 'search-user.html') #chng file name 

def HistoryPage(request):
    return render(request, 'History.html')

def signup(request):
    # referer_url = request.META.get('HTTP_REFERER', '/')
    if request.method == "POST":
        username= request.POST.get('username')
        email = request.POST.get('email')
        pswd = request.POST.get('password')
        if User.objects.filter(username=email).exists():
          return render(request, '/', {'error': 'Email is already in use.'})
        user = User.objects.create_user(username=username, password=pswd, email=email)

        referer_url = request.GET.get('next', '/')  # Get 'next' from the URL parameters
        login(request, user)
        print(referer_url)
        return redirect("/")
        # print(user)
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/")

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("logged in")
            return redirect('/')
        else:
            print("invalid")
            return redirect("/signup")

def booking(request):
    available_pcs = list(set(range(1, 4)) - set(BookPc.objects.values_list('pc_number', flat=True)))
    print(available_pcs.__len__())
    
    return render(request, 'booking.html', {"avl_pc":available_pcs.__len__()}) #chng file name 

@csrf_exempt
def save_booking(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("user_id")  # Assuming user ID is passed in request
        days = data.get("days")
        controllers = data.get("controllers")
        amount = data.get("amount")
        console = data.get("console")
        
        # Save booking to the database
        try:
            user = User.objects.get(id=user_id)
            booking = Booking.objects.create(
                user=user,
                days = int(data.get("days", 1)),
                controllers=controllers,
                console=console,
                amount=amount,
                booking_date=now(),
            )
            return JsonResponse({
                "success": True,
                "booking_id": booking.id,
                "booking_date": booking.booking_date,
                "pickup_date": booking.pickup_date,
                "return_date": booking.return_date,
                "amount": amount,
                "controllers":controllers,
                "days":days,
            }, status=201)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid user ID"}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

@csrf_exempt
def book_pc(request):
    if request.method == "POST":
        user = request.user
        duration = int(request.POST.get("duration"))
        time_string = request.POST.get("start_time")
        try:
            # Attempt parsing as 12-hour format
            start_time = datetime.strptime(time_string, "%I:%M %p").time()
        except ValueError:
            # Fallback to 24-hour format
            start_time = datetime.strptime(time_string, "%H:%M").time()

        # Calculate the end time
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=duration)).time()

        # Check if any PC is available
        available_pcs = list(set(range(1, 4)) - set(BookPc.objects.values_list('pc_number', flat=True)))

        print(available_pcs.__len__())

        if not available_pcs:
            return JsonResponse({"success": False, "message": "All PCs are fully booked."})

        # Assign the first available PC
        pc_number = available_pcs[0]
        # Save the booking
        BookPc.objects.create(
            user=user,
            pc_number=pc_number,
            duration=duration,
            start_time=start_time,
            end_time=end_time,
        )

        return JsonResponse({
            "success": True,
            "message": f"PC {pc_number} has been booked successfully.",
            "pc_number": pc_number,
            "start_time": start_time.strftime("%I:%M %p"),
            "end_time": end_time.strftime("%I:%M %p"),
            "avl_pc":available_pcs.__len__()-1,
        })

    return JsonResponse({"success": False, "message": "Invalid request method."})

def search_user(request):
    query = request.GET.get('username', '').strip()  # Get the username query from the request
    if query:
        users = User.objects.filter(username__icontains=query)  # Perform a case-insensitive search
        user_list = [
            {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'email': user.email,
                'last_login': user.last_login,
                'date_joined': user.date_joined
                # Add more fields as needed
            }
            for user in users
        ]
        return JsonResponse({'success': True, 'users': user_list})
    return JsonResponse({'success': False, 'message': 'No username provided'})

def get_users_by_date(request):
    start_date = request.GET.get('start_date')  # Example: "2025-01-01"
    end_date = request.GET.get('end_date')  # Example: "2025-01-31"

    if not start_date or not end_date:
        return JsonResponse({'success': False, 'message': 'Start date and end date are required.'}, status=400)

    try:
        # Parse the date strings into datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filter users by joined_date
        users = User.objects.filter(date_joined__date__range=(start_date, end_date))
        user_list = [
            {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'email': user.email,
                'last_login': user.last_login,
                'date_joined': user.date_joined
            }
            for user in users
        ]

        return JsonResponse({'success': True, 'users': user_list})
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)


@csrf_exempt  # Disable CSRF for testing
def make_user_prime(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.is_prime = True
        user.save()
        return JsonResponse({"message": "User is now a prime member", "user_id": user.id, "is_prime": user.is_prime, 'success':'true'})
    return JsonResponse({"error": "Invalid request method"}, status=400)
