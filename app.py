from flask import *
import worker


app = Flask(__name__)

def check_authantication(req):
	if request.cookies.get('userID'):
		if len(worker.check_id(request.cookies.get('userID'))):
			return("ok")
		else:
			return("error")
	else:
		return("error")

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/log_in' ,methods = ['POST', 'GET'])
def log_in():
	if request.method == 'POST':
		value = request.form
		id_no = worker.log_in(value)
		print(id_no)
		if id_no != "error":
			resp = make_response(render_template('readcookie.html',data = "/Dashboad"))
			resp.set_cookie('userID', id_no)
			return resp
		else:
			return redirect(url_for('log_in'))
	else:
		return render_template('log_in.html')

@app.route('/sign_up',methods = ['POST', 'GET'])
def sign_up():
	if request.method == 'POST':
		value = request.form
		if worker.sign_up(value) == "ok":
			return redirect(url_for('log_in'))
		else:
			return redirect(url_for('sign_up'))
	else:
		return render_template('sign_up.html')
   
@app.route('/Dashboad')
def Dashboad():
	if check_authantication(request) == "ok":
		id_no = request.cookies.get('userID')
		data = worker.Dashboad(id_no)
		print(data)
		if data != "error":
			hackathon_list = worker.check_registration(data)
			return render_template('Dashboad.html', data = hackathon_list , length= len(hackathon_list) )
		elif data == "error":
			return render_template('Dashboad.html', data = [] , length= 0 )                          
	else:
		return redirect(url_for('log_in'))
		
@app.route('/Dashboad/<name>')
def Dashboad_name(name):
	if check_authantication(request) == "ok":
		id_no = request.cookies.get('userID')
		data = worker.Dashboad(id_no)
		if data != "error":
				hackathon_list = worker.check_registration(data)
				Data = worker.dashboad(name)
				return render_template('Dashboad_name.html',data = Data , dta = hackathon_list, length=len(Data),leng= len(hackathon_list),flag = "full" , Name = name)
		else:
			return redirect(url_for('log_in'))
	else:
		return redirect(url_for('log_in'))
		
		

@app.route('/Organiser_form',methods = ['POST', 'GET'])
def Organiser_form():
	if check_authantication(request) == "ok":
		if request.method == 'POST':
			value = request.json
			id_no = request.cookies.get('userID')
			return({ "sever_response": worker.organiser_form(id_no,value)})
		else:
			id_no = request.cookies.get('userID')
			data = worker.Dashboad(id_no)
			if data != "error":
				hackathon_list = worker.check_registration(data)
				return render_template('Organiser_form.html', data = hackathon_list , length= len(hackathon_list) )
			elif data == "error":
				return render_template('Organiser_form.html', data = [] , length= 0 )       
		
	else:
		return redirect(url_for('log_in'))
	   
@app.route('/hackathon/<name>',methods = ['POST', 'GET'])
def hackathon(name):
	data = worker.register_form(name)
	print(data)
	if data != "error":
		if request.method == 'POST':
			value = request.json
			return ({"sever_response": worker.register_update(value,name) })
		else:
			return render_template('registration_form.html',Data = data["organizer"], Name = data["hackathon_name"] )
	else:
		return redirect(url_for('log_in'))
		
@app.route('/log_out')
def log_out():
		resp = make_response(render_template('readcookie.html',data = "/"))
		resp.set_cookie('userID',  expires=0)
		return resp
		
   
if __name__ == '__main__':
   app.run(debug = True)
