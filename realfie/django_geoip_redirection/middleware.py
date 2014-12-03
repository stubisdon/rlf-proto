# -*- coding: utf-8 -*-
import pygeoip
from django.conf import settings
from django.http import HttpResponseRedirect


def get_country_request(ip_address):
    """
    Looks up the database to find out country of the incoming IP.
    """
    file_path = settings.PROJECT_ROOT + '/data/GeoIP.dat.dat'
    geo_object = pygeoip.GeoIP(file_path)
    country = geo_object.country_name_by_addr(ip_address)
    return country


class LocationMiddleWare(object):
    """
    Middleware to redirect user as per country returned by get_country_request
    """
    CIS_COUNTRIES = [
        "Russian Federation",
        "Ukraine",
        "Belarus",
        "Moldova, Republic of",
        "Armenia",
        "Azerbaijan",
        "Kazakhstan",
        "Kyrgyzstan",
        "Tajikistan",
        "Turkmenistan",
        "Uzbekistan",
    ]

    def process_request(self, request):
        if request.path != '/':
            return None

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_FORWARDED_FOR']
        ip_address = request.META['REMOTE_ADDR']
        country = get_country_request(ip_address)

        if country in self.CIS_COUNTRIES:
            return HttpResponseRedirect('/ru/')
        else:
            return HttpResponseRedirect('/en/')
