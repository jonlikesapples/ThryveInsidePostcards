'''
Coding Challenge for Software Engineer Position at ThryveInside.

postcards.py: python script that parses through a dynamoDB database, 
checks if today's date is anniversary, and sends a postcard using Lob API.
Hosted on AWS EC2, using a cronjob that will run this script everyday at 5am.
crontab syntax: 0 5 * * * /usr/bin/python3 /home/ubuntu/postcards.py >> /home/ubuntu/output.txt 2>&1

__date__: 11/15/2018
__author__: Jonathan Wong
__version__: 1.0
__email__: CVJonWong@gmail.com
'''

import lob
from boto3.session import Session
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import json
import requests
import datetime
from config import *

##API keys are stored in Config.py
lob.api_key = LOB_API_KEY
session = Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME
)

dynamodb = session.resource('dynamodb')
table = dynamodb.Table('ThryvePostcards')

#all postcards will be sent from Thryve
THRYVE_INSIDE = lob.Address.create(
    name='Thryve Inside',
    address_line1='4701 Patrick Henry Drive',
    address_city='Santa Clara',
    address_state='CA',
    address_country='US',
    address_zip='95054'
)

def parse_date(datestring):
    return "{}/{}/{}".format(datestring[5:7],
                             datestring[8:10],
                             datestring[0:4])

#parse month and date from a string, format: YYYY-MM-DDTHH:MM:SSZ
def parse_month_and_day(datestring):
    return "{}/{}".format(datestring[0:2], datestring[3:5])

#given a date, checks if today's date is the same date, returns true if is
def return_true_if_anniversary(datestring):
    if datetime.datetime.today().strftime('%m/%d') == datestring:
        return True
    return False

# ThryvePostcards table contains 1000 entries of customers.
for i in range(0, 1000):
    try:
        response = table.get_item(Key={'customerID': i})
        customer = response['Item']
    except:
        print("No entries match with that customerID")
    else:
        anniversaryDate = parse_month_and_day(str(customer['Anniversary']))
        if return_true_if_anniversary(anniversaryDate):
            createdPostcard = lob.Postcard.create(
                description='Happy Anniversary!',
                metadata={
                    'name': customer["Name"],
                    'Anniversary': customer['Anniversary']
                },
                to_address={
                    'name': customer["Name"],
                    'address_line1': customer['address_line1'],
                    'address_city': customer['address_city'],
                    'address_state': customer['address_state'],
                    'address_zip': customer['address_postcode'],
                    'address_country': 'US'
		    	},
                from_address=THRYVE_INSIDE,
                front="""
					<html>
					<div style="padding: 30px;">
					  <div style="margin: 0 auto;
					  width: 200px;
					  text-align: center;
					  vertical-align: middle;
					  line-height: 20px;">
					   <h2>
					      Happy Anniversary From Thryve!
					   </h2>
					  </div>
					</div>
					</html>""",
                back=""" <div> </div> """
		)
print(datetime.datetime.now());
print("i'm done!")

# if __name__ == '__main__':
# 	app.debug = True
# 	from os import environ
# 	app.run(debug=True, host='0.0.0.0', port=int(environ.get("PORT", 5000)))
# 	app.run(threaded=True)
