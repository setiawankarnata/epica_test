from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('logout/', views.LogoutPageView.as_view(), name='logout'),
    path('password_change/', views.PasswordChangePageView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDonePageView.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordResetPageView.as_view(), name='password_reset'),
    path('password_reset_done/', views.PasswordResetDonePageView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmPageView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompletePageView.as_view(), name='password_reset_complete'),
    path('signup/', views.SignUpPageView.as_view(), name="signup"),
    path('profile/', views.profile_page_view, name='profile'),
    # path('profile/update/<int:pk>/', views.ProfileUpdatePageView.as_view(), name='profile_update'),
    path('profile/update/<int:pk>/', views.profile_update_page_view, name='profile_update'),
    path('profile/create/<int:id>', views.ProfileCreatePageView.as_view(), name='profile_create'),
]
