from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rentalapp.models.cars import *
from rentalapp.models.car_features import CarFeatures
from django.db.models import Avg, Sum
from django.utils import timezone
from datetime import timedelta, date
from .forms import *
from rentalapp.models.users import *
from django.contrib.auth.hashers import make_password
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
def admin_view_user_details(request, id):
    user = User.objects.get(id=id)
    notifications = UserNotification.objects.filter(user=user).order_by('-created_at')
    tasks = LeadsTasks.objects.filter(user=user).order_by('-date_time')
    notes = LeadsNotes.objects.filter(user=user).order_by('-created_on')
    context = {
        'user': user,
        'notifications': notifications,
        'form': LeadsTasksForm(),
        'task_count': tasks.count(),
        'tasks': tasks,
        'notes_count': notes.count(),
        'notes': notes,
        'notes_form': LeadsNotesForm(),
        'sendmail_form': SendMailForm()
    }
    return render(request, template_name="admin/home/app/user_details.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_tasks(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = LeadsTasksForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                messages.success(request, f"Successfully created task of {user.username}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "form is invalid")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url="/secure-admin/auth/private/login")
def admin_edit_tasks(request, id):
    task = LeadsTasks.objects.get(id=id)
    if request.method == "POST":
        form = LeadsTasksForm(request.POST, instance=task)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Successfully updated task of {task.task_title}")
                return redirect('admin_view_user_details', task.user.id)
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "form is invalid")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = LeadsTasksForm(instance=task)
    
    return render(request, template_name="admin/home/app/admin_update_task.html", context={'updateform':form, 'task': task})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_delete_tasks(request, id):
    task = LeadsTasks.objects.get(id=id)
    if request.user.is_staff:
        task.delete()
        messages.warning(request, f"Successfully deleted {task.task_title}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exists'}, status=404)
    except Exception as e:
        messages.warning(request, str(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
        car = Cars.objects.get(slug=booking.car.slug)
        if booking.car.in_stock is False:
            car.in_stock = True
            car.save()
        booking.delete()
        messages.warning(request, f"{car.brand}' booking is deleted")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Booking.DoesNotExist:
        return JsonResponse({'error': 'Booking info does not exists'}, status=404)
    except Exception as e:
        messages.warning(request, str(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url="/secure-admin/auth/private/login")
def admin_all_cars(request):
    context ={
        'cars': Cars.objects.all().order_by('-year')
    }
    return render(request, template_name="admin/home/page/all_cars.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_car_categories(request):
    context = {
        'car_types': CarTypes.objects.all()
    }
    return render(request, template_name="admin/home/page/car_categories.html", context=context)

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
            messages.warning(request, str(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def update_car_categories(request, slug):
    car_types = CarTypes.objects.get(slug=slug)
    if request.method == "POST":
        types = request.POST.get('car_types')
        category_images = request.FILES.get('category_images')
        price_detail = request.POST.get('price_detail')
        slug = request.POST.get('slug')
        try:
            if category_images is None:
                messages.warning(request, f"Empty image upload field")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            car_types.car_types = types
            car_types.category_images = category_images
            car_types.price_detail = price_detail
            car_types.slug = slug
            car_types.save()
            messages.success(request, f"Successfully updated {types}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
            messages.warning(request, str(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
        messages.warning(request, str(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_new_car(request):
    context = {
        'types': CarTypes.objects.all()
    }
    return render(request, template_name="admin/home/page/add_new_car.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def add_new_car(request):
    if request.method == "POST":
        category = request.POST.get('category')
        car_brand = request.POST.get('car_brand')
        car_number = request.POST.get('car_number')
        car_slug = request.POST.get('slug')
        car_year = request.POST.get('year')
        desc = request.POST.get('desc')
        body_type = request.POST.get('body_type')
        engine = request.POST.get('engine')
        fuel_type = request.POST.get('fuel_type')
        exterior_color = request.POST.get('exterior_color')
        actual_price = int(request.POST.get('actual_price'))
        discounted_price = int(request.POST.get('discounted_price'))
        in_stock = bool(request.POST.get('in_stock'))

        try:
            if not all([category, car_brand, car_number, car_slug, car_year, body_type, engine, fuel_type, actual_price, exterior_color, discounted_price, in_stock]):
                messages.warning(request, "Required fields are missing")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            car_type = CarTypes.objects.filter(car_types=category).first()
            if not car_type:
                messages.warning(request, f"Car type '{category}' does not exist")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            if Cars.objects.filter(brand=car_brand, slug=car_slug).exists():
                messages.warning(request, f"Car Brand: {car_brand} & Slug: {car_slug} already exists")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            car = Cars(
                car_type=car_type,
                brand=car_brand,
                car_number=car_number,
                slug=car_slug,
                year=car_year,
                desc=desc,
                body_type=body_type,
                engine=engine,
                fuel_type=fuel_type,
                exterior_color=exterior_color,
                actual_price=actual_price,
                discounted_price=discounted_price,
                in_stock=in_stock
            )
            car.save()
            # car images uploading in bulk
            car_images = request.FILES.getlist('car_images')
            for image in car_images:
                CarImages.objects.create(cars=car, car_images=image)
            
            messages.success(request, "Car added successfully")
            return redirect('admin_all_cars')
            
        except Exception as e:
            messages.warning(request, str(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def delete_car(request, slug):
    try:
        car = Cars.objects.get(slug=slug)
        car.delete()
        messages.warning(request, f"{car.brand} delete successfully")
        return redirect('admin_all_cars')
    except Cars.DoesNotExist:
        return JsonResponse({'error': 'Car object does not exists'}, status=404)
    except Exception as e:
        messages.warning(request, str(e))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_show_car_details(request, slug):
    car = Cars.objects.get(slug=slug)
    average_review = CarReviews.objects.filter(cars=car).aggregate(rating=Avg('rating'))
    context = {
        'car': car,
        'average_review': average_review
    }
    return render(request, template_name="admin/home/page/show_car_details.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_update_car_details(request, slug):
    cars = Cars.objects.get(slug=slug)
    if request.method == "POST":
        category = request.POST.get('category')
        car_brand = request.POST.get('car_brand')
        car_number = request.POST.get('car_number')
        car_slug = request.POST.get('slug')
        car_year = request.POST.get('year')
        desc = request.POST.get('desc')
        body_type = request.POST.get('body_type')
        engine = request.POST.get('engine')
        fuel_type = request.POST.get('fuel_type')
        exterior_color = request.POST.get('exterior_color')
        actual_price = int(request.POST.get('actual_price'))
        discounted_price = int(request.POST.get('discounted_price'))
        in_stock = request.POST.get('in_stock')

        try:
            if not all([category, car_brand, car_number, car_slug, car_year, body_type, engine, fuel_type, actual_price, exterior_color, discounted_price, in_stock]):
                messages.warning(request, "Required fields are missing")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            car_type = CarTypes.objects.filter(car_types=category).first()
            if not car_type:
                messages.warning(request, f"Car type '{category}' does not exist")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            cars.car_type = car_type
            cars.brand = car_brand
            cars.car_number = car_number
            cars.slug = car_slug
            cars.year = car_year
            cars.desc = desc
            cars.body_type = body_type
            cars.engine = engine
            cars.fuel_type = fuel_type
            cars.exterior_color = exterior_color
            cars.actual_price = actual_price
            cars.discounted_price = discounted_price
            cars.in_stock = in_stock
            cars.save()
            
            messages.success(request, f"{car_brand} car updated successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        except Exception as e:
            messages.warning(request, str(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="/secure-admin/auth/private/login")
def admin_new_features(request):    
    context={
        'cars': Cars.objects.all()
    }
    return render(request, template_name="admin/home/page/add_new_features.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def add_new_features(request):
    if request.method == "POST":
        car = request.POST.get('cars')
        feature = request.POST.get('features')
        try:
            if not all([car, feature]):
                messages.warning(request, "Required fields are missing")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            cars = Cars.objects.filter(brand=car).first()
            if not cars:
                messages.warning(request, f"This '{car}' car does not exist")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if CarFeatures.objects.filter(cars=cars, features=feature).exists():
                messages.warning(request, f"This {feature} feature in {car} already exists")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            feature = CarFeatures(cars=cars, features=feature)
            feature.save()
            messages.success(request, f"{feature} added in {car} successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
        except Exception as e:
            messages.warning(request, str(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def delete_car_features(request, feature_id):
    feature = CarFeatures.objects.get(feature_id=feature_id)
    feature.delete()
    messages.warning(request, f"{feature.features} delete successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def update_car_features(request, feature_id):
    features = CarFeatures.objects.get(feature_id=feature_id)
    if request.method == "POST":
        car = request.POST.get('cars')
        feature = request.POST.get('features')
        try:
            if not all([car, feature]):
                messages.warning(request, "Required fields are missing")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            cars = Cars.objects.filter(brand=car).first()
            if not cars:
                messages.warning(request, f"This '{car}' car does not exist")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if CarFeatures.objects.filter(cars=cars, features=feature).exists():
                messages.warning(request, f"This {feature} feature in {car} already exists, update new one.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            features.cars = cars
            features.features = feature
            features.save()
            messages.success(request, f"{feature} updated in {car} successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
        except Exception as e:
            messages.warning(request, str(e))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_view_blog(request):
    context={
        'blogs': BlogsDetail.objects.all().order_by('-created_at')
    }
    return render(request, template_name="admin/home/page/admin_view_blog.html", context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
                messages.success(request, f"Successfully added {instance.title} blog.")
                return redirect('admin_view_blog')
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Form is invalid.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, template_name="admin/home/page/admin_add_blog.html", context={'form': BlogForm})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_delete_blog(request, slug):
    blog_obj = BlogsDetail.objects.get(slug=slug)
    if blog_obj.author == request.user:
        blog_obj.delete()
        messages.warning(request, f"Successfully deleted {blog_obj.title}.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_update_blog(request, id):
    blog = get_object_or_404(BlogsDetail, id=id)
    if request.method == 'POST':
        form = BlogUpdateForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Successfully updated {blog.title}.")
                return redirect('admin_view_blog')
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Form is invalid.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = BlogUpdateForm(instance=blog)
    
    return render(request, 'admin/home/page/admin_update_blog.html', context={'form': form, 'blog': blog})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_faqs_list(request):
    return render(request, template_name="admin/home/page/admin_faqs_list.html", context={'faqs': Faq.objects.all()})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_new_faqs(request):
    if request.method == "POST":
        form = FaqForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Successfully added faq.")
                return redirect('admin_faqs_list')
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Form is invalid.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = FaqForm()
    return render(request, template_name="admin/home/page/admin_new_faq.html", context={'form': form})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_update_faq(request, id):
    faq = get_object_or_404(Faq, id=id)
    if request.method == 'POST':
        form = FaqForm(request.POST, instance=faq)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Successfully updated {faq.question}.")
                return redirect('admin_faqs_list')
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Form is invalid.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = FaqForm(instance=faq)
    
    return render(request, 'admin/home/page/admin_update_faq.html', context={'form': form, 'faq': faq})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_delete_faq(request, id):
    faq = get_object_or_404(Faq, id=id)
    if request.user.is_staff:
        faq.delete()
        messages.warning(request, f"{faq.question} deleted successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_contact_form_details(request):
    context = {'contact': ContactUs.objects.all().order_by('-created_on')}
    return render(request, 'admin/home/app/admin_contact_form_details.html', context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_delete_contact(request, id):
    contact = ContactUs.objects.get(id=id)
    if request.user.is_superuser or request.user.is_staff:
        contact.delete()
        messages.warning(request, f"{contact.message} from contact form deleted successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_all_tasks(request):
    context = {'tasks': LeadsTasks.objects.all().order_by('-date_time')}
    return render(request, 'admin/home/app/admin_all_tasks.html', context=context)

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_notes(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = LeadsNotesForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.user = user
                instance.save()
                messages.success(request, f"{instance.notes} added successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Invalid form submission")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_edit_notes(request, id):
    note = LeadsNotes.objects.get(id=id)
    if request.method == "POST":
        form = LeadsNotesForm(request.POST, instance=note)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Successfully updated task of {note.notes}")
                return redirect('admin_view_user_details', note.user.id)
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "form is invalid")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = LeadsNotesForm(instance=note)
    
    return render(request, template_name="admin/home/app/admin_update_note.html", context={'updatenotes_form':form, 'note': note})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_delete_notes(request, id):
    notes = LeadsNotes.objects.get(id=id)
    if request.user.is_staff:
        notes.delete()
        messages.warning(request, f"Successfully deleted {notes.notes}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_send_mail_to_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = SendMailForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.sender = settings.EMAIL_HOST_USER
                instance.save()
                instance.receiver.add(user)
                receivers_emails = [receiver.email for receiver in instance.receiver.all()]
                receivers_email = str(receivers_emails[0])
                send_mail_to_user(instance.sender, receivers_email, instance.subject, instance.message)
                messages.success(request, f"Sent mail to {receivers_email} successfully!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Invalid form submission")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_custom_page(request):
    return render(request, template_name="admin/home/page/admin_custom_page.html", context={'customs': CustomPage.objects.all()})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_custom(request):
    if request.method == "POST":
        form = CustomPageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Add page successfully!")
                return redirect('admin_custom_page')
            except Exception as e:
                messages.warning(request, str(e))
        else:
            messages.warning(request, "Invalid form submission")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        custom_form = CustomPageForm()    
    return render(request, template_name="admin/home/page/admin_add_custom.html", context={'custom_form': custom_form})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_update_custom(request, slug):
    custom = CustomPage.objects.get(slug=slug)
    if request.method == "POST":
        form = CustomPageForm(request.POST, request.FILES, instance=custom)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Updated {custom.title} page successfully!")
                return redirect('admin_custom_page')
            except Exception as e:
                messages.warning(request, str(e))
        else:
            messages.warning(request, "Invalid form submission")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        custom_form = CustomPageForm(instance=custom)    
    return render(request, template_name="admin/home/page/admin_update_custom.html", context={'custom_form': custom_form, 'custom':custom})


@login_required(login_url="/secure-admin/auth/private/login")
def admin_delete_custom(request, slug):
    custom = CustomPage.objects.get(slug=slug)
    if request.user.is_staff:
        custom.delete()
        messages.warning(request, f"{custom.title} delete successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_user(request):
    if request.user.is_superuser:
        if request.method == "POST":
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                try:
                    instance = user_form.save(commit=False)
                    if User.objects.filter(email=instance.email).exists():
                        messages.warning(request, f"{instance.email} is already taken. Please use another one.")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    instance.password = make_password(user_form.cleaned_data['password'])
                    instance.save()
                    messages.success(request, f"Added {instance.username} successfully!")
                    return redirect('admin_add_profile')
                except Exception as e:
                    messages.warning(request, str(e))
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.warning(request, "Invalid form submission")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_form = UserForm()
    else:
        messages.warning(request, "Sorry! You are not authorized.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, template_name="admin/home/app/add_new_user.html", context={'user_form': user_form})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_profile(request):
    if request.user.is_superuser:
        if request.method == "POST":
            profile_form = ProfileForm(request.POST, request.FILES)
            if profile_form.is_valid():
                try:
                    instance = profile_form.save(commit=False)
                    instance.save()
                    messages.success(request, f"Added successfully!")
                    return redirect('admin_customers')
                except Exception as e:
                    messages.warning(request, str(e))
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.warning(request, "Invalid form submission")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        profile_form = ProfileForm()
    else:
        messages.warning(request, "Sorry! You are not authorized.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, template_name="admin/home/app/add_new_profile.html", context={'profile_form': profile_form})

@login_required(login_url="/secure-admin/auth/private/login")
def admin_add_booking(request):
    if request.user.is_superuser:
        if request.method == "POST":
            booking_form = BookingForm(request.POST, request.FILES)
            if booking_form.is_valid():
                try:
                    instance = booking_form.save(commit=False)
                    car = Cars.objects.get(slug=instance.car.slug)
                    if not car.in_stock:
                        messages.warning(request, f"{car.brand} is not available. Please book another car")
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    else:
                        instance.total_days = (instance.return_date - instance.pickup_date).days
                        instance.save()
                        car.in_stock = False
                        car.save()
                        messages.success(request, f"Added booking successfully!")
                        return redirect('admin_user_orders')
                except Exception as e:
                    messages.warning(request, str(e))
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.warning(request, "Invalid form submission")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        booking_form = BookingForm()
    else:
        messages.warning(request, "Sorry! You are not authorized.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, template_name="admin/home/app/add_new_booking.html", context={'booking_form': booking_form})