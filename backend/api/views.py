from django.shortcuts import render
import os
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,parser_classes
from .models import Dataset
from .serializers import DatasetSerializer
from .utils import analyze_csv
from reportlab.pdfgen import canvas
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    file=request.FILES['file']
    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    upload_dir = 'media/uploads'
    os.makedirs(upload_dir, exist_ok=True) 
    file_path = os.path.join(upload_dir, file.name)
    with open(file_path,'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    
    summary = analyze_csv(file_path)

    dataset = Dataset.objects.create(
        file=file,
        **summary
    )

    # delete older datasets>5 
    qs= Dataset.objects.all()
    if qs.count() >5:
        for obj in qs[5:]:
            obj.delete()

    return Response(DatasetSerializer(dataset).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def summary(request):
    return Response(DatasetSerializer(Dataset.objects.all(),many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_pdf(request,id):
    dataset=Dataset.objects.get(id=id)
    upload_dir = 'media/reports'
    os.makedirs(upload_dir, exist_ok=True) 
    pdf_path = f"media/reports/report_{id}.pdf"

    c=canvas.Canvas(pdf_path)
    c.drawString(100,800,f"Dataset ID: {id}")
    c.drawString(100,780,f"Total Count: {dataset.total_count}")
    c.drawString(100,760,f"Avg Flowrate: {dataset.avg_flowrate}")
    c.drawString(100,740,f"Avg Pressure: {dataset.avg_pressure}")
    c.drawString(100,720,f"Avg Temperature: {dataset.avg_temperature}")
    c.save()

    return FileResponse( open(pdf_path, 'rb'),
        content_type='application/pdf',
        as_attachment=True,
        filename=f"report_{id}.pdf")
