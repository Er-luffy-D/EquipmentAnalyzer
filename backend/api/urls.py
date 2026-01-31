from django.urls import path
from .views import signup,upload_csv,summary,generate_pdf

urlpatterns=[
    path('signup/',signup),
    path('upload/',upload_csv),
    path('summary/',summary),
    path('report/<int:id>/',generate_pdf),
]