############ All you need to modify is below ############
# Full path and name to your csv file
csv_filepathname="C:/Users/winni/Downloads/review_data.csv"
# Full path to the directory immediately above your django project directory
your_djangoproject_home="C:/MAMP/htdocs/KTL2002/KTL2002_webapp"
############ All you need to modify is above ############

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] ='KTL2002.settings'

import django
django.setup()

from products.models import ProductCategory

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

cat = []

for row in dataReader:
    if (not(row[7] in cat)):
        a = ProductCategory()
        a.product_category_name = row[7]
        a.save()
        cat.append(row[7])
        print('found ', row[7])

# length = len(user_id)

# for i in range(length):
#     a = User(username=user_name[i])
#     # a.username = user_name[i]
#     a.first_name = user_id[i]
#     a.password = "000000"
#     a.save()

