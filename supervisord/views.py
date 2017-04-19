# coding: utf8
import json
from django.db.models import Q
from django.db import transaction, connection,IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.cache import cache

from accounts.user_info import *
import time
import os, sys, subprocess, shlex, re, fnmatch,signal
import os.path
from subprocess import call

@csrf_exempt
def supervisord(request):
        if not request.user.is_authenticated():
                return HttpResponseRedirect('/accounts/login')
        user = user_info(request)
        return render_to_response('supervisord/supervisord.html',user)
