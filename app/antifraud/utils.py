from os.path import exists, isfile, isdir, join
from os import pathsep, linesep
import codecs
import tempfile
from shutil import copy

folder =  tempfile.gettempdir() 


def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT')

def get_client_ip(request):
    ip = None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def record_user(username, country):
    country_records = '%s.txt' % country
    country_records = join(folder, country_records)
    username       = "%s\n" % username
    if not exists(country_records):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(username)
        copy(f.name, country_records)
    f = codecs.open(country_records, 'a')
    f.write(username)
    f.close()

def delete_user(username, country):
    country_records = '%s.txt' % country
    country_records = join(folder, country_records)
    username       = "%s\n" % username
    if not exists(country_records):
        f = tempfile.NamedTemporaryFile(delete=False)
        copy(f.name, country_records)
    else:
        f = codecs.open(country_records, 'r')
        lines = f.readlines() 
        f.close()
        f = codecs.open(country_records, 'w')
        for line in lines:
            if line != username:
                f.write(line)
        f.close()
    

def check_user(username, country):
    country_records = '%s.txt' % country
    country_records = join(folder, country_records)
    username = "%s%s" % (username, linesep)
    if exists(country_records):
        records = codecs.open(country_records).readlines()
        if username in records:
            return True
        else:
            return False
    return False