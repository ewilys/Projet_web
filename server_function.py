# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import os, hashlib
import sqlite3 
import sys 
import time

reload(sys) 
sys.setdefaultencoding('utf8')

#cryptage des mdp
def crypter(pswrd): 
	mdp=pswrd.encode()
	return hashlib.sha1(mdp).hexdigest()    
	
	
#insertion des champs dans les differentes tables
def insert(table, fields=(), values=()):
	db = sqlite3.connect('dtb.db')
	#cur = db.cursor()

	query = 'INSERT INTO %s (%s) VALUES (%s)' % (
		table,
		', '.join(fields),
		', '.join(['?'] * len(values))

	)
	try: 
		db.execute(query, values)
		db.commit()
	except: 
		print("INSERT ERROR in ",table) 
	finally: 
		db.close()

#verifie si login est unique , return False si n'existe pas, true si deja dans base
def checklog (login, mtype):
	db= sqlite3.connect('dtb.db')
	if mtype == "Member":#member
	
		try: 
			row = db.execute('SELECT login_membre FROM Connex_Membre WHERE login_membre=:who', {"who": login}).fetchone()
			if row is None: 
				print("JE PASSE ICI MTYPE = "+mtype) 
				return False
			else :
				return True
		except: 
			print("login error")
		finally: 
			db.close()
	else : #club
		try: 
			row = db.execute('SELECT login_club FROM Connex_Club WHERE login_club=:who', {"who": login}).fetchone()
			if row is None: 
				print("JE PASSE ICI MTYPE = "+mtype) 
				return False
			else :
				return True
		except: 
			print("login error")
		finally: 
			db.close()
			
			
#verifie unicicte licence, return False si licence n'existe pas, True si existe	
def checkLicense (license):
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT licence,nom FROM Membres WHERE licence=:who', {"who": license}).fetchone()
		if row is None: 
			return False
		else :
			if row[1] is None: 
				return False 
			else: 
				return True
	except: 
		print("login error")
	finally: 
		db.close()

#verifie unicite clubId, return False si clubid n'existe pas, True si existe (attention gestion differente pour le coup)
def checkClubId (clubId): 
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT club_id FROM Clubs WHERE club_id=:who', {"who": clubId}).fetchone()
		if row is None: 
			return False
		else :
			return True
	except: 
		print("clubId error")
	finally: 
		db.close()
		
#recupere le clubId	, pour un login	
def getClubId(login):
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT club_id FROM Connex_Club WHERE login_club=:who', {"who": login}).fetchone()
		if row is not None: 
			return row
		else :
			return ""
	except: 
		print("clubId error")
	finally: 
		db.close()
		
		
#verifie unicite clubName, return False si nom n'existe pas, True si existe
def checkClubName (clubName): 
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT nom_club FROM Clubs WHERE nom_club=:who', {"who": clubName}).fetchone()
		if row is None: 
			return False
		else :
			return True
	except: 
		print("clubName error")
	finally: 
		db.close()

#verifie unicite nameEvent, return False si nom n'existe pas, True si existe
def checkNameEvent (nameE): 
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT nom_ev FROM Evenements WHERE nom_ev=:who', {"who": nameE}).fetchone()
		if row is None: 
			return False
		else :
			return True
	except: 
		print("nameEvent error")
	finally: 
		db.close()	
		
				
#verifie email , return False si email n'existe pas , True si existe	
def checkEmail(email, mtype):
	db= sqlite3.connect('dtb.db')
	if mtype=="Member" :
		try: 
			row = db.execute('SELECT email FROM Membres WHERE email=:which', {"which": email}).fetchone()
			if row is None: 
				return False
			else :
				return True
		except: 
			print("email member error")
		finally: 
			db.close()
	else : #club
		try: 
			row = db.execute('SELECT email FROM Clubs WHERE email=:which', {"which": email}).fetchone()
			if row is None: 
				return False
			else :
				return True
		except: 
			print("email club error")
		finally: 
			db.close()
		
		
#Returns True if login and password are correct and exist in database, False if not
def sign_in (login, password, mtype):
	db= sqlite3.connect('dtb.db')
	pwd=crypter(password)
	if mtype == "Member":#member
		
		try: 
			row = db.execute('SELECT login_membre,mdp_membre FROM Connex_Membre WHERE login_membre=:who AND mdp_membre=:pass',{"who": login, "pass": pwd}).fetchone()
			if row is not None: 
				return True, True
			else: 
				print("MTYPE = "+mtype)
				repLog=checklog(login, mtype);
				return False, repLog
		except: 
			print("sigin error")
		finally: 
			db.close()
	else :#club
	 
		try: 
			row = db.execute('SELECT login_club,mdp_club FROM Connex_Club WHERE login_club=:who AND mdp_club=:pass',{"who": login, "pass": pwd}).fetchone()
			if row is not None: 
				return True, True
			else: 
				repLog=checklog(login, mtype);
				return False , repLog
		except: 
			print("signin error")
		finally: 
			db.close()


#Retourne 0 si l'ajout est un succes, res des requetes si une des exigences n'est pas respectee et -1 si erreur	
def sign_up_club(clubName,city,email,login,password,clubId):

	cl=checklog(login,"Club")
	ci=checkClubId(clubId)
	ce=checkEmail(email, "Club")
	cn=checkClubName(clubName)

	pwd=crypter(password)

	try: 
		if (cl==False) and  (ci==False) and (ce==False) and (cn==False): 
			insert("Clubs",("club_id","nom_club","ville","email"),(clubId,clubName,city,email)) 
			insert("Connex_Club",("login_club","mdp_club","club_id"),(login,pwd,clubId))
			return 0
		else:  
			return cl, ci, ce, cn
	except: 
		print("CLUB SIGNUP error")
		return  -1 
	finally: 
		print("End signup CLUB")



#Retourne True si l'ajout est un succes, FAlse si il y a eu une erreur et False si l'id du membre existe			
def sign_up_member(licenseNo, userName,userFirstName,bday,userMail,clubId,login,pswrd):

	cli=checkLicense(licenseNo)
	clo=checklog(login,"Member")
	ce=checkEmail(userMail,"Member")
	cc=checkClubId(clubId)

	pwd=crypter(pswrd)

	try: 
	
		if ( cli == False) and (clo==False) and (ce==False):  
		

			if cc == True : #le clubID existe 

				insert("Membres",("licence","nom","prenom","date_n","email","club_id"),(licenseNo,userName,userFirstName,bday,userMail,clubId)) 
				insert("Suivis",("licence", "club_id"),(licenseNo, clubId))
			else: #le club n'existe pas
				insert("Membres",("licence","nom","prenom","date_n","email","club_id"),(licenseNo,userName,userFirstName,bday,userMail,0)) 
					
			#si pas de redondance on peut inserer login et mot de passe		

			insert("Connex_Membre",("login_membre","mdp_membre","licence"),(login,pwd,licenseNo))
			cat=CategorieMember(bday)
			print(cat)
			insert("Categories",("licence","categorie"),(licenseNo,cat))
			return 0		

		else: 
			print("LICENSE OR LOGIN OR EMAIL ALREADY EXISTS") 
			return cli,clo,ce,cc 
	
	except: 
		print("MEMBER SIGNUP error")
		return False 
	finally: 
		print("End signup MEMBER")
	
	
	
#Returns the tuple associated to the profile of a club with all the Datas
def getClubProfile(login): 
	db= sqlite3.connect('dtb.db')
	c=db.cursor()
	try: 
		print(login)
		row= c.execute('SELECT nom_club, ville, email, c.club_id FROM Clubs AS c, Connex_Club AS cc WHERE c.club_id = cc.club_id AND cc.login_club=:who',{"who":login}).fetchone()
		if row is not None:
			print(row) 
			return row
		else: 
			return "" 
	except: 
		print("problem with the login in database search")
	finally: 
		db.close()

#Returns the tuple associated to the profile of a member with all the datas. 
#Returns the tuple associated to the profile of a member with all the datas. 
def getMemberProfile(login): 
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT m.nom,m.prenom,c.nom_club,ca.categorie, m.date_n, m.email FROM Membres AS m, Categories AS ca,Connex_Membre AS cm, Clubs AS c WHERE m.club_id=c.club_id AND ca.licence=m.licence AND m.licence=cm.licence AND cm.login_membre=:who', {"who": login}).fetchone()
		if row is None: 
			return False
		else :
			return row
		print row
	except: 
		print("error in getting member profile")
	finally: 
		db.close()


#creation d'un evenement
def createEvent(nameEvent,categorie,nbPlace,desc,adress,start,hour,clubId,imageLink): 
	db=sqlite3.connect('dtb.db')
	try: 
		insert("Evenements",("nom_ev","club_id","categorie","date_e","heure_e","nb_places","etat","adresse","description","lien_image"),(nameEvent,clubId,categorie,start,hour,nbPlace,"open",adress,desc,imageLink))
		return 1
	except: 
		print("Could not insert Event in database ....")
		return -1 
	finally: 
		db.close()

#recupere info event pour le profile Event
def getEvent(eventName):
	db=sqlite3.connect('dtb.db')
	try: 
		row = db.execute("SELECT club_id,categorie,date_e,heure_e,nb_places, etat, adresse,description,lien_image FROM Evenements WHERE nom_ev=:eventName",{"eventName":eventName}).fetchone()
		if row is not None: 
			#print(row) #debug
			return row
		else: 
			return "" 
	except: 
		print("exception in getEvent")
	finally: 
		db.close()


#recupere nb club et clubs suivis pour un login
def getClubFollowed(login):

	db=sqlite3.connect('dtb.db')
	c=db.cursor()	
	try: 
		row = c.execute('SELECT cc.login_club, c.nom_club, c.ville FROM Clubs AS c, Suivis AS s, Connex_Club AS cc, Connex_Membre AS cm WHERE cc.club_id=c.club_id AND s.licence=cm.licence AND s.club_id=c.club_id AND cm.login_membre=:who ',{"who":login}).fetchall()
		if row is not None: 
			#print(row)
			#for i in row:
			#	print(i,"".join(i[0]),"".join(i[1]))
				
			return len(row),row
		else: 
			return 0
	except: 
		print("exception in seeking club_id followed")
	finally: 
		db.close()
			
		
#recupere nb event et evenements auquel un login est inscrit			
def getEventFollowed(login):
	db=sqlite3.connect('dtb.db')
	c=db.cursor()	
	try: 
		row = c.execute('SELECT e.nom_ev, e.date_e, e.heure_e, e.adresse FROM Evenements AS e, Inscriptions AS i, Connex_Membre AS cm WHERE i.licence=cm.licence AND i.nom_ev=e.nom_ev AND cm.login_membre=:who ',{"who":login}).fetchall()
		if row is not None: 
			print(row)
			return len(row),row
		else: 
			return 0
	except: 
		print("exception in seeking event followed")
	finally: 
		db.close()


#recupere nb event et events des clubs suivis si sportif ou tous les events si club 
def getNumberEvent(login,mtype):
	db=sqlite3.connect('dtb.db')
	print(login)
	c=db.cursor()	
	club_id=[]
	events=[]
	if mtype == "Member":
		try: 
			row = c.execute('SELECT club_id FROM Suivis AS s, Connex_Membre AS cm WHERE s.licence=cm.licence AND cm.login_membre=:who ',{"who":login}).fetchall()
			if row is not None: 
				#print(row) #debug
				for i in row:
					club_id.append(i)
			else: 
				club_id.append("none")
			#print(club_id)
		
		except: 
			print("exception in seeking club_id")
		finally: 
			if club_id[0]!="none":
				for i in range (len(club_id)):
					print(club_id[i])
					row=getEventForLogin(club_id[i],mtype)
					for a in row:
						events.append(a)
						
				#print(events)
				return len(events),events
				
			else:
				print("no club followed")
				return 0
			db.close()
	else: #club
		try:
			row = c.execute('SELECT club_id FROM Connex_Club WHERE login_club=:who',{"who":login}).fetchone()
			if row is not None: 
				print(row) #debug
				row=getEventForLogin(row,mtype)
				for a in row:
						events.append(a)
				return len(events),events	
			else:
				print("no club for this login")
				return 0
		
		except: 
			print("exception in getting events information")
		finally: 
			print("get information associated to event for this login") 
			db.close()
	

#renvoi tous les events pour un club_id suivant le mtype 
def getEventForLogin(club_id,mtype):
	db=sqlite3.connect('dtb.db')
	c=db.cursor()	
	club_id=''.join(club_id)
	if mtype == "Member":
		try:
			row = c.execute('SELECT e.nom_ev,c.nom_club,e.categorie,e.date_e,e.heure_e FROM Evenements AS e, Clubs AS c WHERE c.club_id=e.club_id AND e.club_id=:which',{"which":club_id}).fetchall()
			if row is not None: 
				#print(row) #debug
				return row
			else:
				print("no event for this club")
		
		except: 
			print("exception in getting events information")
		finally: 
			print("get information associated to event for this login") 
			db.close()
			
			
	else :#club 
		try:
			row = c.execute('SELECT e.nom_ev,e.categorie,e.date_e,e.heure_e FROM Evenements AS e WHERE e.club_id=:which',{"which":club_id}).fetchall()
			if row is not None: 
				#print(row) #debug
				return row
			else:
				print("no event for this club")
		
		except: 
			print("exception in getting events information")
		finally: 
			print("get information associated to event for this login") 
			db.close()

#recupere licence associe a login
def getLicenseFromLogin (login):
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT licence FROM Connex_Membre WHERE login_membre=:who', {"who": login}).fetchone()
		if row is None: 
			return 0
		else :
			return row[0]
	except: 
		print("error on getting license from login")
	finally: 
		db.close()

#Returns 0 if license already associated to club, 1 if follower successfully added and -1 if error 
def addFollower(license,clubId): 
	db=sqlite3.connect('dtb.db')
	try: 
		#print("LICENSE = "+license)
		#print("CLUBID = "+clubId)
		if checkFollowedClub(license,clubId)==False: 
			insert("suivis",("licence","club_id"),(license,clubId))
		else: 
			print("CLUB DEJA SUIVI !!")
			return 0
		return 1
	except: 
		print("Could not insert follower in database ....")
		return -1 
	finally: 
		db.close()

#retourne vrai si le licencie suit deja le club 
def checkFollowedClub (license,clubId): 
	db= sqlite3.connect('dtb.db')
	print("License = "+license)
	print("Ceci est le clubid"+str(clubId))
	try: 
		#print("LICENSE CHECK = "+str(license))
		#print("CLUBID CHECK = "+str(clubId))
		row = db.execute("SELECT * FROM Suivis WHERE club_id=:idClub AND licence=:licenceNo",{"idClub":clubId,"licenceNo":license}).fetchone()
		print(row)
		if row is None: 
			return False
		else: 
			return True  #deja associe
		
	except: 
		print("Problem with checkFollowedClub")
	finally: 
		db.close()

#ajout licence par club 
def addLicenseClub(license,clubId): 
	pass

#recupere le nombre de licencie associe a un club
def getNumberOfLicensed(loginClub):
	clubId= getClubId(loginClub)
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute("SELECT club_id FROM Membres WHERE club_id=:id",{"id":clubId[0]}).fetchall()
		#print("LOGIN CLUB___________________ = "+clubId[0])
		a=len(row)
		print(a)
		return len(row)
		
	except: 
		print("Problem with getNumberOfLicensed")
	finally: 
		db.close()

#recupere le nombre de personnes suivant un club
def getNumberOfFollower(loginClub):
	clubId= getClubId(loginClub)
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute("SELECT licence FROM Suivis WHERE club_id=:id",{"id":clubId[0]}).fetchall()
		return len(row)
		
	except: 
		print("Problem with getNumberOffollower")
	finally: 
		db.close()
		
#calcul categorie pour les sportifs		
def CategorieMember(bday): 
	today=time.strftime('%y',time.localtime())
	print(today)
	today_year=int("20"+today)
	a=bday[:4]	
	cat=today_year-int(a)
	if cat<10:
		 return "poussin"	
	elif 10<=cat<=18:
		return "ado"
	elif 18<cat<=25:
		return "jeune"
	else:
		return "senior"



#update les info du club	
def updateInfoClub(table,fields,values,login):
	clubId=getClubId(login)
	db = sqlite3.connect('dtb.db')
	#cur = db.cursor()

	query = 'UPDATE %s SET %s = "%s" WHERE club_id= "%s"' % (table,fields,values,"".join(clubId))
	print (query)
	try: 
		db.execute(query)
		db.commit()
		return 0
	except: 
		print("UPDAT ERROR in ",table) 
	finally: 
		db.close()
		
		
#update les info du membre	
def updateInfoMember(table,fields,values,login):
	licence=getLicenseFromLogin(login)
	db = sqlite3.connect('dtb.db')
	#cur = db.cursor()

	query = 'UPDATE %s SET %s = "%s" WHERE licence= "%s"' % (table,fields,values,"".join(licence))
	print (query)
	try: 
		db.execute(query)
		db.commit()
		return 0
	except: 
		print("UPDAT ERROR in ",table) 
	finally: 
		db.close()	


def registerEvent(license,nomEv): 
	print("LICENSE = "+license)
	print("NOMEV = "+nomEv)
	if checkFollowedEvent(license,nomEv)==True: 
		print("DEJA ASSOCIE")
	else: 
		print("inscriptions")
		insert("Inscriptions",("licence","nom_ev"),(license,nomEv))



#On retourne vrai si le membre est deja inscrit a l'event.
def checkFollowedEvent (license,nomEv): 
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute("SELECT * FROM Inscriptions WHERE licence=:licence AND nom_ev=:nom_ev",{"licence":license,"nom_ev":nomEv}).fetchone()
		if row is None: 
			return False
		else: 
			return True  #deja associe
		
	except: 
		print("Problem with checkFollowedClub")
	finally: 
		db.close()
	
	
def searchResultEv (categorie,nameEvent,date):
	db= sqlite3.connect('dtb.db')
	
		
	try: 
		if nameEvent !="": 
			row= db.execute("SELECT nom_ev,adresse FROM Evenements WHERE nom_ev=:nameEvent",{"nameEvent":nameEvent}).fetchall()
		#elif city != "":
			#row = db.execute("SELECT nom_ev,adresse FROM Evenements WHERE adresse=:city",{"city":city}).fetchall()
		elif date != "": 
			row= db.execute("SELECT nom_ev,adresse FROM Evenements WHERE date_e=:date",{"date":date}).fetchall()
		elif categorie !="": 
			row= db.execute("SELECT nom_ev,adresse FROM Evenements WHERE categorie=:categorie",{"categorie":categorie}).fetchall()
		else: 
			return -1 
		
		print(row)
		return row
	except: 
		print("Problem with searchResult")
	finally: 
		db.close()
	
def searchResultClub (clubName,city):
	db= sqlite3.connect('dtb.db')
	
	try: 
		if clubName != "" and city !="": 
			row = db.execute("SELECT nom_club, ville, login_club FROM Clubs AS c, Connex_Club AS cc WHERE c.club_id=cc.club_id AND nom_club=:nom_club AND ville=:ville",{"nom_club":clubName,"ville":city}).fetchall()
		elif city != "":
			row = db.execute("SELECT nom_club, ville, login_club FROM Clubs AS c, Connex_Club AS cc WHERE c.club_id=cc.club_id AND ville=:city",{"city":city}).fetchall()
		elif clubName != "":
			row = db.execute("SELECT nom_club, ville, login_club FROM Clubs AS c, Connex_Club AS cc WHERE c.club_id=cc.club_id AND nom_club=:nom_club ",{"nom_club":clubName}).fetchall()	
		else: 
			return -1 
		if row ==[] :
			row=[("null",)]	
		print(row)
		return row
	except: 
		print("Problem with searchResult")
	finally: 
		db.close()
		
def updateAvailablePlace(nomEv): 
	db= sqlite3.connect('dtb.db')
	try: 
		nbPlace = db.execute("SELECT nb_places FROM Evenements WHERE nom_ev=:nomEv",{"nomEv":nomEv}).fetchone()
		print("NOMBRE DE PLACES= "+nbPlace[0])
		Place = int(nbPlace[0])-1
		newNbPlace = str(Place)
		print("NEW NB PLACE = "+newNbPlace)
		db.execute('UPDATE Evenements SET %s = "%s" WHERE nom_ev= "%s"' % ("nb_places",newNbPlace,nomEv))
		db.commit()
		row =db.execute("SELECT nb_places FROM Evenements WHERE nom_ev=:nomEv",{"nomEv":nomEv}).fetchone()
		print row[0]
		if row[0] == "0":
			db.execute('UPDATE Evenements SET %s = "%s" WHERE nom_ev= "%s"' % ("etat","close",nomEv))
			db.commit()
		return row[0]
		
	except: 
		print("Problem with updateAvailablePlace")
	finally: 
		db.close()
