#-------------------------------------------------------------------------------
# Name:        URPSM distiller
# Purpose:     get useful mobile data from gsmarena scrapped files
#
# Author:      Mohamad Hamza EL BAKOUCHI
#
# Created:     22/12/2016
# Copyright:   (c) urpsm 2016
# Licence:     <hamza.bakouchi(at)gmail.com>
#-------------------------------------------------------------------------------

import codecs, os
from bs4 import BeautifulSoup as bs
import argparse
import nltk
import sys, linecache
FOLDER_NAME= "gsmarena"
import re


import logging

logger = logging.getLogger('urpsm')
hdlr = logging.FileHandler('urpsm.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

parser=argparse.ArgumentParser(
    description='''get useful mobile data from gsmarena scrapped files ''',
    epilog="URPSM forever")

parser.add_argument('--folder', type=str, default=FOLDER_NAME, help='Working folder')
parser.add_argument('--brand', type=str,  help='the brand to tokenize')

tokenize_parser = parser.add_mutually_exclusive_group(required=False)

tokenize_parser.add_argument('--tokenize', dest='tokenize', action='store_true')
tokenize_parser.add_argument('--no-tokenize', dest='tokenize', action='store_false')
parser.set_defaults(tokenize=False)

args=parser.parse_args()
from HTMLParser import HTMLParser

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    # if 'bootcamp-master' in PROJECT_DIR:
    msg = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print msg
    return msg

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
from nltk.tokenize import TweetTokenizer
tknzr = TweetTokenizer()
#vpython distiller.py --folder f:\gsmarena-full\gsmarena2 --tokenize --brand Samsung suddsud spth
def tokenize(brand):
    

    brand_folder = os.path.join(args.folder, brand)

    things = os.listdir(brand_folder)
    for thing in things:
        thing = os.path.join(brand_folder, thing)
        if os.path.isfile(thing):
            # txts = os.listdir(thing)
            # for txt in txts:
            #     _txt = os.path.join(thing, txt)
            #     print txt
                if thing.endswith('-2.txt'):
                    markup = codecs.open(thing, 'rb').read()
                    # clean_data = strip_tags(markup)
                    useful_data  = bs(markup, "html.parser")
                    specs = useful_data.find('div', {'id':'specs-list'})
                    modelname = useful_data.find("h1", {"class" : "specs-phone-name-title"}).text
                    try:
                        versions     = specs.find('p').text
                        if versions:
                        # print versions
                            tokens       = tknzr.tokenize(versions)
                        # print tokens
                        # newfilename  = thing.replace('-2.txt','-tokens.txt')
                        # newfile = codecs.open(newfilename, 'w', 'utf-8-sig')
                        # for token in tokens:
                        #     newfile.write(token)
                        #     newfile.write('\n')
                            urpsm_name = urpsm_name_maker(args.brand, modelname, tokens)
                            cleaned_tokens = clean_tokens(tokens)
                            series = ' '.join(cleaned_tokens)
                            _modelname = tknzr.tokenize(modelname)
                            clean_modelname = clean_tokens(_modelname)
                            cleaned_modelname = ' '.join(clean_modelname)
                            series = remove_model_from_series(cleaned_modelname,  series )

                            # cleaned_modelname = cleaned_modelname.replace('plus','+').replace('Plus', '+')
                            # cleaned_modelname = remove_typing_errors(cleaned_modelname)
                            # series = remove_typing_errors(series)
                            cleaned_modelname =  " ".join(cleaned_modelname.split())
                            series            = " ".join(series.split())

                            print  cleaned_modelname, series
                        
                        # newfile.close()
                    except:
                        # PrintException() 
                        # print brand, modelname
                        # modelname = useful_data.find("h1", {"class" : "specs-phone-name-title"})
                        error = "%s %s does not have versions see path: %s" % (brand,  modelname , thing)
                        logger.error(error)
    print brand, 'is processed'
                    # exit()


def remove_model_from_series(model, series):
    model_tokens = tknzr.tokenize(model)
    series_tokens = tknzr.tokenize(series)
    clean = []
    for token in series_tokens:
        if not token in model_tokens:
            # for _ in stale:
            #     if _ in token:
            #         if not _.isdigit():
            #             token = token.replace(_,'')
            clean.append(token)
    return ' '.join(clean)

stale = [
'Versions', 'Also', 'known', 'as', '(',')' , ':', ',', '/', ');', '):', ';', 'BH', 'DF',
'This','is','not','a','GSM','device','it','will','not','work','on','any','GSM','network','worldwide','.',
'Europe','Latin','America','Taiwan','Southeast','Asia','Hong','Kong','New','Zealand','Australia','Africa',
'UAE','Malaysia','Indonesia','Singapore','with','no','LTE','Brazil', 'Duos',
'HK','India','South','Thailand','LATAM','Virgin','Mobile','Boost','China','South','Pakistan','Vietnam','Canada','Verizon','Sprint','US','Cellular','Sprint',
'T-Mobile','North','Available','in','China','128','GB','storage','and','6','GB','RAM','T-Mobile','version','5','MP','rear','camera','and','2','MP','front','camera',
'Korea','Curved','screen','version','available',
'Tablet','support','for','voice','communication','SMS','MMS', 'For','AT','Unofficial','preliminary','specifications','Global','Curved','Philippines',
'Wi-Fi','only','S-Pen','versions', 'USA', ' USA ','dual-SIM','card','slots', 'Turkey',
 'model','1080p','display','3','Nxt','&','Cricket','','Metro','PCS','Value','Edition','DD' , 'EMEA', 'FM', 'BH','Wide','plus','+', 'Curved', 'Plus',
'Product','image','illustrative','purposes', 'single-SIM','slot','Vibrant','Vibrant', 'Telstra','Germany','Within','Jasper','"','N','CDMA','data',
'Galaxy','Q','Txt','Previously','Triumph','different','design','announced','Initially','announced','2003','Pocket','PC','2002',
'Chinese','Initially','','2003','WLAN','Corby','Smartphone','Europa','550', 
'Saturn','Orange','Naos','Leo','Lite','Portal','Jack','projector','phone','WiTu','AMOLED','Galaxy','S','III','mini','S3','more',
'Vodafone','exclusive','NFC','connectivity','Google','Play','LTE-A','SK','Telecom','Hoppin','Pixon','Waikiki','Moment','Transform','Ultra','Showcase',
]

def remove_typing_errors(string):
    for litter in stale:
        string = string.replace(litter, '')
    return string
def clean_tokens(tokens):
    clean = []
    for token in tokens:
        if not token in stale:
            clean.append(token)

    return clean


def urpsm_name_maker(brand, model, tokens):
    gsmarena_tokens = tknzr.tokenize(model)
    brandless = []
    for ga_token in gsmarena_tokens:
        if not ga_token == brand:
            brandless.append( ga_token )
    # print gsmarena_name
    gsmarena_name = ' '.join(brandless)
    return gsmarena_name



CAMERA_REGEX = "(\d*\.?\d+\ MP)"
PRICE_REGEX = "(\d*\.?\d+\ EUR)"
BATTERY_REGEX = "(\d*\.?\d+\ mAh)"
RAM_SIZE_REGEX = "(\d*\.?\d+\ MB\ RAM|\d*\.?\d+\ GB\ RAM)"
INTERNAL_RAM_SIZE_REGEX =   "(\d*\.?\d+\ MB|\d*\.?\d+\ GB)"

def literal_details_td(chunck):
    key   = str(chunck.find('td', {'class':'ttl'}).text)
    value = str(chunck.find('td', {'class':'nfo'}).text)
    return key, value


def numerical_details(chunk, regex, primary):
        feature = 0
        try:
            for item in chunk:
                tds = item.findAll("td")
                if primary is True:
                    if str(tds[0].text) == "Primary":
                        string = re.findall(regex, str(tds[1].text))
                        if len(string):
                            string = string[0].split()
                            feature = float(string[0])
                        break
                else:
                    string = re.findall(regex, str(tds[1].text))
                    if len(string):
                        string = string[0].split()
                        feature = float(string[0])
##                        if string[1] == 'MB':
##							feature = round(feature/1024, 2)
                    break
        except:
            pass
        return feature

def get_mobile_name(soup):
		heading = soup.find("h1", {"class" : "specs-phone-name-title"})
		return str(heading.text)

def process_features(soup):
    features = dict()

def distill_details(details):
    distilled = dict()
    for detail, bulk in details.iteritems():
        couples = dict()
        for data in bulk:
            couple =  literal_details_td(data)
            couples[couple[0]] = couple[1]
        distilled[detail] = couples
    return distilled




def process_details(soup):
    details = dict()
    tables = soup.findAll("table")

    for item in tables:
        type_name = str(item.find("th").text)
        print type_name
        details[type_name] = item.findAll("tr")
    return details


##def process_head(soup):
##    popularity = soup.find('li', {'class':'light pattern help help-popularity'}).text
##    hits       = soup.find('li', {'class':'light pattern help help-popularity'}).text


def process_model(model):
    markup = codecs.open(model, 'rb').read()
##    print markup
    soup = bs(markup)
    model_name = get_mobile_name(soup)

    bulk =  process_details(soup)
##    print details
    details = distill_details(bulk)

    exit()

def process_brand(brand):
    things = os.listdir(brand)
    for thing in things:
        model = os.path.join(brand, thing)
        if os.path.isfile(model):
            print model
            process_model(model)


def main():
    print args.folder
    things = os.listdir(args.folder)
##    print models
    for thing in things:
        brand = os.path.join(args.folder, thing)
        if os.path.isdir(brand):
            print brand
            process_brand(brand)

if __name__ == '__main__':
    if not args.tokenize:
        main()
    else:
        tokenize(args.brand)
