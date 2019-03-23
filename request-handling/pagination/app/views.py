import csv
from urllib.parse import urlencode

from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .settings import BUS_STATION_CSV

station_list = []
with open(BUS_STATION_CSV, newline='', encoding='cp1251') as file:
    reader = csv.DictReader(file)
    for row in reader:
        station_list.append({
            'Name': row['Name'],
            'Street': row['Street'],
            'District': row['District']
        })


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    paginator = Paginator(station_list, 10)
    page = request.GET.get('page')

    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
        page = 1
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    prev_page_url = content.has_previous() and ('?'.join([reverse(bus_stations),
                                                          urlencode({'page': content.previous_page_number()})]))
    next_page_url = content.has_next() and ('?'.join([reverse(bus_stations),
                                                      urlencode({'page': content.next_page_number()})]))

    return render_to_response('index.html', context={
        'bus_stations': content.object_list,
        'current_page': page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
