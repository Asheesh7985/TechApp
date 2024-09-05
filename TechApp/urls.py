from django.urls import path
from TechApp import views

urlpatterns = [
    path('',views.HomeView,name='home'),
    path('signup/',views.SignupView,name='signup'),
    path('login/', views.LoginView,name='login'),
    path('logout/',views.LogoutView,name='logout'),
    path('dashboard/',views.DashboardView,name='dashboard'),
    path('contact/',views.ContactView,name='contact'),
    path('add-post/',views.AddPostView,name='addpost'),
    path('update-post/<str:slug>/',views.UpdatePostView,name='updatepost'),
    path('delete-post/<str:slug>/',views.DeletePostView,name='deletepost'),
    path('forget-password/',views.ForgetPasswordView,name='forgetpassword'),
    path('enter-otp/<str:email>/',views.EnterOtpView,name='enterotp'),
    path('reset-password/<str:email>/',views.ResetPasswordView,name='resetpassword'),
    path('category/',views.CategoryView,name='category'),
    path('add-category/',views.AddCategoryView,name='addcategory'),
    path('edit-category/<int:id>/',views.EditCategoryView,name='editcategory'),
    path('delete-category/<int:id>/',views.DeleteCategoryView,name='deletecategory'),
    path('change-password/',views.ChangePasswordView,name='changepassword'),
    path('user-profile/',views.UserProfileView,name='userprofile'),
    path('edit-profile/<int:id>/', views.UserEditProfileView,name='editprofile'),
    path('delete-profile/',views.UserDeleteProfileView,name='deleteprofile'),
    path('single-post/<str:slug>/',views.SinglePostView,name="singlepost"),
    path('postComment/', views.postCommentView,name='postComment'),
]
