# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import server_function
import os, hashlib
import sqlite3 

# ............................................................................................... #
app = Flask(__name__)
app.secret_key = os.urandom(256)   
# ............................................................................................... #

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
		
		#ajax handler
		if request.json :
			log_user=request.json["login"]
			psw=request.json["pswrd"]
			mtype=request.json["memtype"]
			
			#validate login
			if server_function.checklog(log_user, mtype) == True : 
				user= " Le login est valide ! Well done !"
			else :
				user= " login inconnu "
				
			#validate psw
			if psw != "" : 
				if server_function.sign_in(log_user,psw, mtype) == True:
					psw= "le mot de passe est le bon ! bonne memoire"
				else :
					psw="mot de passe incorrect"		
			return jsonify({'user': user, 'psw' : psw})
			
		#submission 	
    		if request.form['subBtn'] == 'Connexion':
       			# read the posted values from the UI
			login = request.form['userID']
   	 		password = request.form['pswrd']
 			mtype=request.form['memberType']
 			
	    		# validate the received values
	    		oklog= server_function.sign_in(login,password, mtype)
	    		print (oklog)
	    		if oklog== True: #signIn has worked
	    			session['username']=login 
	    			mtype=mtype.capitalize()
	    			return redirect(url_for("profile"+mtype, login=login))
	    		else: 
	    			return redirect('/login')
		
		#redirect to appropriate signUp	
	    	elif request.form['subBtn'] == 'Club':
    			return redirect(url_for('registerClub'))
    		elif request.form['subBtn'] == 'Sportif':
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
		if server_function.sign_up_club(request.form['username'], request.form['ville'],request.form['email'],request.form['login'],request.form['pswrd'],request.form['nofederation']) == 0 :
			return redirect(url_for('profileClub',login=request.form['login'))
		else: 
			return redirect(url_for('registerClub'])) 
	return render_template('registerClub.html')
	
@app.route('/register/member', methods=['GET', 'POST'])
def registerMember():
	if request.method == 'POST':
		#ajax handler
		if request.json :
			license=request.json['license']
			
			#duplicate license :
			if server_function.checkLicense(license) == False : 
				
			
		#submission :	
		if server_function.sign_up_member(request.form['userNo'],request.form['userName'],request.form['userFirstName'],request.form['bday'],request.form['userMail'],request.form['clubId'],request.form['login'],request.form['pswrd']) == 0:
			return redirect( url_for('profileMember',login=request.form['login']))
		else: 
			return redirect(url_for('registerMember'))
	#GET :
	return render_template('registerMember.html')

@app.route('/home')
def home(): 
	return render_template('home.html')


@app.route('/home/profileClub/<login>')
def profileClub(login): 
	result = server_function.getClubProfile(login) 
	return render_template('profileClub.html')
	
@app.route('/home/profileMember/<login>')
def profileMember(login): 
	result = server_function.getMemberProfile(login) 
	return render_template('profileMember.html')


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
