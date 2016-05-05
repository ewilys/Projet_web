# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import os, hashlib
import sqlite3 
import sys 

reload(sys) 
sys.setdefaultencoding('utf8')

def insert(table, fields=(), values=()):
	# g.db is the database connection
	db=sqlite3.connect('dtb.sql')
	cur = db.cursor()
	query = 'INSERT INTO %s (%s) VALUES (%s)' % (
		table,
		', '.join(fields),
		', '.join(['?'] * len(values))
		)
	cur.execute(query, values)
	db.commit()
	id = cur.lastrowid
	cur.close()
	return id


def checklog (login):
	db= sqlite3.connect('dtb.db')
	
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
	
	
		
#Returns True if login and password are correct and exist in database, False if not
def sign_in (login, password):
	db= sqlite3.connect('dtb.db')
	c=db.cursor()
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
	db= sqlite3.connect('dtb.db')
	#c=db.cursor()
	try: 
		insert(clubs,(club_id,nom_club,ville,email),(clubId,clubName,city,email))
		insert(Connex_Club,(login_club,mdp_club,club_id),(login,password,clubId))
		#row = c.fetchone()
		#c.execute('INSERT INTO clubs (club_id, nom_club, ville, email) VALUES (club_id:=clubId, nom_club:=clubName, ville:=city,email:=email)',{"clubName":clubName, "city":city, "email":email})
		#c.execute('INSERT INTO Connex_Club (login_club,mdp_club,club_id) VALUES (login_club:=login, mdp_club:= password, club_id:=clubId)',{"login":login,"password":password,"clubId":clubId})
	except: 
		print("login error")
	finally: 
		db.close()
		

#Returns the tuple associated to the profile of a club with all the Datas
def getClubProfile(login): 
	db= sqlite3.connect('dtb.db')
	c=db.cursor()
	try: 
		row = c.fetchone()
		c.execute('SELECT nom, ville, email FROM clubs AS c, club_connex AS cc WHERE c.club_id = cc.club_id AND cc.login=:who',{"who":login})
		if row is not None:
			print(row) 
			return row
		else: 
			return "" 
	except: 
		print("login error")
	finally: 
		db.close()


