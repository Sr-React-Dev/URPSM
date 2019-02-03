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
from peewee import *

psql_db = PostgresqlDatabase('mbdb_test2', user='mobilify', password='&é"aze123.')

class Phone_Brand(Model):
    name = CharField(max_length=255, unique=True)
    # slug = SlugField(editable=False, db_index=True)

    created = DateTimeField()
    updated = DateTimeField()
    class Meta:
        database = psql_db



class Phone_Model(Model):
    name = CharField(max_length=255)
    # slug = SlugField(editable=False, db_index=True)
    brand = ForeignKeyField(Phone_Brand, related_name='brand_models')

    created = DateTimeField()
    updated = DateTimeField()

    

    class Meta:
        database = psql_db

mobiles = Phone_Model.select()

for mobile in mobiles:
    # print mobile.name, mobile.brand.name, mobile.id
    print mobile.id, mobile.brand.name, mobile.name.strip()
    # test = "%s%s" % (mobile.brand.name.strip().lower(), mobile.name.strip().lower())
    # test = test.replace(' ','')
    # print test
def main():
    pass

if __name__ == '__main__':
    main()
