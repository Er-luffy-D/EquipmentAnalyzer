from django.urls import path
from .views import signup,upload_csv,summary,authorise,generate_pdf

urlpatterns=[
    path('signup/',signup),
    path('upload/',upload_csv),
    path('summary/',summary),
    path('loggedIn/',authorise),
    path('report/<int:id>/',generate_pdf),
]