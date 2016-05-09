# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import os, hashlib
import sqlite3 
import sys 

reload(sys) 
sys.setdefaultencoding('utf8')

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
		print("INSERT ERROR in %s",table) 
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
		row = db.execute('SELECT license FROM Membres WHERE license=:who', {"who": license}).fetchone()
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
	if mtype == "member":#member
		
		try: 
			row = db.execute('SELECT login_membre,mdp_membre FROM Connex_Membre WHERE login_membre=:who AND mdp_membre=:pass',{"who": login, "pass": password}).fetchone()
			if row is not None: 
				return True
			else: 
				return False 
		except: 
			print("sigin error")
		finally: 
			db.close()
	else :#club
	 
		try: 
			row = db.execute('SELECT login_club,mdp_club FROM Connex_Club WHERE login_club=:who AND mdp_club=:pass',{"who": login, "pass": password}).fetchone()
			if row is not None: 
				return True
			else: 
				return False 
		except: 
			print("signin error")
		finally: 
			db.close()

#Retourne True si l'ajout est un succes, False si il y a eu une erreur et False si l'id du club existe		
def sign_up_club(clubName,city,email,login,password,clubId):
	
	try: 
		if (checklog(login,"club")==False) and  (checkClubId(clubId)==False) and (checkEmail(email, "club")==False) and (checkClubName(clubName)==False): 
			insert("Clubs",("club_id","nom_club","ville","email"),(clubId,clubName,city,email)) 
			insert("Connex_Club",("login_club","mdp_club","club_id"),(login,password,clubId))
<<<<<<< HEAD
			return 0 
		else: 
			print("THE ID OF THIS CLUB IS REGISTERED") 
			return 1
=======
			return True 
		else:  
			return False
>>>>>>> a1758e00211f890feda2353f180afa216dd806da
	except: 
		print("CLUB SIGNUP error")
		return  False 
	finally: 
		print("End signup CLUB")



#Retourne True si l'ajout est un succes, FAlse si il y a eu une erreur et False si l'id du membre existe			
def sign_up_member(licenseNo, userName,userFirstName,bday,userMail,clubId,login,pswrd):

	try: 
	
		if (checkLicense(licenseNo) == False) and (checklog(login,"member")==False) and (checkEmail(userMail,"member")==False):  
		
			if checkClubId(clubId) == True: #le clubID existe 
				insert("Membres",("license","nom","prenom","date_n","email","club_id"),(licenseNo,userName,userFirstName,bday,userMail,clubId)) 
				insert("Suivis",("license", "club_id"),(licenseNo, clubId))
			else: #le club n'existe pas
				insert("Membres",("license","nom","prenom","date_n","email","club_id"),(licenseNo,userName,userFirstName,bday,userMail,0)) 
					
			#si pas de redondance on peut inserer login et mot de passe		
			insert("Connex_Membre",("login_membre","mdp_membre","license"),(login,pswrd,licenseNo))
			return True		
		else: 
			print("LICENSE OR LOGIN OR EMAIL ALREADY EXISTS") 
			return False 
	
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
		row= c.execute('SELECT nom_club, ville, email FROM Clubs AS c, Connex_Club AS cc WHERE c.club_id = cc.club_id AND cc.login_club=:who',{"who":login}).fetchone()
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
	c=db.cursor()
	try: 
		row= c.execute('SELECT m.nom, m.prenom, ca.categorie, c.nom_club, m.email, m.date_n FROM Membres AS m, Categories AS ca, Clubs AS c, Connex_Membre AS mc WHERE m.licence=ca.licence AND m.club_id=c.club_id AND m.licence=mc.licence AND mc.login_membre:=who',{"who":login}).fetchone()
		if row is not None:
			print(row) 
			return row
		else: 
			return "" 
	except: 
		print("Problem with the login in database Search ")
	finally: 
		db.close()

