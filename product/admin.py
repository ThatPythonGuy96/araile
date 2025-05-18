from django.contrib import admin
from .models import *

class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ['image']

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1
    fields = ['key', 'value']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')
    prepopulated_fields = {'slug': ('category',)}
    search_fields = ('category',)
    list_filter = ('category',)
    ordering = ('category',)
    list_per_page = 10
    list_editable = ('slug',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory', 'category', 'slug')
    prepopulated_fields = {'slug': ('subcategory',)}
    search_fields = ('subcategory',)
    list_filter = ('subcategory',)
    ordering = ('subcategory',)
    list_per_page = 10
    list_editable = ('slug',)

@admin.register(Sub_SubCategory)
class Sub_SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_subcategory', 'subcategory', 'slug')
    prepopulated_fields = {'slug': ('sub_subcategory',)}
    search_fields = ('sub_subcategory',)
    list_filter = ('sub_subcategory',)
    ordering = ('sub_subcategory',)
    list_per_page = 10
    list_editable = ('slug',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'brand', 'color', 'sku', 'category', 'subcategory', 'sub_subcategory', 'stock', 'size', 'visibility', 'warranty', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('category', 'subcategory', 'sub_subcategory')
    ordering = ('name',)
    list_per_page = 10
    list_editable = ('description', 'price', 'brand', 'color', 'sku', 'stock', 'size', 'visibility')
    inlines = [ImageInline, SpecificationInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'image_tag')
    search_fields = ('product__name',)
    list_filter = ('product',)
    ordering = ('product',)
    list_per_page = 10

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'key')
    search_fields = ('product__name',)
    list_filter = ('product',)
    ordering = ('product',)
    list_per_page = 10