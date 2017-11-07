# coding: utf8
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse

import json
from accounts.user_info import *
from utils import *
from setting.settings import EXTENTION

@require_http_methods(['GET', 'POST'])
@csrf_exempt
def supervisord(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    if request.method=='POST':
        agrs={}
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "No data input found!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        name = data['name'].strip()
        stream_type = data['stream_type'].strip()
        source = data['source'].strip()
        stream_key = data['stream_key'].strip()
        #Cut white space
        name = name.replace(" ", "")
        if not name.find(EXTENTION):
            name = name + EXTENTION
        '''Save as supervisord config'''
        if stream_type == "Facebook":
            Facebook(name).save(source, stream_key)
        elif stream_type == "Youtube":
            Youtube(name).save(source, stream_key)
        '''Add new job to supervisord'''
        Process(name).update_job()
        Process(name).stop_job()
        agrs["detail"] = "Successfully added to stream %s"%(name)
        messages = json.dumps(agrs)
        return HttpResponse(messages, content_type='application/json', status=202)
    user = user_info(request)
    return render_to_response('supervisord/supervisord.html', user)

@require_http_methods(['GET'])
def supervisord_json(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    configFileList = get_conf_files_list()
    args = []
    for job in configFileList:
    #job = job.strip( '.ini' )
    #print job
        args.append({'name'             : job if job else None,
                    'state'             : Process(job).get_job_status(),
                    'description'       : Process(job).job_status(),
                    'command'           : File(job).get_command(),
                    'dmodified'         : File(job).get_last_modified(),
                    'source'            : Streaming(job).get_source(),
                    'stream_key'        : Streaming(job).get_streamkey(),
                    'stream_type'       : Streaming(job).get_type()
                    })
    json_data = json.dumps({"process": args})
    return HttpResponse(json_data, content_type='application/json', status=200)

@require_http_methods(['PUT', 'DELETE', 'OPTIONS'])
@csrf_exempt
def action(request, name):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    agrs = {}
    if request.method == 'DELETE':
        if Process(name).get_job_status() == 1:
            agrs["detail"] = "Streaming %s is RUNNING, you need stop process!"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        else:
            File(name).delete()
            Process(name).update_job()
            agrs["detail"] = "Successfully deleted to stream %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
    if request.method == 'PUT':
        print 'edit'
    if request.method == 'OPTIONS':
        try:
            data = json.loads(request.body)
        except Exception as e:
            agrs["detail"] = "Error! Unknow"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)
        action = data['action']
        '''start'''
        if action == 'start':
            if Process(name).get_job_status():
                agrs["detail"] = "Streaming %s is RUNNING!"%(name)
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=203)
            else:
                Process(name).start_job()
                agrs["detail"] = "Successfully start to stream %s"%(name)
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=202)
        '''stop'''
        if action == 'stop':
            if not Process(name).get_job_status():
                agrs["detail"] = "Streaming %s is STOP!"%(name)
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=203)
            else:
                Process(name).stop_job()
                agrs["detail"] = "Successfully stop to stream %s"%(name)
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=202)
        '''restart'''
        if action == 'restart':
            Process(name).stop_job()
            Process(name).start_job()
            agrs["detail"] = "Successfully restart to stream %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)