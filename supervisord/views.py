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
from django.contrib.auth.models import User
import random

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
        source = data['source']
        try:
            udp_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{2,5}")
            source_list = re.findall(udp_pattern, source)
            source = source_list[0]
        except Exception as e:
            agrs["detail"] = "Invalid source input!"
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=203)           
        stream_key = data['stream_key'].strip()
        '''Check if stream name exists
        flag == 0 --> not exists
        flag == 1 --> adreally exists
        '''
        flag = 0
        configFileList = get_conf_files_list()
        for job in configFileList:
            if job == name:
                flag = 1
                break
        #Cut white space
        name = name.replace(" ", "")
        if name.find(EXTENTION) < 0:
            name = name + EXTENTION
        '''get new stream id'''
        stream_id = random.randint(10000000000,99999999999)
        if not flag:
            try:
                stream_id = StreamingHistory().get_new_id(request)
            except Exception as e:
                print e
            name = str(stream_id) + '_' + name
        else:
            stream_id = Streaming(name).get_id()
        '''Save as supervisord config'''
        if stream_type == "Facebook":
            #Facebook(name).save()
            Facebook(name).save(source, stream_key, stream_id, request.user.username, '')
        elif stream_type == "Youtube":
            Youtube(name).save(source, stream_key, stream_id, request.user.username, '')
        '''Add new job to supervisord'''
        if flag:
            '''Write history'''
            try:
                StreamingHistory().write_history(request.user.username, 'edited', stream_id)
            except Exception as e:
                print e
            if not Process(name).get_job_status():
                Process(name).update_job()
                Process(name).stop_job()
            agrs["detail"] = "Successfully edited to stream %s"%(name)
            messages = json.dumps(agrs)
        else:
            '''Write history'''
            try:
                StreamingHistory().write_history(request.user.username, 'started', stream_id)
            except Exception as e:
                print e
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
    my_stream_list = []
    if request.user.is_superuser:
        my_stream_list = configFileList
    else:
        for stream in configFileList:
            if Streaming(stream).get_owner_name() == request.user.username:
                my_stream_list.append(stream)
    args = []
    for job in my_stream_list:
    #job = job.strip( '.ini' )
    #print job
        args.append({'name'             : job if job else None,
                    'state'             : Process(job).get_job_status(),
                    'description'       : Process(job).job_status(),
                    'command'           : File(job).get_command(),
                    'dmodified'         : File(job).get_last_modified(),
                    'source'            : Streaming(job).get_source(),
                    'stream_key'        : Streaming(job).get_streamkey(),
                    'stream_type'       : Streaming(job).get_type(),
                    'owner'             : Streaming(job).get_owner_name()
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
            '''Write history'''
            try:
                stream_id = Streaming(name).get_id()
                StreamingHistory().write_history(request.user.username, 'deleted', stream_id)
            except Exception as e:
                print e
            '''End write history'''
            File(name).delete()
            Process(name).update_job()
            agrs["detail"] = "Successfully deleted to stream %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)
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
                '''Write history'''
                try:
                    stream_id = Streaming(name).get_id()
                    StreamingHistory().write_history(request.user.username, 'start', stream_id)
                except Exception as e:
                    print e
                '''End write history'''
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
                '''Write history'''
                try:
                    stream_id = Streaming(name).get_id()
                    StreamingHistory().write_history(request.user.username, 'stoped', stream_id)
                except Exception as e:
                    print e
                '''End write history'''
                Process(name).stop_job()
                agrs["detail"] = "Successfully stop to stream %s"%(name)
                messages = json.dumps(agrs)
                return HttpResponse(messages, content_type='application/json', status=202)
        '''restart'''
        if action == 'restart':
            '''Write history'''
            try:
                stream_id = Streaming(name).get_id()
                StreamingHistory().write_history(request.user.username, 'restart', stream_id)
            except Exception as e:
                print e
            '''End write history'''
            Process(name).stop_job()
            Process(name).start_job()
            agrs["detail"] = "Successfully restart to stream %s"%(name)
            messages = json.dumps(agrs)
            return HttpResponse(messages, content_type='application/json', status=202)


def history(request):
    print request
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login')
    history_list = History.objects.all().order_by('-date_time')[:200]
    args = {}
    args['history_list'] = history_list
    args['id'] = request.user.id
    args['email'] = request.user.email if request.user.email else request.user.username
    args['is_superuser'] = 'true' if request.user.is_superuser else 'false'
    args['is_staff'] =  'true' if request.user.is_staff else 'false'
    return render_to_response('supervisord/history.html', args)
