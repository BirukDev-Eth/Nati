from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),  # ← this makes /api/auth/register/ valid
    path('api/experience/', include('apps.experience.urls')),
    path('api/education/', include('apps.education.urls')),
    path('api/personal_info/', include('apps.personal_info.urls')), 
    path('api/resume/', include('apps.resume.urls')),
    path('api/project/', include('apps.project.urls')),
    path('api/customer/', include('apps.customer.urls')),
    path("api/contacts/", include("apps.customeremail.urls")),
    path("api/contact-reply/", include("apps.contactreplay.urls")),
    path("api/testimonies/", include("apps.testimonies.urls")),
    path("api/password-reset/", include("apps.tokenWithForgetPassword.urls")),

]
