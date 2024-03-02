from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from rentalapp.models.users import ContactUs, send_contact_form_email
from rentalapp.models.cars import CarTypes, Cars, Booking
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rentalapp.models.newsletter import EmailNewsletters, send_newsletter_email
from rentalapp.models.blogs import BlogsDetail
from hitcount.views import HitCountDetailView

def home_page(request):
    category = CarTypes.objects.all()
    return render(request, template_name="frontend/index.html", context={'category':category})

def signup_newsletter(request):
    if request.method == "POST":
        email = request.POST.get('email')
        email_obj = EmailNewsletters.objects.filter(email=email).first()

        if email_obj and email_obj.is_subscribe:
            messages.warning(request, "Your email address has already been registered")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        email_obj = EmailNewsletters.objects.create(email=email)
        send_newsletter_email(email_obj)
        messages.success(request, "You've successfully registered newsletter signup.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def menu_items(request):
    cars = Cars.objects.all()
    car_types = CarTypes.objects.all()
    return {'car_detail': cars, 'car_types': car_types}

def calculate_dynamic_price(discounted_price, total_days):
    if total_days == 1:
        return discounted_price
    elif total_days == 2:
        return discounted_price - 50
    elif 3 <= total_days <= 6:
        return discounted_price - 100
    elif 7 <= total_days <= 29:
        return discounted_price - 150
    else:
        return discounted_price - 180

def booking_search(request):
    if request.method == 'GET':
        selected_category = request.GET.get('car_category')
        pickup_date = request.GET.get('pickup_date')
        return_date = request.GET.get('return_date')

        if not all([selected_category, pickup_date, return_date]):
            return redirect('homepage')
        

        request.session['car_type'] = selected_category

        # Start with all bookings
        filtered_bookings = Booking.objects.all()

        available_cars = Cars.objects.exclude(
            Q(booking__pickup_date__lte=return_date, booking__return_date__gte=pickup_date) |
            Q(booking__pickup_date__gte=pickup_date, booking__return_date__lte=return_date) |
            Q(booking__pickup_date__lte=pickup_date, booking__return_date__gte=return_date)
        ).filter(car_type__car_types=selected_category)

        try:
            pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError(_('Invalid date format. Please use YYYY-MM-DD format.'))

        # Filter by category
        if selected_category:
            filtered_bookings = filtered_bookings.filter(car__car_type__car_types=selected_category)

        # Filter by pickup date
        if pickup_date:
            filtered_bookings = filtered_bookings.filter(pickup_date__gte=pickup_date)

        # Filter by return date
        if return_date:
            filtered_bookings = filtered_bookings.filter(return_date__lte=return_date)

        total_days = (return_date - pickup_date).days

        car_prices = {}
        for car in available_cars:
            dynamic_price = calculate_dynamic_price(car.discounted_price, total_days)
            car.total_price = total_days * dynamic_price
            total_price = total_days * dynamic_price
            car_prices[car.slug] = {'total_price': total_price, 'total_days': total_days}
        
        request.session['car_prices'] = car_prices

        # Pass the filtered bookings to the template
        context = {
            'categories': CarTypes.objects.all(),
            'filtered_bookings': available_cars,
            'total_days': total_days,
            'car_type': request.session['car_type']
        }

    return render(request, 'frontend/booking_search.html', context=context)

def all_cars(request):
    context={'cars': Cars.objects.all(),}
    return render(request, template_name="frontend/cars.html", context=context)

def about_us(request):
    return render(request, template_name="frontend/about_us.html")

def car_category(request, slug):
    request.session.clear()
    category = get_object_or_404(CarTypes, slug=slug)
    try :
        selected_car_type = request.GET.get('car_type')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        filtered_cars = category.cars_set.all()
        min_price = str(min_price).split('.')[0]
        max_price = str(max_price).split('.')[0]
        # Filter by car type
        if selected_car_type:
            filtered_cars = filtered_cars.filter(car_type__car_types=selected_car_type)

        # Filter by price range
        if min_price and max_price:
            filtered_cars = filtered_cars.filter(discounted_price__gte=min_price, discounted_price__lte=max_price)
    except Exception as e:
        print(e)

    # Pass the filtered cars to the template
    context = {
        'car_types': CarTypes.objects.all(),
        'category': category,
        'filtered_cars': filtered_cars,
    }

    return render(request, template_name="frontend/car_category.html", context=context)

def car_details(request, slug):
    cars = get_object_or_404(Cars, slug=slug)
    car_id = cars.slug

    if request.method == 'GET':
        pickup_date = request.GET.get('pickup_date')
        return_date = request.GET.get('return_date')

        if pickup_date and return_date:
            pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date()

            if pickup_date < datetime.now().date():
                messages.warning(request, "Pickup date should be not less than today")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
            if return_date < pickup_date:
                messages.warning(request, "Return date is less than pickup date.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            booking_days = (return_date - pickup_date).days
            discounted_price = cars.discounted_price
            total_price = booking_days * discounted_price

            car_prices = {}
            if booking_days > 1:
                car_prices[car_id] = {'total_price': total_price, 'total_days': booking_days}
            request.session['car_prices'] = car_prices
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    car_prices = request.session.get('car_prices', {})
    car_info = car_prices.get(car_id, {})
    total_days = car_info.get('total_days')
    total_price = car_info.get('total_price')

    context = {
        'cars' : cars,
        'total_days': total_days,
        'total_price': total_price,
        'car_detail': Cars.objects.all()
    }

    return render(request, template_name="frontend/car_detail.html", context=context)

@login_required(login_url='/auth/login')
def add_to_cart(request, slug):
    car_obj = Cars.objects.get(slug=slug)
    user_obj = request.user

    old_cart_items = Booking.objects.filter(user=user_obj)

    old_cart_items.delete()

    car_prices = request.session.get('car_prices', {})
    car_info = car_prices.get(car_obj.slug, {})
    total_days = car_info.get('total_days')
    total_price = car_info.get('total_price')
    cart_item = Booking.objects.create(car=car_obj, user=user_obj)
    if total_days and total_price:
        cart_item.total_day = total_days
        cart_item.total_price = total_price
        cart_item.save()
    else:
        cart_item.total_day = 1
        cart_item.total_price = car_obj.discounted_price
        cart_item.save()
    messages.success(request, 'Added to cart, make your payment now...')
    return redirect('cart')

def cart(request):    
    cart_obj = None
    user = request.user
    
    try:
        cart_obj = Booking.objects.get(is_paid=False, user=user)
    except Exception as e:
        print(e)

    context = {
        'cart' : cart_obj,
    }
    return render(request, template_name="frontend/cart.html", context=context)

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact_obj = ContactUs(name=name, email=email, number=phone, message=message)
        contact_obj.save()
        send_contact_form_email(contact_obj)
    
        messages.success(request, "You have successfully submitted form. We'll reach you soon!")
        return redirect('contact_us')

    return render(request, template_name="frontend/contact_us.html")

def privacy_policy(request):

    return render(request, template_name="frontend/privacy_policy.html")

def terms_condititon(request):

    return render(request, template_name="frontend/terms_condititon.html")

def help_center(request):
    return render(request, template_name="frontend/help_center.html")

def faqs(request):
    return render(request, template_name="frontend/faqs.html")

def blogs_page(request):
    context = {
        'blogs' : BlogsDetail.objects.all(),
    }
    return render(request, template_name="frontend/blog_site/blogs.html", context=context)

class PostDetailView(HitCountDetailView):
    model = BlogsDetail
    template_name = 'frontend/blog_site/blog_detail.html'
    context_object_name = 'blog'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': BlogsDetail.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context