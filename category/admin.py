from django.contrib import admin
from .models import CategoryModel
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Corrected the reference to 'brand'
    list_display = ['name', 'slug']  # Displaying 'brand' and 'slug'

admin.site.register(CategoryModel, CategoryAdmin)