from django.contrib import admin
from .models.cars import CarImages, Cars, CarTypes
from .models.users import Profile
# Register your models here.

@admin.register(CarTypes)
class CarTypesAdmin(admin.ModelAdmin):
    list_display = ['car_types', 'slug']
    prepopulated_fields = {'slug': ('car_types',)}

class CarImagesAdmin(admin.StackedInline):
    model = CarImages

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ['brand', 'year', 'price']
    inlines = [CarImagesAdmin,]
    prepopulated_fields = {'slug': ('brand',)}

admin.site.register(CarImages)

admin.site.register(Profile)