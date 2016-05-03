# ............................................................................................... #

from flask  import *
from sqlalchemy import *
import os, hashlib
import sqlite3 
import sys 

reload(sys) 
sys.setdefaultencoding('utf8')

def sign_in (login, password):
	db= sqlite3.connect('dtb.db')
	c=db.cursor()
	try: 
		row = c.fetchone()
		c.execute('SELECT login,mdp FROM membre_connex WHERE login=:who AND mdp=:pass', {"who": login, "pass": password})
		if row is not None: 
			return True
		else: 
			return False 
	except: 
		print("login error")
	finally: 
		db.close()
		
def sign_up_member ():
	pass
