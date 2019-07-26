from django.urls import reverse_lazy
from .models import CustomUser
from django.views import generic
from  .forms import CustomUserChangeForm, CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views
from .models import Commodity, PurchasedCommodity,Portfolio
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

from django.utils import timezone

class Register(generic.CreateView):   

    form_class = CustomUserCreationForm
    next_page = reverse_lazy('tradingSite:login')
    template_name = 'tradingSite/register.html'

    def get_success_url(self):
        return self.next_page


class Login(auth_views.LoginView):
    template_name = 'tradingSite/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tradingSite:commodities')





class CommoditiesView(generic.ListView,LoginRequiredMixin):
    context_object_name = 'latest_commodity_prices'
    template_name = 'tradingSite/commodities.html'
    login_url = 'tradingSite/login.html'

    def get_queryset(self):
        return Commodity.objects.filter(Date__gte=date.today()).filter(Date__lte=date.today())


class Portfolio(LoginRequiredMixin, generic.ListView):
    context_object_name = 'portfolio_list'
    template_name = 'tradingSite/userPortfolio'
    login_url = 'tradingSite/login.html'

    def get_queryset(self):
        user  = CustomUser.objects.get(name=self.request.POST['user']) #get the user
        coms_in_portfolio = user.portfolio.purchasedcommodity_set.all() # get all the unsold purchased commodity in user's porfolio
        unique_purchased_com = coms_in_portfolio.distinct('name').all()
        coms_gains = []
        for p in unique_purchased_com:
            p_items = coms_in_portfolio.filter(__name=p.name)
            gains = 0
            for item in p_items:
                gains += item.calculate_gains()
            
            coms_gains.append((p.name, gains))
            
        return coms_gains

        
class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('tradingSite:homepage')
    
    
class HomepageView(generic.TemplateView):
    template_name = 'tradingSite/homepage.html'