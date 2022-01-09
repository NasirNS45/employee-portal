from django.db import models
from django.urls import reverse
# from django_fields import DefaultStaticImageField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    cell_number = models.IntegerField(default=None, null=True)
  #  profile_picture = DefaultStaticImageField(upload_to='user_images', null=True, blank=True,
   #                                           default_image_path='img/anonymous-user.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.name


class Address(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    zip_code = models.IntegerField()

    def __str__(self):
        return self.address


class ProductCategory(models.Model):
    name = models.CharField(max_length=150, db_index=True, default=None)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, default=None)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products-by-category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='pictures', default=True, null=True)
    specs = models.CharField(max_length=100)
    current_price = models.IntegerField()
    old_price = models.IntegerField()
    discount = models.IntegerField(default=False)
    category = models.ForeignKey(ProductCategory, related_name='products', null=True, blank=True,
                                 on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
#     product_name = models.CharField(max_length=50)
#     product_price = models.IntegerField()
#     product_image = models.ImageField(upload_to='cart_item_images', default='static/img/faq-cover.jpg', null=True,
#                                       blank=True)
#
#     def __str__(self):
#         return self.product_name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=None)


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=30, blank=True, null=True, default=None)
    area_code = models.IntegerField()
    primary_phone = models.IntegerField()
    street_address = models.CharField(max_length=100)
    zip_code = models.IntegerField()


class PaymentInfo(models.Model):
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    stripe_payment_id = models.CharField(max_length=50, blank=True, null=True)
    stripe_payment_status = models.CharField(max_length=20, default=None)
    stripe_paid_amount = models.IntegerField(default=None)

# class TransactionInfo(models.Model):
#     SUCCESS = 'success'
#     PENDING = 'pending'
#     SUSPENDED = 'suspended'
#     PAYMENT_STATUS = (('success', SUCCESS), ('pending', PENDING), ('suspended', SUSPENDED))
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
#     transaction_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default=PENDING)
#     transaction_reference_number = models.IntegerField()
#     bank_authorised_code = models.IntegerField()
#     transaction_date = models.DateTimeField(default=timezone.now())
#     total_amount = models.IntegerField(default=None)
#
#     def __str__(self):
#         return self.transaction_status
