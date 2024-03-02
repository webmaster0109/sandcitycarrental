from django.contrib import admin
from .models.cars import CarImages, Cars, CarTypes, Booking
from .models.users import Profile, Country, UserNotification
from .models.car_features import CarFeatures
from .models.newsletter import EmailNewsletters
from .models.blogs import BlogsDetail
# Register your models here.

admin.site.register(UserNotification)
admin.site.register(EmailNewsletters)

@admin.register(BlogsDetail)
class BlogsDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(CarTypes)
class CarTypesAdmin(admin.ModelAdmin):
    list_display = ['car_types', 'slug']
    prepopulated_fields = {'slug': ('car_types',)}

class CarImagesAdmin(admin.StackedInline):
    model = CarImages

class CarFeaturesAdmin(admin.StackedInline):
    model = CarFeatures

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ['brand', 'year']
    inlines = [CarImagesAdmin, CarFeaturesAdmin]
    prepopulated_fields = {'slug': ('brand',)}

admin.site.register(CarImages)

admin.site.register(Profile)
admin.site.register(CarFeatures)
admin.site.register(Country)
admin.site.register(Booking)