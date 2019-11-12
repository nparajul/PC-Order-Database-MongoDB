import pymongo
from pymongo import MongoClient
import csv
import configparser
from bson.objectid import ObjectId
import redis




def initialize():
    # this function will get called once, when the application starts.
  
    global customers
    global products
    global orders
    client = MongoClient()
    customers = client.newproject1.customers
    products = client.newproject1.products
    orders = client.newproject1.orders
    
    
    global myredis
    myredis = redis.StrictRedis(host='redis-19530.c91.us-east-1-3.ec2.cloud.redislabs.com', port=19530, password='XXXXXXXXXXXXXXXXXXXXXXXXX', charset='utf-8', decode_responses=True)


def get_customers():
	all=customers.find({})
	for each in all:
		yield each

def get_customer(id):
	my_cust= customers.find_one({'_id':ObjectId(id)})
	return my_cust

def upsert_customer(customer):
	if "_id" in customer:
		toInsert = {'firstName':customer['firstName'], 'lastName' : customer['lastName'], 'street' : customer['street'], 'city' : customer['city'], 'state' : customer['state'], 'zip' : customer['zip']}
		customers.update_one({'_id':ObjectId(customer['_id'])}, {'$set':toInsert})
	else:
		toInsert = {'firstName':customer['firstName'], 'lastName' : customer['lastName'], 'street' : customer['street'], 'city' : customer['city'], 'state' : customer['state'], 'zip' : customer['zip']}
		customers.insert_one(toInsert)


def delete_customer(id):
	customers.delete_one({'_id':ObjectId(id)})
	orders.delete_many({'customerId':ObjectId(id)})
	
    
def get_products():
	all=products.find({})
	for each in all:
		yield each
    

def get_product(id):
	my_product = products.find_one({'_id':ObjectId(id)})
	return my_product

def upsert_product(product):
	if "_id" in product:
		toInsert = {'name':product['name'], 'price' : product['price']}
		products.update_one({'_id':ObjectId(product['_id'])},{'$set':toInsert})
	else:
		toInsert = {'name':product['name'], 'price' : product['price']}
		products.insert_one(toInsert)

    

def delete_product(id):
	products.delete_one({'_id':ObjectId(id)})
	orders.delete_many({'productId' : ObjectId(id)})
	myredis.flushall()
	

def get_orders():
    all = orders.find({})
    for each in all:
    	my_order={'_id':each['_id'],'customerId':each['customerId'], 'productId':each['productId'], 'date':each['date'], 'customer':get_customer(each['customerId']), 'product':get_product(each['productId'])}
    	yield my_order


def get_order(id):
	my_order=orders.find_one({'_id':ObjectId(id)})
	return my_order
 
def upsert_order(order):
	orders.insert_one(order)
	myredis.flushall()

def delete_order(id):
	orders.delete_one({'_id':ObjectId(id)})
	myredis.flushall()

def customer_report(id):
    return None

  

# - When a product dictionary is computed, it is saved as a hash in Redis with the product's
#   ID as the key.  
def sales_report():
	report=list()
	product_list= get_products()
	for each in product_list:
		my_id=each['_id']
		details = myredis.hgetall(my_id)
		if myredis.exists(my_id):
			report.append(details)
		else:
			order = [o for o in get_orders() if o['product']['_id'] == my_id]  
			order = sorted(order, key=lambda k: k['date'])
			if(len(order)>0):
				each['total_sales'] = len(order)
				each['gross_revenue'] = each['price'] * len(order)
				each['last_order_date'] = order[-1]['date']
				myredis.hmset(my_id, each)
				report.append(each)
	return report		
    

initialize()