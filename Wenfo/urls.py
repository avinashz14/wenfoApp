from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Wenfo_app.views import EditProfileView, DashboardView, SigninView, SignupView,AddNews,NotificationView,RecommendationView,logout_view, AllNewsView, password_reset_view
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView, PasswordResetForm, PasswordResetCompleteView


urlpatterns = [
    path('admin/', admin.site.urls,name="admin"),
    path('accounts/signup/', SignupView.as_view(),name="signup"),
    path('accounts/login/', SigninView.as_view(),name="signin"),
    path('profile/', DashboardView.as_view(),name="dashboard"),
    path('', AllNewsView.as_view(),name="worldnews"),
    path('accounts/edit-profile/', EditProfileView.as_view(),name="edit_profile"),
    path('accounts/addnews/', AddNews.as_view(),name="addnews"),
    path('accounts/notification/', NotificationView.as_view(),name="notification"),
    path('accounts/recommendation/', RecommendationView.as_view(),name="recommendation"),
    path('accounts/logout/',logout_view,name="logout_view"),
    
    path('accounts/forgotPassword/', PasswordResetView.as_view(),name='password_reset_view'),
    path('accounts/forgotPassword/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/forgotPassword/reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/forgotPassword/reset-done/',PasswordResetCompleteView.as_view(), name='password_reset_complete'),
      
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 