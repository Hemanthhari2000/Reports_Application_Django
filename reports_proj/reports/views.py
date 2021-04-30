from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.dateparse import parse_date


from .utils import get_report_image

from .models import Report
from profiles.models import Profile
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer

from xhtml2pdf import pisa
import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/detail.html'

class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'

@login_required
def csv_upload_view(request):
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:
                    if len(row) > 0:
                        transaction_id = row[0]
                        product = row[1]
                        quantity = int(row[2])
                        customer= row[3]
                        date = parse_date(row[4])
                        
                        try:
                            product_obj = Product.objects.get(name__iexact= product)
                        except Product.DoesNotExist:
                            product_obj = None
                        
                        # print(product_obj)

                        if product_obj is not None:
                            customer_obj, _ = Customer.objects.get_or_create(name=customer)
                            salesman_obj = Profile.objects.get(user= request.user)
                            position_obj = Position.objects.create(product=product_obj, quantity=quantity, created=date)
                            
                            sale_obj, _ = Sale.objects.get_or_create(transaction_id=transaction_id, customer=customer_obj, salesman=salesman_obj, created=date)
                            sale_obj.positions.add(position_obj)
                            sale_obj.save()
                return JsonResponse({'exists': False})
        else:
            print('already created')
            return JsonResponse({'exists': True})

    return HttpResponse()



@login_required
def create_report_view(request):
    if request.is_ajax():
        name = request.POST.get('name')
        remarks = request.POST.get('remarks')
        image = request.POST.get('image')

        img = get_report_image(image)
        # print(img)
        author = Profile.objects.get(user = request.user)

        Report.objects.create(name = name, remarks=remarks, image=img, author=author)
        
        return JsonResponse({'msg':'send'})
    return JsonResponse({'msg': 'error'})



@login_required
def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = Report.objects.get(id = pk)
    context = {'object': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response