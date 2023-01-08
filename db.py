import sqlite3
import random

def insert(text: str):
	conn = sqlite3.connect('DataBase.db')
	cursor = conn.cursor()
	row = cursor.execute(text)
	conn.commit()
	return row

def fetch(text: str):
	conn = sqlite3.connect('DataBase.db')
	cursor = conn.cursor()
	row = cursor.execute(text)
	fetch_info = row.fetchall()
	conn.commit()
	cursor.close()
	conn.close()
	return fetch_info

def random_logins():
	for j in range(0, 100):
		login = ''
		password = ''
		for i in range(6):
			login += f'{chr(random.randint(48, 122))}'
		for i in range(8):
			password += f'{chr(random.randint(35, 122))}'
		print(login, password)
		insert(f'INSERT INTO Auth_data VALUES ("{login}", "{password}")')
