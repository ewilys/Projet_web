# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import server_function
import os, hashlib
import sqlite3 

# ............................................................................................... #
app = Flask(__name__)
app.secret_key = os.urandom(256)
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # la session dure une heure
   
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
	if 'usernameMember' in session: 
		#A CHANGER PAR HOME QUAND ON AURA FINI LA PAGE HTML HOME 
		result = server_function.getMemberProfile(session['usernameMember'])
		return redirect(url_for('profileMember',login=session['usernameMember']))
	elif 'usernameClub' in session: 
		result = server_function.getClubProfile(session['usernameClub']) 
		print(result)
		return render_template('profileClub.html',clubName=result[0],clubCity=result[1],clubEmail=result[2])
	else: 
		if request.method =='POST' : 
			
			#ajax handler
			if request.json :
				log_user=request.json["login"]
				psw=request.json["pswrd"]
				mtype=request.json["memtype"]
				
				#validate login
				if server_function.checklog(log_user, mtype) == True : 
					user= "login valide"
				else :
					user= " login inconnu "
					
				#validate psw
				if psw != "" : 
					if server_function.sign_in(log_user,psw, mtype) == True:
						psw= "mot de passe valide"
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
	    				#session['username']=login 
	    				mtype=mtype.capitalize()
	    				if mtype=='Club':
	    					session['usernameClub']=login 
	    				else : 
	    					session['usernameMember']=login 
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
	session.clear()
	#session.pop('pseudo', None)
	return redirect('/login')

@app.route('/register/club', methods=['GET', 'POST'])
def registerClub():
	if request.method=='POST':
		#ajax handler
		if request.json :
			clubName=request.json['userName']
			login=request.json['newLogin']
			email=request.json['email']
			noFede=request.json['noFede']
			
			if clubName!="" :
				#duplicate license :
				if server_function.checkClubName(clubName) == False : 
					clubName="nom de club valide "
				else :
					clubName="ce nom de club existe deja"
						
				
			if login != "":
				#duplicate login :
				if server_function.checklog(login,"club") == False:
					login="login valide"
				else : 
					login="ce login existe deja , veuillez en choisir un autre"
					
			if len(noFede)==6:
				#validate clubId :
				if server_function.checkClubId(noFede) == False:
					noFede="numero du club valide"
				else : 
					noFede="ce numero de club existe deja"
			elif noFede !="" :
				noFede="veuillez entrer un numero de club a 6 chiffres"
			
			if email != "":
				#validate email:
				if server_function.checkEmail(email, "club") == False :
					email="email valide"
				else:
					email="cet email existe deja, veuillez en choisir un autre"
							
			return jsonify({'clubName':clubName, 'newLogin': login, 'email':email,'noFede':noFede})
			
		#submission :	
		if server_function.sign_up_club(request.form['userName'],request.form['city'],request.form['email'],request.form['login'],request.form['pswrd'],request.form['noFederation']) == True:
			session['usernameClub']=request.form['login']
			return redirect( url_for('profileClub',login=request.form['login']))
		else: 
			return redirect(url_for('registerClub'))
	return render_template('registerClub.html')
	
@app.route('/register/member', methods=['GET', 'POST'])
def registerMember():
	if request.method == 'POST':
		#ajax handler
		if request.json :
			license=request.json['license']
			login=request.json['newLogin']
			email=request.json['email']
			clubId=request.json['clubId']
			
			if len(license)==8 :
				#duplicate license :
				if server_function.checkLicense(license) == False : 
					license="numero de licence valable"
				else :
					license="ce numero de licence existe deja"
			elif license !="":
				license ="veuillez entrez un numero de licence a 8 chiffres"
				
				
			if login != "":
				#duplicate login :
				if server_function.checklog(login,"member") == False:
					login="login valide"
				else : 
					login="ce login existe deja , veuillez en choisir un autre"
					
			if len(clubId)==6:
				#validate clubId :
				if server_function.checkClubId(clubId) == True:
					clubId="numero du club valide"
				else : 
					clubId="numero du club invalide"
			elif clubId !="" :
				clubId="veuillez entrer un numero de club a 6 chiffres"
			
			if email != "":
				#validate email:
				if server_function.checkEmail(email,"member") == False :
					email="email valide"
				else:
					email="cet email existe deja, veuillez en choisir un autre"
							
			return jsonify({'license':license, 'newLogin': login, 'email':email,'clubId':clubId})
			

		#submission :	
		if server_function.sign_up_member(request.form['userNo'],request.form['userName'],request.form['userFirstName'],request.form['bday'],request.form['userMail'],request.form['clubId'],request.form['login'],request.form['pswrd']) == True:
			session['usernameMember']=request.form['login']
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
	print(result)
	return render_template('profileClub.html',clubName=result[0],clubCity=result[1],clubEmail=result[2])
	
@app.route('/home/profileMember/<login>')
def profileMember(login): 
	#nom, prenom, categorie, club, email 
	result = server_function.getMemberProfile(login) 
	print(result)
	return render_template('profileMember.html', userName=login)


@app.route('/home/profile/addLicense')
def addLicense(): 
	return render_template('addLicense.html')

@app.route('/home/search')
def search (): 
	return render_template('search.html')

@app.route('/home/creaEvent', methods=['GET', 'POST'])
def createEvent():
	if request.method== 'POST': 
		adress=request.form['city']+" "+ request.form['road']
		nameEvent=request.form['nameEvent']
		categorie=request.form['categorie']
		nbPlace=request.form['nbPlace']
		start= request.form['start']
		desc= request.form['desc']
		hour=request.form['hour']
		imageLink="http://www.google.fr/"
		if server_function.createEvent(nameEvent,categorie,nbPlace,desc,adress,start,hour)==1: 
			print("SUCESS !" )
			return redirect(url_for('main'))
		else: 
			print("error on event creation")
			return redirect(url_for('createEvent'))
	else: 
		return render_template('createEvent.html')

@app.route('/main')
def main():
	return "MAIN"
# ............................................................................................... #
#lancement appli
if __name__ == '__main__':
	app.run(debug=True)

# ............................................................................................... #
