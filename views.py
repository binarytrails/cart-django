# Copyright (C) 2016 Seva Ivanov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import os, random

from django.conf import settings
from django.shortcuts import HttpResponse, render
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache

from kedfilms.settings import MOBILE_HOSTS

from frontend.views import old_browsers

APP = "cart"
MEDIA = settings.MEDIA_URL
STATIC = os.path.join(settings.STATIC_ROOT, APP)
ERRORS = os.path.join(APP, "errors")

def is_mobile(request):
    # .mobile -> minidetector.Middleware
    return request.mobile or request.get_host() in MOBILE_HOSTS

def template_prefix(request):
    return ("-mobile.html" if is_mobile(request) else ".html")

def template_exists(template):
    return os.path.exists(os.path.join(APP, "templates", template))

def merge_context(request, new_context=None):
    base_context = {
        "APP": APP,
        "PLATFORM": "mobile" if is_mobile(request) else "desktop",
        "PARENT": os.path.join(APP, "base.html")
    }
    if new_context: return dict(base_context.items() + new_context.items())
    return base_context

# views

@never_cache
@old_browsers
def project(request, folder, html_file):
    context = None
    template = os.path.join(APP, folder, html_file + template_prefix(request))
    if template_exists(template) == False: return error404(request)

    if html_file == "moodboard":
        context = {"files": moodboard_data(
            os.path.join(STATIC, "moodboard/images/data"))}

    return render(request, template, merge_context(request, context))

# projects related

def moodboard_data(folder):
    unordered_files = []
    video_formats = ["webm"]
    image_formats = ["jpg", "png", "gif", "svg"]
    supported_formats = image_formats + video_formats

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        if os.path.isfile(filepath):

            extension = os.path.splitext(filename)[1][1:].lower()
            if extension not in supported_formats: continue

            unordered_files.append({
                # wrap with 'time.ctime()' to make readable
                "mtime": os.path.getmtime(filepath),
                "is_video": extension in video_formats,
                "top_shift": random.randint(1, 10),
                "filename": filename
            })

    ordered_files = sorted(unordered_files,
        key=lambda item: item["mtime"], reverse=True)

    return ordered_files

# errors

def error404(request):
    template = os.path.join(ERRORS, "404.html")
    if template_exists(template) == False: return error404(request)

    return render(request, template, merge_context(request, {
        "PARENT": os.path.join(APP, "base.html"),
        "APP": APP,
        "header": "404 NOT FOUND",
        "href": "/cart/home/welcome/",
        "image_source": "images/errors/404.gif"
    }))
