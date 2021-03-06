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
#gestion des url

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'mtype' in session: 
		#A CHANGER PAR HOME QUAND ON AURA FINI LA PAGE HTML HOME  
		if session['mtype']=='Member': 
			result = server_function.getMemberProfile(session['username'])
			return redirect(url_for('home',login=session['username']))
		elif session['mtype']=='Club': 
			result = server_function.getClubProfile(session['username']) 
			#print(result)
			return redirect(url_for('home',login=session['username']))
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
					if server_function.sign_in(log_user,psw, mtype)[0] == True:
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
		    		oklog, repLog = server_function.sign_in(login,password, mtype)
	    			print (oklog)
			    	if oklog== True: #signIn has worked
	    				mtype=mtype.capitalize()
	    				if mtype=='Club':
	    					session['username']=login 
	    					session['mtype']='Club'
	    				else : 
	    					session['username']=login 
	    					session['mtype']='Member'
	    				return redirect(url_for('home',login=session['username']))
	    			else: 
	    				if repLog == True:
	    					flash("Echec de connexion : Le mot de passe est incorrect")
	    				else :
	    					flash("Echec de connexion : Le login est incorrect")
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
					clubName="ce nom de club existe deja, veuillez en choisir un autre"
						
				
			if login != "":
				#duplicate login :
				if server_function.checklog(login,"Club") == False:
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
				if server_function.checkEmail(email, "Club") == False :
					email="email valide"
				else:
					email="cet email existe deja, veuillez en choisir un autre"
							
			return jsonify({'clubName':clubName, 'newLogin': login, 'email':email,'noFede':noFede})
			
		#submission :	

		repRegClub=server_function.sign_up_club(request.form['userName'],request.form['city'].capitalize(),request.form['email'],request.form['login'],request.form['pswrd'],request.form['noFederation'])
		print(repRegClub)
		if repRegClub == 0:

			session['username']=request.form['login']
			session['mtype']='Club'
			return redirect( url_for('profileClub',login=session['username']))

		else:
			flash("Erreur d'inscription!") 
			rep=[]
			for i in repRegClub:
				rep.append(i)
				print(rep)
			if rep[0]== True:
				flash(" Login deja existant, veuillez en choisir un autre")
			if rep[1]== True:
				flash(" Numero de federation deja existant, veuillez en choisir un autre")
			if rep[2]== True:
				flash(" Email deja existant, veuillez en choisir un autre")
			if rep[3]== True:
				flash(" Nom de club deja existant, veuillez en choisir un autre")		
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
				if server_function.checklog(login,"Member") == False:
					login="login valide"
				else : 
					login="ce login existe deja , veuillez en choisir un autre"
					
			if len(clubId)==6:
				#validate clubId :
				if server_function.checkClubId(clubId) == True:
					clubId="numero du club valide"
				else : 
					clubId="numero du club invalide, veuillez en entrer un autre"
			elif clubId !="" :
				clubId="veuillez entrer un numero de club a 6 chiffres"
			
			if email != "":
				#validate email:
				if server_function.checkEmail(email,"Member") == False :
					email="email valide"
				else:
					email="cet email existe deja, veuillez en choisir un autre"
							
			return jsonify({'license':license, 'newLogin': login, 'email':email,'clubId':clubId})
			

		#submission :	

		repRegMem=server_function.sign_up_member(request.form['userNo'],request.form['userName'],request.form['userFirstName'],request.form['bday'],request.form['userMail'],request.form['clubId'],request.form['login'],request.form['pswrd'])
		
		if repRegMem == 0:
			session['username']=request.form['login']
			session['mtype']='Member'

			return redirect( url_for('profileMember',login=session['username']))
		else: 
			flash("Erreur d'inscription!") 
			rep=[]
			for i in repRegMem:
				rep.append(i)
				print(rep)
			if rep[0]== True:
				flash(" Licence deja existante, veuillez en choisir un autre")
			if rep[1]== True:
				flash(" Login deja existant, veuillez en choisir un autre")
			if rep[2]== True:
				flash(" Email deja existant, veuillez en choisir un autre")
			if rep[3]== False:
				flash(" Numero du club invalide, veuillez en choisir un autre")
			return redirect(url_for('registerMember'))
	#GET :
	return render_template('registerMember.html')

@app.route('/home/<login>',methods=['GET','POST'])
def home(login): 
	login=session['username']
	if request.method=='POST':
		if request.json:
			nbEvents, events=server_function.getNumberEvent(login,session["mtype"])
			print(nbEvents, events)
			return jsonify({'N' : nbEvents, 'listeEvent' : events})	
	if session['mtype']=='Club':
		clubLogged=True
	else :
		clubLogged=False
	return render_template('home.html',clubLogged=clubLogged)



@app.route('/home/profileClub/<login>',methods = ['GET','POST'])
def profileClub(login): 

	if request.method =='POST' :
		print("POST detected")
		#ajax handler
	 	if request.json:
	 		newL=request.json['newL']
			newE=request.json['newE']
			
			if newL != "":
				#duplicate login :
				if server_function.checklog(newL,"Club") == False:
					newL="login valide"
				else : 
					newL="ce login existe deja , veuillez en choisir un autre"
					
			if newE != "":
				#validate email:
				if server_function.checkEmail(newE, "Club") == False :
					newE="email valide"
				else:
					newE="cet email existe deja, veuillez en choisir un autre"
					
			return jsonify({'newE':newE, 'newL':newL})
			
			
		#modif info
		if request.form ['subBtn'] == 'Enregistrer les modifications': 
			newL=request.form['newLogin']
			newE=request.form['newEmail']
			newP=request.form['newPswrd']

			if newL != "":
				cl=server_function.checklog(newL,"Club")
				if cl ==False : 
					if server_function.updateInfoClub("Connex_Club","login_club",newL,session['username']) == 0:
						session['username']=newL
						flash("Changement de login effectue")
					else : 
						print ("error update")
				else : 
					flash(" Login deja existant, veuillez en choisir un autre")
					
			if newE != "":
				ce=server_function.checkEmail(newE, "Club")
				if ce ==False : 
					if server_function.updateInfoClub("Clubs","email",newE,session['username']) == 0:
						flash("Changement d'email effectue")
					else : 
						print ("error update")
				else : 
					flash(" Email deja existant, veuillez en choisir un autre")
					
			if newP != "":
				pwd=server_function.crypter(newP)
				if server_function.updateInfoClub("Connex_Club","mdp_club",pwd,session['username']) == 0:
					flash("Changement de mot de passe effectue")
				else : 
					print ("error update")
			return redirect(url_for('profileClub',login=session['username'])) 
		
		elif request.form['subBtn'] == 'Creer des Evenements':

			return redirect(url_for('createEvent',loginClub=session['username']))
			
		elif request.form['subBtn'] == 'Ajouter des Licences': 
			return redirect(url_for('addLicense',loginClub=session['username']))
				
		#suivre
		elif request.form['subBtn']=='Suivre':
			
			loginMember= session['username'] 
			licenseNo= server_function.getLicenseFromLogin(loginMember)
			clubId=server_function.getClubId(login)
			server_function.addFollower(licenseNo,clubId[0])
			#clubFollowed = server_function.checkFollowedClub(licenseNo,clubId[0])

			return redirect(url_for('profileClub',login=login))

	else: 
		result = server_function.getClubProfile(login) 

		if session['mtype'] == 'Member':
			clubLogged = False
			licenseNo= server_function.getLicenseFromLogin(session['username'])
			clubId=server_function.getClubId(login)
			clubFollowed = server_function.checkFollowedClub(licenseNo,clubId[0])
		else:
			clubLogged= True 
			clubFollowed=False
			
		nbLicensed= server_function.getNumberOfLicensed(login)
		nbFollo=server_function.getNumberOfFollower(login)
		
		return render_template('profileClub.html',clubName=result[0],clubCity=result[1],clubEmail=result[2],clubNumber=result[3],nbPlayers=nbLicensed,nbFollowers=nbFollo,clubLogin=login,clubLogged=clubLogged,checkFollowedClub=clubFollowed)

	
@app.route('/home/profileMember/<login>',methods=['GET','POST'])
def profileMember(login): 
	login=session['username']
	if request.method == 'POST':
		#ajax handler
		if request.json :
			action=request.json['action']
		
			if action == "getEventFollowed":
				nbEv,Ev=server_function.getEventFollowed(session['username'])
				return jsonify({'nb':nbEv,'events':Ev})
			elif action == "getClubFollowed" :
				nbClub,Clubs=server_function.getClubFollowed(session['username'])
				return jsonify({'nb':nbClub,'clubs':Clubs})
			else : 
				newL=request.json['newL']
				newE=request.json['newE']
			
				if newL != "":
					#duplicate login :
					if server_function.checklog(newL,"Member") == False:
						newL="login valide"
					else : 
						newL="ce login existe deja , veuillez en choisir un autre"
					
				if newE != "":
					#validate email:
					if server_function.checkEmail(newE, "Member") == False :
						newE="email valide"
					else:
						newE="cet email existe deja, veuillez en choisir un autre"
					
				return jsonify({'newE':newE, 'newL':newL})
				
				
		if request.form ['subBtn'] == 'Enregistrer les modifications': 
			newL=request.form['newLogin']
			newE=request.form['newEmail']
			newP=request.form['newPswrd']

			if newL != "":
				cl=server_function.checklog(newL,"Member")
				if cl ==False : 
					if server_function.updateInfoMember("Connex_Membre","login_membre",newL,session['username']) == 0:
						session['username']=newL
						flash("Changement de login effectue")
					else : 
						print ("error update")
				else : 
					flash(" Login deja existant, veuillez en choisir un autre")
					
			if newE != "":
				ce=server_function.checkEmail(newE, "Member")
				if ce ==False : 
					if server_function.updateInfoMember("Membres","email",newE,session['username']) == 0:
						flash("Changement d'email effectue")
					else : 
						print ("error update")
				else : 
					flash(" Email deja existant, veuillez en choisir un autre")
					
			if newP != "":
				pwd=server_function.crypter(newP)
				if server_function.updateInfoMember("Connex_Membre","mdp_membre",pwd,session['username']) == 0:
					flash("Changement de mot de passe effectue")
				else : 
					print ("error update")
			return redirect(url_for('profileMember',login=session['username'])) 		
				
	else : #affichage debut
			#nom, prenom, categorie, club, email 
		result = server_function.getMemberProfile(session['username']) 
		print "RESULT :"
		print result
		if result [0] != False :
			userName=result[0]+" "+result[1]

	return render_template('profileMember.html', userName=userName, userClub=result[2],userDate=result[4],userMail=result[5], userLogin=session['username'],userCat=result[3])

@app.route('/home/profileClub/<loginClub>/addLicense',methods = ['GET','POST'])
def addLicense(loginClub): 
	clubId=server_function.getClubId(loginClub)
	if request.method =='POST' : 
		#ajax handler: 
		if request.json : 
			numero=request.json['num']
			action=request.json['action']
			if action=="chkDupEm":
				email=request.json['email']
				#check si email existe deja dans la table membre
				if server_function.checkEmail(email,"Member")==False:
					dE= "email "+numero+" valide"
				else: 
					dE="email "+numero+" deja existant dans la base de donnee,un compte existe deja"
				return jsonify({'dE':dE})
			elif action == "chkDupLi" : 
				licence=request.json['licence']
				if len(licence)==8 :
					if server_function.checkLicense(licence) == False : 
						dL="licence "+numero+" valide"

					else :
						dL="licence "+numero+" deja existant dans la base de donnee,un compte existe deja"
				elif licence !="":
					dL ="veuillez entrez un numero de licence a 8 chiffres"
								
				return jsonify({'dL':dL})
				
				
		#submission: 	
		if request.form['subBtn'] == "Ajouter les licences":
			return redirect(url_for("profileClub",login=loginClub))
	
	clubLogged=True		
	return render_template('addLicense.html',loginClub=loginClub,clubLogged=clubLogged)



@app.route('/home/search', methods=['GET', 'POST'])
def search (): 

	if request.method == 'POST':
		print('POST recieved') 
			
		if request.json:
			print('JSON recieved')
			stype=request.json['stype']
			print (stype)
			if stype == "club" :
				clubName= request.json['clubName']
				city= request.json['place'].capitalize()
				result=server_function.searchResultClub(clubName,city)
				return jsonify({ 'resSearch' : result, 'searchType' : 'Club' })
			else :
				categorie= request.json['categorie']
				nameEvent= request.json['eventName']
				date= request.json['date']
				#city= request.json['place']
				result=server_function.searchResultEv(categorie,nameEvent,date)
				print(result)
				return jsonify({'resSearch' : result, 'searchType' : 'Event' })
			
			
	if session['mtype'] == 'Club':
		return render_template('search.html', clubLogged=True)
	else:	
		return render_template('search.html')



@app.route('/home/profileClub/<loginClub>/creaEvent', methods=['GET', 'POST'])
def createEvent(loginClub):
	clubId=server_function.getClubId(loginClub)
	#print(clubId)
	if request.method == 'POST': 

		if request.json:
			nameE=request.json['nameE']
			print(nameE)			
			if nameE!="" :
				#duplicate nameE :
				if server_function.checkNameEvent(nameE) == False : 
					nameE="nom d'evenement valide "
				else :
					nameE="ce nom d'evenement existe deja, veuillez en choisir un autre"
				return jsonify({'nameE':nameE})
		
		else :				
		#submission :
			adress=request.form['city'].capitalize()+" "+ request.form['road']
			nameEvent=request.form['nameEvent']
			categorie=request.form['categorie']
			nbPlace=request.form['nbPlace']
			start= request.form['start']
			desc= request.form['desc']
			hour=request.form['hour']
			imageLink="http://www.google.fr/"
		
			if server_function.checkNameEvent(nameEvent) == True : 
				flash("Erreur de creation d'evenements : le nom de l'evenement existe deja, veuillez en choisir un autre")
				return redirect(url_for("createEvent",loginClub=session['username']))
			else : 
				if server_function.createEvent(nameEvent,categorie,nbPlace,desc,adress,start,hour,clubId[0],imageLink)==1: 
					print("SUCCESS !" )
					return redirect(url_for('profileEvent',eventName=nameEvent.replace(" ","_")))
				else: 
					print("error on event creation")
					return redirect(url_for('createEvent',loginClub=session['username']))

	clubLogged=True	
	return render_template('createEvent.html',clubLogged=clubLogged)

@app.route('/profileEvent/<eventName>',methods=['GET','POST'])
def profileEvent(eventName):
	nomEv= eventName.replace("_"," ") #On remplace les _ par des espaces 
			
	if request.method == 'POST' :
		if request.form['subBtn'] == 'Retourner sur son profil':
			return redirect(url_for('profileClub',login=session['username']))
		elif request.form['subBtn']== "S'inscrire":
			license= server_function.getLicenseFromLogin(session['username'])
			server_function.registerEvent(license,nomEv)
			place=server_function.updateAvailablePlace(nomEv);
			print(place) 
			return redirect(url_for('profileEvent',eventName=eventName))
	
	else :
		result = server_function.getEvent(nomEv)
		if session['mtype']=='Member':
			license= server_function.getLicenseFromLogin(session['username'])
			alreadyRegistered= server_function.checkFollowedEvent(license,nomEv)
			clubLogged=False
		else: 
			alreadyRegistered=False
			clubLogged=True
	
		return render_template("profileEvent.html",eventName=nomEv,image=result[8],descEvent=result[7],cityEvent=result[6],dateEvent=result[2],startHour=result[3],categorie=result[1],nbPlaceStillAvailable=result[4],clubLogged=clubLogged,alreadyRegistered=alreadyRegistered) #AAAAA VOIR 

@app.route('/about')
def about():
	return render_template('about.html')
# ............................................................................................... #
#lancement appli
if __name__ == '__main__':
	app.run(debug=True)

# ............................................................................................... #
