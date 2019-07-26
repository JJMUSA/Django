from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class Commodity(models.Model):
    name = models.CharField(max_length=20)
    id = models.AutoField(auto_created=True, max_length=20, primary_key=True)
    current_price = models.FloatField(default=0)
    previous_price = models.FloatField(default=0)
    change = models.FloatField(default=0)
    Date = models.DateTimeField(default=timezone.now)

class Portfolio(models.Model):
    portfolioUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE)



class PurchasedCommodity(models.Model):
    purchase_date = models.DateTimeField()
    commodity_purchased = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    portfolio_purchased_in = models.ForeignKey(Portfolio,on_delete=models.CASCADE)
    sold = models.BooleanField(default=False)
    sold_date = models.DateTimeField()


    @property
    def calculate_gains(self):
        trading_price =  self.get_purchasing_price()
        return trading_price - self.purchase_price

    @property
    def get_sold(self):
        return self.sold

    @property
    def get_sold_date(self):
        return self.sold_date

    @property
    def get_com_name(self):
        return self.commodity_purchased.name

    @property
    def get_purchasing_price(self):
        return self.commodity_purchased.current_price

    @property
    def get_purchasing_date(self):
        return self.purchase_date

class Wallet(models.Model):
    user  = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    wallet_amount = models.FloatField()
    
    @property
    def withdraw(self, amount):
        if(self.wallet_amount>=amount):
            self.wallet_amount -=amount
    
    def deposit(self,amount):
        if(amount>0): 
            self.wallet_amount +=amount
    



