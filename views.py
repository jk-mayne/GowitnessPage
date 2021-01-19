from django.shortcuts import render
from django.http import HttpResponse
from armory2.armory_main.models import *
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import register
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
from base64 import b64encode

# from armory2.

def index(request):

    data = {} #holds all of the port data and gowitness flag this is a dictionary of lists
    ips = IPAddress.objects.all()
    good_ips = [] #weeds out port zeros and such
    #ips, total = IPAddress.get_sorted('active', '', false, 1, )
    #using code from get_sorted...
    port_ids = []
    for ip in ips:
        #print(ip.port_set.all())
        for p in ip.port_set.all():
            if p.port_number > 0:
                if ip not in good_ips:
                    good_ips.append(ip)
                #data[p.id] = []
                if p.meta.get('Gowitness'):
                    #print(p.id)
                    data[p.id] = []
                    data[p.id].append('Gowitness')
                    data[p.id].append(p.service_name + '://' + str(ip.ip_address) + ':' + str(p.port_number))
                    for gw in p.meta['Gowitness']:
                        data[p.id].append(get_file_data(gw['screenshot_file']))
                    port_ids.append(p.id)
    '''gowit_data = []
    #{{ port.service_name}}://{{ ip.ip_address }}:{{port.port_number}}
    for x in port_ids:
        #for each port ID we need to get the gowtiness info from the metadata. This is stored in the Port objects. 
        #the html template needs the 
        #now we need to generate an array (or similiar object) of links to the gowtiness files
        port = Port.objects.get(id=x)
        
        for gw in port.meta['Gowitness']:
            #if gw['screenshot_file'].exists(): this would throw an exception I think but I need to do like a try catch or something I think 
            fdata = get_file_data(gw['screenshot_file'])
            gowit_data.append(fdata)'''




    '''for x in good_ips:
        #lookp through good ips and grab the portid to correlate with Port objects. 


    {% for gw in port.meta.Gowitness %}

  {% if gw.screenshot_file|file_exists %}
    <img src="{{ gw.screenshot_file|get_file_data }}" class="w-100">
  {% else %}
    <p>No image file found</p>
  {% endif %}
{% endfor %}'''
    #print(data[port_ids[1]].0)
    return render(request, 'gowitnessPage/index.html', {'data': data, 'port_ids':port_ids}) #, 'gowit_data':gowit_data})

def get_ips(request, pkid):
    obj = get_object_or_404(CIDR, pk=pkid)

    ips = obj.ipaddress_set.all().order_by('ip_address')

    return render(request, 'host_scoping/ips.html', {'ips': ips})

def get_file_data(file_name):
    return "data:image/png;base64," + b64encode(open(file_name, 'rb').read()).decode()

#This alows dictionary lookups within the template
@register.filter
def get_item(dictionary, key):
    #print(dictionary.get(key))
    return dictionary.get(key)

def get_gowitness2(request, port_id):
    port = Port.objects.get(id=port_id)
    print('hello!')
    return render(request, 'gowitnessPage/gowitness.html', {'port':port})