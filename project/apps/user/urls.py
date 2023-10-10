from .views import SignupView, JWTLoginView, PasswordChangeView, PasswordResetVerifyView, PasswordResetSendView, PasswordResetConfirmView, PromoteUserPermissionView, UserPhoneViewSet, is_logged_in, UserListViewSet, UserProfileViewSet, UserUpdateView, ShipmentViewSet, RegionViewSet, ContactCreateView, ActivateUserView, UserEmailVerifyView, UserEmailChangeView, OtpUsernameView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter


utils_router = DefaultRouter()

utils_router.register('user/promote', PromoteUserPermissionView)
utils_router.register('phone', UserPhoneViewSet)
utils_router.register('list', UserListViewSet)
utils_router.register('profile', UserProfileViewSet)

utils = [
    path('username/otp/', OtpUsernameView.as_view()),
    path('update/email/', UserEmailChangeView.as_view()),
    path('update/', UserUpdateView.as_view()),
    path('email/verify/', UserEmailVerifyView.as_view())
] + utils_router.urls


password_urls = [
    path('reset/send/', PasswordResetSendView.as_view()),
    path('reset/verify/', PasswordResetVerifyView.as_view()),
    path('reset/change/', PasswordResetConfirmView.as_view()),
    path('change/', PasswordChangeView.as_view()),
]

auth_urls = [
    path('activate/', ActivateUserView.as_view()),
    path('is/logged/', is_logged_in),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('signup/', SignupView.as_view()),
    path('login/', JWTLoginView.as_view()),
    path('password/', include(password_urls))
]

router = DefaultRouter()

router.register('shipment', ShipmentViewSet)
router.register('regions', RegionViewSet)

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('utils/', include(utils)),
    path('utils/contact/', ContactCreateView.as_view()),    
] + router.urls