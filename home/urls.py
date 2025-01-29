from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('login', views.loginPage),
    path('contact', views.contactPage),
    path('rental', views.rentalPage),
    path('signup', views.signup),
    path('loginuser', views.loginUser),
    path('logout', views.logoutUser),
    path('booking', views.booking),
    path('save-booking/', views.save_booking, name='save_booking'),
    path('book-pc/', views.book_pc, name='book_pc'),
    path('search-user/', views.searchUser, name='searchUser'),
    
    path('search/', views.search_user, name='search_user'),
    path('users-by-date/', views.get_users_by_date, name='get_users_by_date'),
]
