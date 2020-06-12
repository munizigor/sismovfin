from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='main/')),

	# path('success/', views.success, name='success'),
	path('submit_movfin/', views.submit_movfin, name='submit_movfin'),
    path('download_sample/', views.download_sample, name='download_sample'),

]