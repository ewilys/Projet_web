# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import server_function
import os, hashlib
import sqlite3 
# ............................................................................................... #
app = Flask(__name__)
app.secret_key = os.urandom(256)        

SALT = 'foo#BAR_{baz}^666'       #permet de tatouer le mot de passe   ,modif l'info    

# ............................................................................................... #
#gestion base de donnees

"""
engine = create_engine('sqlite:///dtb.db', echo=True)
metadata = MetaData()

accounts = Table('membre_connex', metadata,
    Column('login', String, primary_key=true),
    Column('password_hash', String, nullable=False))    

pages = Table('pages', metadata,
    Column('name', String, primary_key=true),
    Column('text', String))# contenu brut de la page

metadata.create_all(engine)

def page_content(name):
    db = engine.connect()
    try:
        row = db.execute(select([pages.c.text]).where(pages.c.name == name)).fetchone()
        if row is None:
            return '**(This page is empty or does not exist.)**'
        return row[0]
    finally:
        db.close()

def indexation():
    db = engine.connect()
    try:
        row=list()
        for i in db.execute("select name from pages") :
        	row.append(i)
        	print(row)
        	return row
    finally:
        db.close()
        
        
def update_page(name, text):
    db = engine.connect()
    try:
        row = db.execute(select([pages.c.name]).where(pages.c.name == name)).fetchone()
        if row is None:
            db.execute(pages.insert().values(name=name,text=text))
        else :
            db.execute(pages.update().values(text=text).where(pages.c.name==name))
    finally:
        db.close()
     

def delete_page(name, text):
	db = engine.connect()
    	try:
    		if db.execute(select([pages.c.name]).where(pages.c.name == name)).fetchone() != None:
    			db.execute(pages.delete().where(pages.c.name == name))       	
    	finally:
        	db.close() 
        
def hash_for(password): #hashage du password 
	salted = '%s @ %s' % (SALT, password)
	return hashlib.sha256(salted).hexdigest()       


def authenticate_or_create(login, password):
    db = engine.connect()
    hash_pass=hash_for(password)
    try:
        if db.execute(select([accounts.c.login]).where(accounts.c.login == login)).fetchone() is None:
            db.execute(accounts.insert().values(login=login,password_hash=hash_pass))
            return True
        else: 
        	  s=select([accounts.c.login]).where(
        			and_(
        				accounts.c.login ==login,
        				accounts.c.password_hash == hash_pass
        			)
        		)
        	  return db.execute(s).fetchone() != None
    finally:
        db.close()
"""

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
	    			exists= server_function.sign_in(login,password)
	    			print(exists) 
	    			if exists== True: 
	    				return redirect(url_for("main"))
	    			else: 
	    				flash("Invalid password or login")
	    				return redirect('/login')
			else :
				flash("Please enter a login or password ")
	    			return redirect('/login')
	    	elif request.form['subBtn'] == 'Club':
    			return redirect(url_for('registerClub'))
    		elif request.form['subBtn'] == 'Membre':
    			return redirect(url_for('registerMember'))
       		
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
	
@app.route('/register/member', methods=['GET', 'POST'])
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
def profile(): 
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
