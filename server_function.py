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
		row = db.execute('SELECT license FROM Connex_Membre WHERE license=:who', {"who": license}).fetchone()
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
		row = db.execute('SELECT club_id FROM Connex_Club WHERE club_id=:who', {"who": clubId}).fetchone()
		if row is None: 
			return False
		else :
			return True
	except: 
		print("login error")
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

#Retourne 0 si l'ajout est un succes, -1 si il y a eu une erreur et 1 si l'id du club existe		
def sign_up_club(clubName,city,email,login,password,clubId):
	print("je passe ici")
	try: 
		if (checklog(login,"club")==False) and  (checkClubId(clubId)==False) : 
			insert("Clubs",("club_id","nom_club","ville","email"),(clubId,clubName,city,email)) 
			insert("Connex_Club",("login_club","mdp_club","club_id"),(login,password,clubId))
			return 0 
		else: 
			print("THE ID OF THIS CLUB IS REGISTERED") 
			return 1
	except: 
		print("CLUB SIGNUP error")
		return  -1 
	finally: 
		print("End signup CLUB")

#Retourne 0 si l'ajout est un succes, -1 si il y a eu une erreur et 1 si l'id du membre existe			
def sign_up_member(licenseNo, userName,userFirstName,bday,userMail,clubId,login,pswrd):
	try: 
		if (checkLicense(licenseNo) == False) and (checklog(login,"member")==False):  #checker redondance email (lisa s'en charge)
			if clubId: #le clubID existe (a tester lisa s'en charge!)
				insert("Membres",("license","nom","prenom","date_n","email","club_id"),(licenseNo,userName,userFirstName,bday,userMail,clubId)) 
			else: 
				insert("Membres",("license","nom","prenom","date_n","email","club_id"),(licenseNo,userName,userFirstName,bday,userMail,0)) 	
			#si pas de redondance on peut inserer login et mot de passe		
			insert("Connex_Membre",("login_membre","mdp_membre","license"),(login,pswrd,licenseNo))
			return 0		
		else: 
			print("LICENSE OR LOGIN ALREADY EXISTS") 
			return 1 
	
	except: 
		print("MEMBER SIGNUP error")
		return -1 
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

