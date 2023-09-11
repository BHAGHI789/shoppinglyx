from re import U
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top wear'),
    ('BW','Bottom wear'),
)

class Product(models.Model):
    title=models.CharField(max_length=150)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=150)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=10)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


STATE_CHOICES = (
    ('Andaman & nikobar Island', 'Andaman & nikobar Island'),
    ('Andra pradesh', 'Andra pradhesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', ''),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra & Nagar  and Daman & Diu', 'Dadra & Nagar  and Daman & Diu'),
    ('Delhi', 'Delhi'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),
    ('Ladakh', 'Ladakh'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    locality = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Deliverd','Deliverd'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES,default='Pending')
    
    def total_cost(self):
        return self.quantity * self.product.discounted_price
