import sqlite3
import db

with open('order236637.txt', 'r') as file:
	raws = file.readlines()
	for raw in raws:
		raw = raw.split(':')
		if raw[0]:
			db.insert(f'INSERT INTO Auth_data VALUES("{raw[0]}", "{raw[1]}")')