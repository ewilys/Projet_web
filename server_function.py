# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import os, hashlib
import sqlite3 
import sys 

reload(sys) 
sys.setdefaultencoding('utf8')

def crypter(pswrd): 
	mdp=pswrd.encode()
	return hashlib.sha1(mdp).hexdigest()    

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

def checklog (login, mtype):
	db= sqlite3.connect('dtb.db')
	if mtype == "member":#member
	
		try: 
			row = db.execute('SELECT login_membre FROM Connex_Membre WHERE login_membre=:who', {"who": login}).fetchone()
			if row is None: 
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
				return False
			else :
				return True
		except: 
			print("login error")
		finally: 
			db.close()
	
def checkLicense (license):
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT licence FROM Membres WHERE licence=:who', {"who": license}).fetchone()
		if row is None: 
			return False
		else :
			return True
	except: 
		print("login error")
	finally: 
		db.close()

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
		
def checkEmail(email, mtype):
	db= sqlite3.connect('dtb.db')
	if mtype=="member" :
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
	pwd=password.encode()
	if mtype == "member":#member
		
		try: 
			row = db.execute('SELECT login_membre,mdp_membre FROM Connex_Membre WHERE login_membre=:who AND mdp_membre=:pass',{"who": login, "pass": pwd}).fetchone()
			if row is not None: 
				return True, True
			else: 
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

	cl=checklog(login,"club")
	ci=checkClubId(clubId)
	ce=checkEmail(email, "club")
	cn=checkClubName(clubName)

	pwd=password.encode()

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
	clo=checklog(login,"member")
	ce=checkEmail(userMail,"member")
	cc=checkClubId(clubId)

	pwd=pswrd.encode()

	try: 
	
		if ( cli == False) and (clo==False) and (ce==False):  
		

			if cc == True : #le clubID existe 

				insert("Membres",("licence","nom","prenom","date_n","email","club_id"),(licenseNo,userName,userFirstName,bday,userMail,clubId)) 
				insert("Suivis",("licence", "club_id"),(licenseNo, clubId))
			else: #le club n'existe pas
				insert("Membres",("licence","nom","prenom","date_n","email","club_id"),(licenseNo,userName,userFirstName,bday,userMail,0)) 
					
			#si pas de redondance on peut inserer login et mot de passe		

			insert("Connex_Membre",("login_membre","mdp_membre","licence"),(login,pwd,licenseNo))
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
def getMemberProfile(login): 
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT m.nom,m.prenom,c.nom_club, m.date_n, m.email FROM Membres AS m, Connex_Membre AS cm, Clubs AS c WHERE m.club_id=c.club_id AND m.licence=cm.licence AND cm.login_membre=:who', {"who": login}).fetchone()
		if row is None: 
			return False
		else :
			return row
	except: 
		print("error in getting member profile")
	finally: 
		db.close()



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


#recupere les clubs suivis pour un login
def getClubFollowed(login):

	db=sqlite3.connect('dtb.db')
	c=db.cursor()	
	try: 
		row = c.execute('SELECT s.club_id, c.nom_club FROM Clubs AS c,Suivis AS s, Connex_Membre AS cm WHERE s.licence=cm.licence AND s.club_id=c.club_id AND cm.login_membre=:who ',{"who":login}).fetchall()
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
			
		
#recupere les evenements auquel un login est inscrit			
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



def getNumberEvent(login,mtype):
	db=sqlite3.connect('dtb.db')
	print(login)
	c=db.cursor()	
	club_id=[]
	events=[]
	if mtype == "member":
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
	


def getEventForLogin(club_id,mtype):
	db=sqlite3.connect('dtb.db')
	c=db.cursor()	
	club_id=''.join(club_id)
	if mtype == "member":
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
		print("LICENSE = "+license)
		print("CLUBID = "+clubId)
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

def checkFollowedClub (license,clubId): 
	db= sqlite3.connect('dtb.db')
	try: 
		print("LICENSE CHECK = "+str(license))
		print("CLUBID CHECK = "+str(clubId))
		row = db.execute("SELECT * FROM Suivis WHERE club_id=:idClub AND licence=:licenceNo",{"idClub":clubId,"licenceNo":license}).fetchone()
		if row is None: 
			return False
		else: 
			return True  #deja associe
		
	except: 
		print("Problem with checkFollowedClub")
	finally: 
		db.close()

def addLicenseClub(license,clubId): 
	pass







