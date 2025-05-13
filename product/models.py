from django.db import models
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    category = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)
    
    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.category.lower().replace(' ', '-')
        super(Category, self).save(*args, **kwargs)

class SubCategory(models.Model):
    subcategory = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.subcategory
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.subcategory.lower().replace(' ', '-')
        super(SubCategory, self).save(*args, **kwargs)

class Sub_SubCategory(models.Model):
    sub_subcategory = models.CharField(max_length=20)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_subcategories')
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.sub_subcategory
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.sub_subcategory.lower().replace(' ', '-')
        super(Sub_SubCategory, self).save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='product_subcategory')
    sub_subcategory = models.ForeignKey(Sub_SubCategory, on_delete=models.CASCADE, related_name='product_sub_subcategory')
    stock = models.PositiveIntegerField()
    size = models.IntegerField()
    visibility = models.BooleanField(default=True)
    warranty = models.PositiveIntegerField()
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
        super(Product, self).save(*args, **kwargs)

def get_product_image_path(instance, filename):
    # Generate a unique filename using the product's slug and the original filename
    return f'products/{instance.product.slug}/{filename}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=get_product_image_path, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    
    def __str__(self):
        return f"Image for {self.product.name}"

    def image_tag(self):
        if self.image:
            return f'<img src="{self.image.url}" width="50" height="50" />'
        return ''
    
class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_specifications')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value} for {self.product.name}"