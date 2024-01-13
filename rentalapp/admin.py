from django.contrib import admin
from .models.cars import CarImages, Cars, CarTypes, CarPrice
from .models.users import Profile
from .models.car_features import CarFeatures
# Register your models here.

@admin.register(CarTypes)
class CarTypesAdmin(admin.ModelAdmin):
    list_display = ['car_types', 'slug']
    prepopulated_fields = {'slug': ('car_types',)}

class CarImagesAdmin(admin.StackedInline):
    model = CarImages

class CarFeaturesAdmin(admin.StackedInline):
    model = CarFeatures

class CarPriceAdmin(admin.StackedInline):
    model = CarPrice

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ['brand', 'year']
    inlines = [CarPriceAdmin, CarImagesAdmin, CarFeaturesAdmin]
    prepopulated_fields = {'slug': ('brand',)}

admin.site.register(CarImages)

admin.site.register(Profile)
admin.site.register(CarFeatures)