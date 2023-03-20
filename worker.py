from pymongo import MongoClient
import uuid

mongodbHost = "127.0.0.1"
mongodbPort = 27017

client = MongoClient(mongodbHost, mongodbPort)
database = client['hackathon']
log_in = database['log_in']
organiser_form = database['organiser_form']
register_form = database['register_form']


def sign_up(value):
	try:
		id_no = uuid.uuid4()
		data = list(database.log_in.find({"email": value['email']}))
		if (len(data) == 0):
			database.log_in.insert_one({
            	"id_no": str(id_no), "fname": value['fname'] , "password": value['pass'], "email": value['email']
        	})
			return "ok"
		else:
			return "already"
	except:
		return "error"
		
def log_in(value):
	try:
		data = list(database.log_in.find({
        	"password": value['pass'], "email": value['email']
        }))
		if (len(data)>0):
			return (data[0])['id_no']
		else:
			return "error"
	except:
		return "error"
		
def organiser_form(id_no,value):
	try:
		database.organiser_form.insert_one({
            	"id_no": id_no, "organizer": value["data_org"] , "student": value["data_std"], "company": value["company"], "hackathon_name": value["hackathon_name"]
        	})
		return "ok"
	except:
		return "error"
		
def register_form(name):
	try:
		data = list(database.organiser_form.find({
        	"hackathon_name": name
        }))
		if (len(data)>0):
			return data[0]
		else:
			return "error"
	except:
		return "error"			

def register_update(value,name):
	try:
		database.register_form.insert_one({
        	"hackathon_name": name , "Full_name": value["name"],"Email": value["email"],"phone": value["phone"],"about": value["About"]
        })
		return "ok"
	except:
		return "error"		

def Dashboad(id_no):
	try:
		data = list(database.organiser_form.find({
        	"id_no": id_no
        }))
		if (len(data)>0):
			return data
		else:
			return "error"
	except:
		return "error"	
					
def check_registration(data):
	try:
		hackathon_list =  []
		for i in data:
			hackathon_list.append(i["hackathon_name"]) 
		return (hackathon_list)
	except:
		return "error"				
		
def dashboad(hackathon_name):
	try:
		data = list(database.register_form.find({
        	"hackathon_name": hackathon_name
        }))
	
		return data
	except:
		return "error"
		
def check_id(id_no):
	try:
		data = list(database.log_in.find({
        	"id_no": id_no
        }))
		return data
	except:
		return "error"	
		
