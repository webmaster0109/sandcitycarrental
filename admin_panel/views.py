from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rentalapp.models.cars import *
from django.db.models import Avg, Sum
from django.utils import timezone
from datetime import timedelta, date
# Create your views here.

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin_obj = authenticate(request, username=username, password=password)
        if admin_obj and admin_obj.is_staff:
            login(request, admin_obj)
            return redirect('admin_dashboard')
        else:
            messages.warning(request, "Invalid username or password. Please try again.")
            return redirect('admin_login')
    return render(request, template_name="admin/authentication/admin_login.html")

def get_users():
    return User.objects.filter(profile__is_verified=True, is_staff=False)

def get_total_users():
    return get_users().count()

def get_total_users_details():
    return get_users().order_by('-date_joined')[:6]

def get_bookings():
    return Booking.objects.filter(is_paid=True)

def get_cash_amount():
    cash = Booking.objects.filter(is_paid=True, payment_mode='Cash in Hand')
    cash_in_hand = []
    for cash in cash:
        cash_in_hand.append(cash.total_price)
    return '{:,.0f}'.format(sum(cash_in_hand))
    
def get_bank_amount():
    bank = Booking.objects.filter(is_paid=True, payment_mode='Transfer to Bank')
    bank_transfer = []
    for bank in bank:
        bank_transfer.append(bank.total_price)
    return '{:,.0f}'.format(sum(bank_transfer))

def get_security_amount():
    security = Booking.objects.filter(is_paid=True)
    security_amount = []
    for security in security:
        security_amount.append(security.security_amount())
    return '{:,.0f}'.format(sum(security_amount))

def get_total_income():
    total_income = []
    bookings = get_bookings()
    for booking in bookings:
        if booking.total_price > 0:
            total_income.append(booking.total_price)
        else:
            total_income.append(0)
    return '{:,.2f}'.format(sum(total_income))

def get_net_income():
    net_income = []
    bookings = get_bookings()
    for booking in bookings:
        if booking.total_amount() > 0:
            net_income.append(booking.total_amount())
        else:
            net_income.append(0)
    return '{:,.0f}'.format(sum(net_income))

def get_total_order():
    return get_bookings().count()

def get_average_total_price():
    today = date.today()
    average_price = Booking.objects.filter(
        created_at__date=today,  # Filter bookings created today
        is_paid=True  # Consider only paid bookings
    ).aggregate(avg_price=Sum('total_price'))
    average_price = average_price['avg_price'] or 0
    # average_price = get_bookings().aggregate(avg_price=Avg('total_price'))
    return '{:,.0f}'.format(average_price)

def get_daily_sales():
    today = timezone.now()
    five_days_ago = today - timedelta(days=5)
    daily_sales = Booking.objects.filter(created_at__gte=five_days_ago, created_at__lte=today, is_paid=True).values('created_at__date').annotate(total_sales=Sum('total_price')).order_by('-created_at__date')[:5]
    return daily_sales

@login_required(login_url="/secure-admin/auth/private/login")
def admin_dashboard(request):
    total_users_count = get_total_users()
    total_users = get_total_users_details()
    total_income = get_total_income()
    total_orders_goal = 20
    percentage = (get_total_order() * 100) // total_orders_goal
    average_booking = get_average_total_price()
    today = date.today()
    one_day_ago = today - timedelta(days=1)
    yesterday_booking_amount = Booking.objects.filter(created_at__date=one_day_ago).aggregate(total_price=Sum('total_price'))['total_price'] or 0
    today_booking_date = Booking.objects.filter(created_at__date=today).aggregate(total_price=Sum('total_price'))['total_price'] or 0

    if yesterday_booking_amount != 0:
        booking_percentage = ((today_booking_date - yesterday_booking_amount) / yesterday_booking_amount) * 100
    else:
        booking_percentage= 0
    
    booking_percentage = float('{:.2f}'.format(booking_percentage))
    print(type(booking_percentage))

    context = {
        'total_users_count': total_users_count,
        'total_users': total_users,
        'total_income': total_income,
        'total_orders': get_total_order(),
        'total_goals_percentage' : percentage,
        'total_orders_goal': total_orders_goal - get_total_order(),
        'average_booking': average_booking,
        'net_income' : get_net_income(),
        'bookings': get_daily_sales(),
        'get_cash_amount': int(get_cash_amount().replace(',', '')),
        'get_bank_amount': int(get_bank_amount().replace(',','')),
        'get_security_amount': int(get_security_amount().replace(',','')),
        'booking_percentage': booking_percentage,
        'copyrights_year': date.today()
    }
    return render(request, template_name="admin/home/dashboard.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_calendar(request):

    return render(request, template_name="admin/home/app/calender.html", context={'copyrights_year': date.today()})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_customers(request):
    context = {
        'users': User.objects.filter(is_staff=False).exclude(username="random01092004guy")
    }
    return render(request, template_name="admin/home/app/customers.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exists'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_notifications(request):
    notifications = request.user.usernotification_set.all().order_by('-created_at')
    # Mark notifications as read
    for notification in notifications:
        notification.mark_as_read()
    context = {
        'notifications': notifications
    }
    return render(request, template_name="admin/home/app/notifications.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_user_orders(request):
    context ={
        'bookings': Booking.objects.all()
    }
    return render(request, template_name="admin/home/app/orders.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def delete_booking(request, id):
    try:
        booking = Booking.objects.get(id=id)
        booking.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking info does not exists'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required(login_url="/secure-admin/auth/private/login")
def admin_all_cars(request):
    context ={
        'cars': Cars.objects.all().order_by('-year')
    }
    return render(request, template_name="admin/home/app/all_cars.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_car_categories(request):
    context = {
        'car_types': CarTypes.objects.all()
    }
    return render(request, template_name="admin/home/app/car_categories.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def add_car_categories(request):
    if request.method == "POST":
        types = request.POST.get('car_types')
        category_images = request.FILES.get('category_images')
        price_detail = request.POST.get('price_detail')
        slug = request.POST.get('slug')
        try:
            car_type = CarTypes.objects.filter(car_types=types, slug=slug).first()
            if car_type:
                messages.warning(request, f"Already added Type: {types} & Slug: {slug}. Please type another one.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            car_type = CarTypes(car_types=types, category_images=category_images, price_detail=price_detail, slug=slug)
            car_type.save()
            messages.success(request, f"Successfully added {types}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_delete_category(request, slug):
    try:
        car_type = CarTypes.objects.get(slug=slug)
        car_type.delete()
        messages.warning(request, f"Successfully deleted {car_type.car_types}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except CarTypes.DoesNotExist:
        return JsonResponse({'error': 'Booking info does not exists'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_new_car(request):
    context = {
        'types': CarTypes.objects.all()
    }
    return render(request, template_name="admin/home/app/add_new_car.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def add_new_car(request):
    if request.method == "POST":
        category = request.POST.get('category')
        car_brand = request.POST.get('car_brand')
        car_number = request.POST.get('car_number')
        slug = request.POST.get('slug')
        car_year = request.POST.get('year')
        desc = request.POST.get('desc')
        body_type = request.POST.get('body_type')
        engine = request.POST.get('engine')
        fuel_type = request.POST.get('fuel_type')
        exterior_color = request.POST.get('exterior_color')
        actual_price = request.POST.get('actual_price')
        discounted_price = request.POST.get('discounted_price')
        in_stock = request.POST.get('in_stock')
        # car images uploading in bulk
        car_images = request.FILES.getlist('car_images')


        for image in car_images:
            car_image = CarImages.objects.create(car_images=image)
            # Associate the image with a specific car (assuming you have a car instance available)
            # car_image.cars = car 
            car_image.save()
