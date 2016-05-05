# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import os, hashlib
import sqlite3 
import sys 

reload(sys) 
sys.setdefaultencoding('utf8')

def insert(table, fields=(), values=()):
	print("Je passe dans al fonction")
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
		print("INSERT ERROR") 
	finally: 
		db.close()

#Returns True if login and password are correct and exist in database, False if not
def sign_in (login, password):
	db= sqlite3.connect('dtb.db')
	try: 
		row = db.execute('SELECT login_membre,mdp_membre FROM Connex_Membre WHERE login_membre=:who AND mdp_membre=:pass', {"who": login, "pass": password}).fetchone()
		if row is not None: 
			return True
		else: 
			return False 
	except: 
		print("login error")
	finally: 
		db.close()

		
def sign_up_club (clubName,city,email,login,password,clubId):
	insert("Clubs",("club_id","nom_club","ville","email"),(clubId,clubName,city,email)) 
	insert("Connex_Club",("login_club","mdp_club","club_id"),(login,password,clubId))
	try: 
		print("")
	except: 
		print("SIGNUP error")
	finally: 
		print("End signup")
		
def sign_up_member(): 
	pass 

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
		print("login error")
	finally: 
		db.close()


