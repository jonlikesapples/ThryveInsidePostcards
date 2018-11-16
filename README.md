# ThryveInside Postcards
Coding Challenge for ThryveInside Fall 2018.
Author: Jonathan Wong

Written in Python, utilized Lob and Randomuser API, stored with AWS DyanmoDB and hosted on AWS EC2.

Database contains 1000 rows of randomly populated customer data. Data was populated using https://randomuser.me/.

postcards.py: python script that parses through a dynamoDB database,
checks if today's date is anniversary, and sends a postcard using Lob API. https://lob.com/.

An external cronjob will run this script everyday at 5am.

Snippet of database (from DynamoDB):
![DB Schema](https://i.imgur.com/fH0pkWV.png)

Result (from Lob Dashboard):
![Result](https://i.imgur.com/O3ZdR0u.png)
