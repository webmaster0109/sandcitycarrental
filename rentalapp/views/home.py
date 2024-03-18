import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from rentalapp.models.users import ContactUs, send_contact_form_email
from rentalapp.models.cars import CarTypes, Cars, Booking, CarReviews
from rentalapp.models.faqs import Faq
from django.contrib import messages
from django.db.models import Q, Avg, Count
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rentalapp.models.newsletter import EmailNewsletters, send_newsletter_email
from rentalapp.models.blogs import BlogsDetail
from hitcount.views import HitCountDetailView
from django.template.defaultfilters import striptags
import math
from rentalapp.models.custom_page import CustomPage
from rentalapp.models.users import UserNotification
from django.contrib.auth.models import User

def home_page(request):
    category = CarTypes.objects.all()
    return render(request, template_name="frontend/index.html", context={'category':category})

def add_to_wishlists(request, slug):
    if request.user.is_authenticated:
        car = get_object_or_404(Cars, slug=slug)
        user_profile = request.user.profile
        if car not in user_profile.wishlists.all():
            user_profile.wishlists.add(car)
            messages.success(request, "Successfully added to wishlist")
        else:
            messages.warning(request, "Already in wishlist")
    else:
        messages.error(request, "You need to be logged in to add to wishlist")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_to_wishlists(request, slug):
    if request.user.is_authenticated:
        car = get_object_or_404(Cars, slug=slug)
        user_profile = request.user.profile
        if car in user_profile.wishlists.all():
            user_profile.wishlists.remove(car)
            messages.success(request, "Successfully removed from wishlist")
        else:
            messages.warning(request, "Item not in wishlist")
    else:
        messages.error(request, "You need to be logged in to remove from wishlist")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
        pickup_date_str = request.GET.get('pickup_date')
        return_date_str = request.GET.get('return_date')

        if not all([selected_category, pickup_date_str, return_date_str]):
            return redirect('homepage')
        

        request.session['car_type'] = selected_category

        # Start with all bookings
        filtered_bookings = Booking.objects.all()

        available_cars = Cars.objects.exclude(
            Q(booking__pickup_date__lte=return_date_str, booking__return_date__gte=pickup_date_str) |
            Q(booking__pickup_date__gte=pickup_date_str, booking__return_date__lte=return_date_str) |
            Q(booking__pickup_date__lte=pickup_date_str, booking__return_date__gte=return_date_str)
        ).filter(car_type__car_types=selected_category)

        try:
            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
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

        request.session['pickup_date'] = pickup_date_str
        request.session['return_date'] = return_date_str

        car_prices = {}
        for car in available_cars:
            dynamic_price = calculate_dynamic_price(car.discounted_price, total_days)
            car.total_price = total_days * dynamic_price
            total_price = total_days * dynamic_price
            car_prices[car.slug] = {'total_price': total_price, 'total_days': total_days, 'pickup_date': pickup_date_str, 'return_date': return_date_str}
        
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
        pickup_date_str = request.GET.get('pickup_date')
        return_date_str = request.GET.get('return_date')

        if pickup_date_str and return_date_str:
            pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()

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
                car_prices[car_id] = {'total_price': total_price, 'total_days': booking_days, 'pickup_date': pickup_date_str, 'return_date': return_date_str}
            request.session['car_prices'] = car_prices
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    car_prices = request.session.get('car_prices', {})
    car_info = car_prices.get(car_id, {})
    total_days = car_info.get('total_days')
    total_price = car_info.get('total_price')

    reviews = CarReviews.objects.filter(cars=cars).order_by('-created_at')
    rating_choices = CarReviews.RATING_CHOICES

    average_review = CarReviews.objects.filter(cars=cars).aggregate(rating=Avg('rating'))
    ratings_count = CarReviews.objects.filter(cars=cars).values('rating').annotate(count=Count('rating')).order_by('-rating')

    ratings_counts = []
    for i in range(len(ratings_count)):
        ratings_counts.append([ratings_count[i]['rating'], ratings_count[i]['count'], int(ratings_count[i]['count'] * 100 / len(reviews))])

    context = {
        'cars' : cars,
        'total_days': total_days,
        'total_price': total_price,
        'car_detail': Cars.objects.all(),
        'reviews': reviews,
        'rating_choices': rating_choices,
        'average_review': average_review,
        'ratings_count': ratings_counts,
    }

    return render(request, template_name="frontend/car_detail.html", context=context)

@login_required(login_url='/auth/login')
def car_review_by_user(request, slug):
    cars = Cars.objects.get(slug=slug)
    user = request.user
    if request.method == "POST":
        review = request.POST.get('review')
        rating = request.POST.get('rating')
        CarReviews.objects.create(user=user, cars=cars, reviews=review, rating=rating)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/auth/login')
def delete_reviews(request, id):
    try:
        car_review = CarReviews.objects.get(id=id)
        user = request.user
        if car_review.user == user:
            car_review.delete()
            messages.success(request, f"Successfully delete {car_review.reviews} reviews")
    except CarReviews.DoesNotExist:
        messages.warning(request, "review not found")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/auth/login')
def car_like_by_user(request, id):
    cars = CarReviews.objects.get(id=id)
    user = request.user
    if request.method == "POST":
        if cars.likes.filter(id=user.id).exists():
            cars.likes.remove(user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            cars.likes.add(user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/auth/login')
def add_to_cart(request, slug):
    car_obj = Cars.objects.get(slug=slug)
    user_obj = request.user

    old_cart_items = Booking.objects.filter(user=user_obj, car=car_obj).first()

    car_prices = request.session.get('car_prices', {})
    car_info = car_prices.get(car_obj.slug, {})
    total_days = car_info.get('total_days')
    total_price = car_info.get('total_price')
    pickup_date = car_info.get('pickup_date')
    return_date = car_info.get('return_date')

    if old_cart_items:
        if old_cart_items.is_paid:
            messages.success(request, 'Already booked this car')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, 'Already added to cart')
            return redirect('cart')

    cart_item = Booking.objects.create(car=car_obj, user=user_obj)

    if total_days and total_price:
        cart_item.total_days = total_days
        cart_item.total_price = total_price
        cart_item.pickup_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        cart_item.return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
    else:
        cart_item.total_days = 1
        cart_item.total_price = car_obj.discounted_price

    cart_item.save()

    if cart_item:
        messages.success(request, 'Added to cart, make your payment now...')
        return redirect('cart')
    else:
        messages.error(request, 'Failed to add to cart. Please try again.')
        return redirect('cart')

@login_required(login_url='/auth/login')
def cart(request):    
    try:
        cart_obj = Booking.objects.get(is_paid=False, user=request.user)
        cars = cart_obj.car
        average_review = CarReviews.objects.filter(cars=cars).aggregate(rating=Avg('rating'))
    except Booking.DoesNotExist:
        cart_obj = None
        average_review = None

    if request.method == "POST":
        payment_mode = request.POST.get('payment_method')
        transaction_id = request.POST.get('transaction_id')
        transaction_pdf = request.FILES.get('transaction_copy_pdf')

        if payment_mode in ["Cash in Hand", "Transfer to Bank"]:
            cart_obj.payment_mode = payment_mode
            cart_obj.transaction_id = transaction_id if payment_mode == "Transfer to Bank" else None
            cart_obj.transaction_pdf = transaction_pdf if payment_mode == "Transfer to Bank" else None
            cart_obj.booking_id = f"S-{random.randint(10000000, 99999999)}"
            cart_obj.is_paid = True
            cart_obj.save()

            cars.in_stock = False
            cars.save()

            return_date = cart_obj.return_date + timedelta(hours=6)
            Cars.objects.filter(slug=cars.slug).update(in_stock=False)
            
            user_notification = UserNotification.objects.create(
                user=request.user,
                title = "Payment Confirmation 🎉",
                message = f"Your payment has been successfully processed for {cart_obj.car.brand}, {cart_obj.car.year}.",
            )
            # Create UserNotification for admin
            admin = User.objects.get(is_superuser=True)
            admin_notification = UserNotification.objects.create(
                user=admin,
                title= f"New Payment Received for {cart_obj.car.brand}, {cart_obj.car.year} 🎉",
                message=f"A {cart_obj.payment_mode} payment has been received from {request.user.first_name} {request.user.last_name}. Total Amount is <b>AED {cart_obj.total_price:,}</b> for <i>{cart_obj.total_days} days</i>",
            )
            return redirect('success_payment')

    context = {
        'cart' : cart_obj,
        'average_review': average_review,
    }
    return render(request, template_name="frontend/cart.html", context=context)

def success_payment(request):
    try:
        latest_paid_booking = Booking.objects.filter(is_paid=True, user=request.user).latest('created_at')
    except Booking.DoesNotExist:
        messages.error(request, 'No paid bookings found.')
        return redirect('cart')
    context={'cart_obj' : latest_paid_booking}
    return render(request, template_name="frontend/success_payment.html", context=context)

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
    context={
        'faqs': Faq.objects.all()
    }
    return render(request, template_name="frontend/faqs.html", context=context)

def custom_page(request, slug):
    context = {
        'custompage': CustomPage.objects.get(slug=slug, is_published=True)
    }
    return render(request, template_name="frontend/custom_page.html", context=context)

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

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter the queryset to include only published blog posts
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        stripped_body = striptags(self.object.body)
        total_word_count = len(stripped_body.split())
        total_word_count_per_minutes = math.ceil(total_word_count / 200)
        context.update({
        'popular_posts': BlogsDetail.objects.order_by('-hit_count_generic__hits')[:3],
        'total_time': total_word_count_per_minutes,
        })
        return context