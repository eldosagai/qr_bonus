from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

def default_date():
    return timezone.now() + timezone.timedelta(days=7)


class Type_of_user(models.Model):
    name = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name


class Type_of_organization(models.Model):
    name = models.CharField(max_length=400)
    
    def __str__(self):
        return self.name
    
    
class Type_of_product(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name
    
    
class Type_of_status(models.Model):
    name = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name


class Type_of_operation(models.Model):
    name = models.CharField(max_length=400)
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    name = models.CharField(max_length=50, default="")
    surname = models.CharField(max_length=100, default="")
    otp = models.CharField(max_length=6, null=True, blank=True)
    activated = models.BooleanField(default=False)
    type_of_user = models.ForeignKey(Type_of_user, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=400)
    cost = models.IntegerField()
    description = models.TextField()
    type_of_product = models.ForeignKey(Type_of_product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=500)
    is_halal = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    number_of_scores = models.IntegerField(default=0)
    type_of_organization = models.ForeignKey(Type_of_organization, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organization')
    
    def __str__(self):
        return self.name
    
    
    def increment_number_of_scores(self):
        self.number_of_scores += 1
        self.save()

    
    def average_score(self):
        scores = Score.objects.filter(organization=self.name)
        sum_of_scores = 0
        for score in scores:
            sum_of_scores += score.score
        self.score = sum_of_scores/self.number_of_scores
        self.save()


class Product_of_organization(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Delivery(models.Model):
    date = models.DateField(default=default_date())
    amount = models.IntegerField()
    address = models.TextField()
    type_of_status = models.ForeignKey(Type_of_status, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_delivery')


class Products_of_delivery(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    product_of_organization = models.ForeignKey(Product_of_organization, models.CASCADE)


class Score(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_score")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization_score")


class Branch(models.Model):
    address = models.CharField(max_length=500)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='branch')


class Bonuses(models.Model):
    amount = models.PositiveBigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bonus")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization_bonus")

    def increment_bonuses(self, amount):
        self.amount+=amount
        self.save()

    def decrement_bonuses(self, amount):
        if self.amount > 0:
            self.amount-=amount
        self.save()


class History(models.Model):
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_history')
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, related_name='branch_history')
    type_of_operation = models.ForeignKey(Type_of_operation, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user
    
    
class Booking(models.Model):
    number_of_people = models.IntegerField()
    date = models.DateField()
    accepted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_booking')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_booking')


class Booking_comments(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_booking_comment')