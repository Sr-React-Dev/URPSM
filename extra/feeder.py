#-------------------------------------------------------------------------------
# Name:        URPSM Phones Data Crawler & Scraper
# Purpose:     crawl and scrap data from some websites
#
# Author:      Mohamed Hamza El Bakouchi
#
# Created:     20/12/2016
# Copyright:   (c) URPSM 2016
# Licence:     <hamza.bakouchi(at)gmail.com>
#-------------------------------------------------------------------------------


import requests
import codecs
import urllib
import urllib2
from bs4 import BeautifulSoup as bs
import json
import os,sys, linecache
from urlparse import urlparse
from hashlib import md5
import cfscrape
import argparse

FOLDER_NAME= "gsmarena"
from datetime import datetime





source = "http://www.gsmarena.com/makers.php3"
victim = "http://www.gsmarena.com"



parser=argparse.ArgumentParser(
    description='''URPSM phones crawler & scraper. ''',
    epilog="""All's well that ends well.""")

parser.add_argument('--folder', type=str, default=FOLDER_NAME, help='Work folder')
parser.add_argument('--bfolder', type=str, help='Brand folder')
parser.add_argument('--bfile', type=str, default="brands-urls.txt", help='Where to write brands urls')
parser.add_argument('--mfile', type=str, default="models-urls.txt", help='Where to write models urls')
parser.add_argument('--pagination', type=str, default="http://www.gsmarena.com/%s%s.php", help='pagination schema')
parser.add_argument('--struct', type=str, default="samsung-phones-f-9-0-p", help='fixed part of the pagination')
parser.add_argument('--start', type=int, default=0, help='start pagination')
parser.add_argument('--end', type=int, default=10, help='end pagination')
parser.add_argument('--type',  type=str, help='What to crawl?? brands or models enter one of them as type')
##parser.add_argument('--scrap', type=, default=False, help='The victim to crawl')
parser.add_argument('--source', type=str, default=source, help='The victim url to crawl')
parser.add_argument('--victim', type=str, default=victim, help='The victim website')

crawler_parser = parser.add_mutually_exclusive_group(required=False)
crawler_parser.add_argument('--crawl', dest='crawl', action='store_true')
parser.set_defaults(crawl=False)

scrap_parser = parser.add_mutually_exclusive_group(required=False)
scrap_parser.add_argument('--scrap', dest='scrap', action='store_true')
scrap_parser.add_argument('--no-scrap', dest='scrap', action='store_false')
parser.set_defaults(scrap=False)



args=parser.parse_args()

print args.scrap, "scrapping !!"

try:
    os.makedirs(args.folder, 0755)
except:pass

folder = os.path.join(os.path.dirname(__file__),args.folder)

if 'Student' in folder:
    TEST = True
##    HOME_FILENAME = "C:\\Users\\Student\\Documents\\%s\\%s"
else:
    TEST = False
##    HOME_FILENAME = "/home/ubuntu/%s/%s"

def PrintException(prnt=True):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    # if 'bootcamp-master' in PROJECT_DIR:
    msg = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    if prnt:
        print msg
    return msg

headers={"X-CSRF-ASYNC": "1"}

header = {
            'User-Agent': 'Mozilla/5.0',
            # 'Content-Type': 'multipart/form-data',
            # 'From': 'hamza.bakouchi@gmail.com'  # This is another valid field
        }
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'utf-8',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def scrap_url(url, tech=1, raw=True):
    if tech == 1:
        try:
            request = urllib2.Request(url, headers=hdr)
            response = urllib2.urlopen(request)
            if not raw:
                soup = bs(response.read().decode('utf-8','ignore'))
                return soup
            else:
                return response
        except:
            return PrintException()
    elif tech == 2:
        try:
            response = requests.get(url, headers=headers).text
            if not raw:
                soup = bs(response)
                return soup
            else:
                return response
        except:
            return PrintException()
    elif tech == 4:
        try:
            response = requests.get(url, headers=headers).text
            if not raw:
                return bs(urllib2.urlopen(url), "html.parser")
            else:
                return response
        except:
            return PrintException()

    elif tech == 3:
        try:
            scraper = cfscrape.create_scraper()
            return scraper.get(url).content
        except:
            return PrintException()

def get_anchors(source_data):
    links = source_data.findAll('a')
    return links


def clean_links(anchors, list_file, type='brand'):
    _file   = codecs.open(list_file, 'a')
    for anchor in anchors:
        if type == 'brand':
            try:
                devices     = anchor.find('span').text
                brand       = anchor.text
                brand       = brand.replace(devices, '')
                devices     = devices.replace(' devices' , '')
                brand_url   = anchor['href']
    ##            print brand, devices, brand_url
                _ = "%s,%s/%s,%s\n" % (brand,args.victim, brand_url , devices)
                _file.write(_)

            except:
                PrintException()
        elif type=='model':
            try:
                model     = anchor.find('span').text
                model_url   = anchor['href']
                _ = "%s,%s/%s\n" % (model, args.victim, model_url)
                _file.write(_)
            except:
                PrintException()

    _file.close()


def get_content(soup, tag, selector_name, selector, raw=False):
    """
        Get the useful content by its css selector or whatever
    """
    content = soup.find(tag,{selector_name:selector})
    if raw:
        return str(content)
    return content



def brands():
    data = scrap_url(args.source, 2 , False)
    content = get_content(data,'div', 'class', 'st-text')
    anchors = get_anchors( content )
    brands_file = os.path.join(folder, args.bfile)
    clean_links( anchors, brands_file )

def make_brand_folder(name):
    name = name.replace(' ','_')
    brand_folder = os.path.join(folder,   name)
    try:
        os.makedirs(brand_folder, 0755)
    except:pass
    return brand_folder

import logging
logger = logging.getLogger('urpsm')
hdlr = logging.FileHandler('urpsm.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)


def create_model_folder(brand_folder, model_name):
    model_name = model_name.replace(' ', '_')
    folder_name = os.path.join(brand_folder, model_name)
    try:
        os.mkdir(folder_name, 0775)
    except:
        pass
    return folder_name
def process_models(brand_folder, urls_file):
    try:
        _file = codecs.open(urls_file, 'rb')
        lines = _file.readlines()
        for line in lines:
            model, model_url = line.split(',')
            model_url = model_url.rstrip('\n')
            print model_url
            model_data = scrap_url(model_url, 4, False)
##            model_data = processPhone(model_url)
##            print model_data
##            exit
##            model_info = get_content(model_data, 'div', 'class', 'article-info', True)
##            model_specs = get_content(model_data, 'div', 'id','specs-list', True)

##            break
##            model_folder = create_model_folder(brand_folder, model)
            model_file = model.replace(' ','_').replace('/', '')
            model_file = "%s-2.txt" % model_file
            model_file   = os.path.join(brand_folder, model_file)
            __file       = codecs.open(model_file, 'a')
            model_data   = str(model_data)
##            __file.write(model_info)
##            __file.write(model_specs)
            __file.write(model_data)
            __file.close()



    except:
        error = "file %s does not exists" % urls_file
        logger.error(error)
##        logger.info('While this is just chatty')



def scrap():

    message  = "We are going to scrap from files %s in folder %s.\nAre you sure?[Y/n]:" % (args.mfile, args.folder)
    decision = raw_input(message)
    if decision == 'Y':
        subfolders = os.listdir(folder)
        for subfolder in subfolders:
            brand_folder     = os.path.join(folder, subfolder)
            models_urls_file = os.path.join( brand_folder, args.mfile)
            process_models(brand_folder, models_urls_file)




        pass
    else:
        print 'Ok as you like. Thank you.'

# cmd = "python feeder-paginator.py --crawl --bfolder %s --folder phonesdata/gsmarena2 --struct %s  --mfile missed-models-1.txt --start 2 --end 13 \n"
cmd = "python feeder-paginator.py --scrap --folder F:\gsmarena-full\gsmarena2  --mfile missed-models-1.txt  \n"


def main():
    structs_file = os.path.join(folder, 'structs.txt')
    structs = codecs.open(structs_file, 'w')

    models_file_path = os.path.join(folder, 'brand20161221.txt')
    models_urls      = codecs.open(models_file_path,'rb').readlines()
    for model_url in models_urls:

        parts = model_url.split('/')
        brand = parts[0].split(',')[0].replace(' ','_')
        php_file = parts[-1].split(',')[0].replace('phones-', 'phones-f-')
        struct   = php_file.split('.')[0] + '-0-p'
        # command =  cmd % (brand, struct)
        command =  cmd 
        structs.write(command)
        # print struct

    # structs_file.close()

def get_makers(url):
    brand_models_data = scrap_url(url, 2, False)
    brand_models_content = get_content(brand_models_data, 'div','class', 'makers')
    anchors = get_anchors(brand_models_content)
    return anchors




def models():
    if not args.scrap:
        brands_file =os.path.join(folder, args.bfile)
        _file       = codecs.open(brands_file, 'rb')
        brands_lines      = _file.readlines()
        for line in brands_lines:
            name, url, _ = line.split(',')
            brand_folder = make_brand_folder(name)
            anchors = get_makers(url)
            links  = clean_links(anchors, args.mfile, 'model')




def crawler():
    message  = "We are going to crawl from page %s to page %s.\nAre you sure?[Y/n]:" % (args.start, args.end)
    decision = raw_input(message)
    if decision == 'Y':
        try:
            for i in range(args.start, args.end + 1):
                url = args.pagination % (args.struct, i)
                anchors = get_makers(url)
                missed_urls_filename  =  os.path.join(folder,args.bfolder, args.mfile)

                clean_links(anchors, missed_urls_filename, 'model')
                
                print url
        except:
            PrintException()
    else:
        print "Ok, as you like"

def main2():

    if args.pagination and args.crawl:
        crawler()
    if not args.scrap:
        if args.type == 'brands':
            brands()
        elif args.type == 'models':
            models()
        else:
            print """What do you want to do with GSMARENA?
          Exemple:
            Crawl brands:
             urpsm-feeder.py --type brands --bfile my_brands_file.txt --source http://somewebsiteyou.know
            Crawl models:
             urpsm-feeder.py --type models --bfile my_brands_file.txt --mfile my_models_file.txt
            Scrap models
             urpsm-feeder.py --type models --mfile my_models_file.txt --scrap
          That's all!!
        """
    else:
        scrap()


if __name__ == '__main__':
    print "Here we go!!"
    main()
    print "Let's hope everything is now well done."
