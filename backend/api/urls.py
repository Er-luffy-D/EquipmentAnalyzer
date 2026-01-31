from django.urls import path
from .views import upload_csv,summary,generate_pdf

urlpatterns=[
    path('upload/',upload_csv),
    path('summary/',summary),
    path('report/<int:id>/',generate_pdf),
]