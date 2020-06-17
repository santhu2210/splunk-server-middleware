from django.conf.urls import url
from clientapp import views as app_view
# from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', app_view.Home_view, name='home'),
    url(r'^raise-request/$', app_view.MakeRequest, name='makerequest'),

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/icons/favicon.ico')),

]
