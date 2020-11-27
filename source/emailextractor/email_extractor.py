import sqlite3

"""
Small code for email adresses capture 
Asks for an email dump as txt and captures sender adresses and organizations
saves them in a small sqlite database along with counts.
displays top 10

mailboxdump follows a schema where sender lines are identified by starting with "From: "
regex wasnot used since this is simple enough to work with string commands
 
"""
# Creates connection, drops the tables if they exist and then creates fresh tables
conn = sqlite3.connect(r'data/emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS OrgCounts')
cur.execute('DROP TABLE IF EXISTS SenderCounts')

cur.execute('''
CREATE TABLE OrgCounts (org TEXT, count INTEGER)''')
cur.execute('''
CREATE TABLE SenderCounts (sender TEXT, count INTEGER)''')

# get's the name of the file to process or uses development one
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = r'data/mbox.txt'

fh = open(fname)
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()

    senderemail: str
    senderorg: str

    for piece in pieces:
        if not piece.find("@") == -1:
            senderemail = piece
            senderorg = piece.split("@")[1]

            cur.execute('SELECT count FROM OrgCounts WHERE org = ? ', (senderorg,))
            row = cur.fetchone()
            if row is None:
                cur.execute('''INSERT INTO OrgCounts (org, count)
                        VALUES (?, 1)''', (senderorg,))
            else:
                cur.execute('UPDATE OrgCounts SET count = count + 1 WHERE org = ?',
                            (senderorg,))

            cur.execute('SELECT count FROM SenderCounts WHERE sender = ? ', (senderemail,))
            row = cur.fetchone()
            if row is None:
                cur.execute('''INSERT INTO SenderCounts (sender, count)
                        VALUES (?, 1)''', (senderemail,))
            else:
                cur.execute('UPDATE SenderCounts SET count = count + 1 WHERE sender = ?',
                            (senderemail,))

conn.commit()

sqlstr = 'SELECT org, count FROM OrgCounts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

sqlstr = 'SELECT sender, count FROM SenderCounts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
