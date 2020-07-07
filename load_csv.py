import sqlite3
import csv

conn = sqlite3.connect('budgeting.sqlite')
cur = conn.cursor()

with open('E:\OneDrive\Finances\Archive\expensesSqlite.txt', 'r') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter='\t')
	for row in csv_reader:
		sql = '''INSERT INTO expense(date,category_id,budget_id,description,amount)
				VALUES(?,?,?,?,?)'''
		cur.execute(sql, (row[0], row[1], row[2], row[3], row[4]))
conn.commit()

conn.close()

