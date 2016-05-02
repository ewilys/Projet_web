# ............................................................................................... #

from flask  import *
from sqlalchemy import *

import os, hashlib
import sqlite3 
# ............................................................................................... #

app = Flask(__name__)


# ............................................................................................... #
#gestion base de donnees

conn= sqlite3.connect('dtb.db')
c= conn.cursor()
c.execute('SELECT * FROM MEMBRES')

for row in c.execute('SELECT LOGIN FROM MEMBRES'):
	print(row)


# ............................................................................................... #
#gestion des url

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method =='POST' : 
		
    		if request.form['subBtn'] == 'Connexion':
       			# read the posted values from the UI
			login = request.form['userID']
   	 		password = request.form['pswrd']
 		
	    			# validate the received values
	    		if login and password :
	    			flash("all fiels good! ")
		    		return redirect(url_for("main"))
			else :
				flash("Invalid password for login :"+login)
	    			return redirect('/login')
	    	elif request.form['subBtn'] == 'Club':
    			return redirect(url_for('club'))
    		elif request.form['subBtn'] == 'Membre':
    			return redirect(url_for('membre'))
       		
	else:
		return render_template('login.html')  


@app.route('/logout')
def logout():
	from_page = request.args.get('from', 'main')
	session.clear()
	return redirect('/login')

@app.route('/register/club', methods=['GET', 'POST'])
def registerClub():
	if request.method=='POST':
		#username= request.form('username') 
		#ville=request.form('ville')
		#email= request.form('email')
		#nofederation= request.form('nofederation')
		#login=request.form('login')
		#pswrd= request.form('pswrd')
		return redirect('main')
	return render_template('registerClub.html')
	
@app.route('/inscription/membre', methods=['GET', 'POST'])
def registerMember():
	if request.method == 'POST':
		#username= request.form('username') 
		#userFirstName = request.form('userfirstname')
		#bday=request.form('bday')
		#usermail= request.form('usermail')
		#userNo= request.form('userNo')
		#login=request.form('login')
		#pswrd= request.form('pswrd')
		return redirect( url_for('main'))
	return render_template('registerMember.html')

@app.route('/home')
def home(): 
	return render_template('home.html')

@app.route('/home/profile')
def profil(): 
	return render_template('profile.html')

@app.route('/home/profile/addLicense')
def addLicense(): 
	return render_template('addLicense.html')

@app.route('/home/search')
def search (): 
	return render_template('search.html')

@app.route('/home/creaEnvent')
def createEvent():
	return render_template('createEvent.html')

@app.route('/main')
def main():
	return "MAIN"
# ............................................................................................... #
#lancement appli
if __name__ == '__main__':
    app.run(debug=True)

# ............................................................................................... #
