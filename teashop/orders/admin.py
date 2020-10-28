import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from .models import Orders, OrderItem


"""
Some unbounded actions.
"""

def export_to_csv(modeladmin, request, queryset):
    # get info about model
    opts = modeladmin.model._meta
    # ask browser to work with response as with csv file
    response = HttpResponse(content_type='text/csv')
    # mark, that csv file will be attached
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
        
    # it writes data_rows in response
    writer = csv.writer(response)
    # get all names of fields
    fields = [field for field in opts.get_fields() if not field.many_to_many\
        and not field.one_to_many]
    # write first them in first line 
    writer.writerow([field.verbose_name for field in fields])
    # write data
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                # converting datetime into string (csv consist only of strings)
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
    
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name',
                    'email', 'address', 'postal_code',
                    'city', 'paid', 'created',
                    'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
        