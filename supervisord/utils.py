import json
import os, subprocess, re
from subprocess import call
import time
from setting.settings import *
from setting.DateTime import *
from supervisord.models import *
from django.contrib.auth.models import User

def get_conf_files_list():
    return os.listdir(SUPERVISORD_CONFIG)

###########################################################################################
#                                                                                         #
#------------------------------------------FILE-------------------------------------------#
#                                                                                         #
###########################################################################################

class File:
    def __init__(self, fileName):
        if fileName.find(EXTENTION) >= 0:
            self.fileName = fileName
        else:
            self.fileName = fileName+EXTENTION
        self.supervisord_confFile= SUPERVISORD_CONFIG

    def check_name_already_exists(self):
        name_already_exists_list = get_conf_files_list()
        for name_already_exists in name_already_exists_list:
            if self.fileName == name_already_exists:
                return True
        return False

    def read_file(self):
        f = open(self.supervisord_confFile + self.fileName, 'r')
        lines=f.read()
        f.close()
        return lines

    def get_command(self):
        f = open(self.supervisord_confFile + self.fileName, 'r')
        lines=f.readlines()
        f.close()
        if (len(lines)) > 1:
            return lines[1]
        return 'Invalid configuration file!'

    def get_program_name(self):
        f = open(self.supervisord_confFile + self.fileName, 'r')
        lines=f.readlines()
        f.close()
        if (len(lines)) > 0:
            return lines[0]
        return ''
    def get_description(self):
        resulf = ''
        try:
            f = open(self.supervisord_confFile + self.fileName, 'r')
            lines=f.readlines()
            f.close()
            if (len(lines)) > 0:
                resulf = lines[4]
        except Exception as e:
            print e
        return resulf


    def write_conf_file(self, text):
        f = open(self.supervisord_confFile + self.fileName, 'w')
        f.write(text)
        f.close()
        return 1

    def delete(self):
        cmnd = ['/bin/rm', '-rf', self.supervisord_confFile+self.fileName]
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        return 1

    def get_last_modified(self):
        return time.ctime(os.path.getmtime(self.supervisord_confFile+self.fileName))

###########################################################################################
#                                                                                         #
#----------------------------------------Streaming----------------------------------------#
#                                                                                         #
###########################################################################################
class Streaming:
    def __init__(self, fileName):
        if fileName.find(EXTENTION) > 0:
            self.fileName = fileName
        else:
            self.fileName = fileName+EXTENTION
        self.command=File(self.fileName).get_command()

    def get_source(self):
        ip_multicast = re.search('(?<=udp://)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{2,5}',self.command).group(0)
        return ip_multicast

    def get_destination(self):
        rtmp_link_list = re.search('(?<=-f flv rtmp://)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',self.command)
        if rtmp_link_list:
            return rtmp_link_list.group(0)
        else:
            return None

    def get_streamkey(self):
        destination = self.get_destination()
        streamkey = destination[destination.rfind('/')+1 : len(destination)]
        return streamkey

    def get_type(self):
        destination = self.get_destination()
        if destination.find('facebook') >=0:
            return "Facebook"
        elif destination.find('youtube') >=0:
            return "Youtube"
        return "Unknow"

    def get_id(self):
        stream_id = None
        description = File(self.fileName).get_description()
        if description:
            try:
                stream_id = re.search('(?<=id: )\d+',description)
                stream_id = stream_id.group(0)
            except Exception as e:
                print e
        return stream_id

    def get_owner_name(self):
        owner_name = ''
        description = File(self.fileName).get_description()
        if description:
            try:
                owner_name = re.search('(?<=owner: )\w+',description)
                owner_name = owner_name.group(0)
            except Exception as e:
                print e
        return owner_name



###########################################################################################
#                                                                                         #
#----------------------------------------FACEBOOK-----------------------------------------#
#                                                                                         #
###########################################################################################
'''
'''
class Facebook:
    def __init__(self, fileName):
        if fileName.find(EXTENTION) > 0:
            self.fileName = fileName
        else:
            self.fileName = fileName+EXTENTION

    def get_ip(self):
        command=File(self.fileName).get_command()
        return Streaming(command).get_source()

    def get_streamkey(self):
        command=File(self.fileName).get_command()
        return Streaming(command).get_streamkey()

    def save(self, ip, stream_Key, stream_id, owner_name, description):
        template_config=FACEBOOK_TEMPLATE
        #edit name
        supervisord_config=template_config.replace('[name]', self.fileName)
        #edit ip
        supervisord_config=supervisord_config.replace('[source]',ip)
        #edit stream key
        supervisord_config=supervisord_config.replace('[streamkey]', stream_Key)
        #edit stream id
        supervisord_config=supervisord_config.replace('[streaming_id]', str(stream_id))
        #edit owner_name
        supervisord_config=supervisord_config.replace('[owner_name]', str(owner_name))
        #edit description
        supervisord_config=supervisord_config.replace('[description]', str(description))
        File(self.fileName).write_conf_file(supervisord_config)
        return 1

###########################################################################################
#                                                                                         #
#----------------------------------------YOUTUBE------------------------------------------#
#                                                                                         #
###########################################################################################
class Youtube:
    def __init__(self, fileName):
        if fileName.find(EXTENTION) > 0:
            self.fileName = fileName
        else:
            self.fileName = fileName+EXTENTION

    def get_ip(self):
        command=File(self.fileName).get_command()
        return Streaming(command).get_source()

    def get_streamkey(self):
        command=File(self.fileName).get_command()
        return Streaming(command).get_streamkey()

    def save(self, ip, streamKey, stream_id, owner_name, description):
        template_config=YOUTUBE_TEMPLATE
        #edit name
        supervisord_config=template_config.replace('[name]', self.fileName)
        #edit ip
        supervisord_config=supervisord_config.replace('[source]',ip)
        #edit stream key
        supervisord_config=supervisord_config.replace('[streamkey]', streamKey)
        #edit stream id
        supervisord_config=supervisord_config.replace('[streaming_id]', str(stream_id))
        #edit owner_name
        supervisord_config=supervisord_config.replace('[owner_name]', str(owner_name))
        #edit description
        supervisord_config=supervisord_config.replace('[description]', str(description))
        File(self.fileName).write_conf_file(supervisord_config)
        return 1

###########################################################################################
#                                                                                         #
#------------------------------------------SEVER------------------------------------------#
#                                                                                         #
###########################################################################################

class Server:
    def __init__(self):
        self.supervisord_service = SUPERVIDORD_SERVICES

    #0 is stop
    #1 is running
    def get_service_status(self):
        cmnd = [self.supervisord_service, 'status']
        p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = str(p.communicate())
        if status.find('unix') > 0:
            return 0
        return 1

    def start_service(self):
        cmnd = [self.supervisord_service, 'start']
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        return 1

    def stop_service(self):
        cmnd = [self.supervisord_service, 'stop']
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        return 1

    def restart_service(self):
        cmnd = [self.supervisord_service, 'restart']
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        return 1

###########################################################################################
#                                                                                         #
#----------------------------------------PROCESS------------------------------------------#
#                                                                                         #
###########################################################################################

class Process:
    def __init__(self, jobName):
        if jobName.find(EXTENTION) > 0:
            self.jobName = jobName
        else:
            self.jobName = jobName+EXTENTION
        self.supervisord_control = SUPERVISORD_CONTROL

    def job_status(self):
        cmnd=[self.supervisord_control, 'status', self.jobName]
        p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = str(p.communicate())
        #print status
        #print str(status)
        status = status[status.rfind("     ") +5 : status.rfind(',')-3]
        return status
    #0 is stop
    #1 is running
    #2 is unknow eror
    #3 is server eror
    def get_job_status(self):
        if not Server().get_service_status():
            return 3
        status = self.job_status()
        if status.find('RUNNING') >= 0:
            return 1
        if status.find('STOPPED') >= 0:
            return 0
        return 2

    def update_job(self):
        cmnd = [self.supervisord_control, 'update']
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        return 1

    def start_job(self):
        cmnd = [self.supervisord_control, 'start', self.jobName]
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        return 1

    def stop_job(self):
        cmnd = [self.supervisord_control, 'stop', self.jobName]
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        return 1

    def restart_job(self):
        cmnd = [self.supervisord_control, 'restart', self.jobName]
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        return 1

    def job_status(self):
        cmnd=[self.supervisord_control, 'status', self.jobName]
        p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = str(p.communicate())
        status = status[status.rfind("     ") +3 : status.rfind(',')-3]
        return status


class StreamingHistory:
    def create_message(self, user_name='', action = '', stream_name = ''):
        message = ''
        now_as_human_creadeble = DateTime().get_now_as_human_creadeble()
        message = 'At %s user %s %s stream name %s.'%(now_as_human_creadeble, user_name, action, stream_name)
        return message

    def write_history(self, user_name, action, stream_id):
        stream_obj = Stream.objects.get(pk = stream_id)
        stream_name = stream_obj.name
        msg = self.create_message(user_name, action, stream_name)
        now = DateTime().get_now()
        new_history = History(stream=stream_obj, date_time=now, action=action, messages=msg)
        new_history.save()
        return 1

    def get_new_id(self, request):
        try:
            data = json.loads(request.body)
        except Exception as e:
            return None
        name = data['name'].strip()
        #Cut white space
        name = name.replace(" ", "")
        if name.find(EXTENTION) < 0:
            name = name + EXTENTION
        stream_type = data['stream_type'].strip()
        source = data['source']
        stream_key = data['stream_key'].strip()
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        description = ''
        now = DateTime().get_now()
        new_stream = Stream(name=name, user=user, create_time=now, stream_type=stream_type, source=source, stream_key=stream_key, description=description)
        new_stream.save()
        n = Stream.objects.get(create_time=now)
        return n.id
