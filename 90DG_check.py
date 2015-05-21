import praw
import re
import time
import sqlite3 as lite
import sys

subreddit = '90daysgoal'
database = '90dg.db'

con = None

try:
    con = lite.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM status;")
    data = cur.fetchone()
    #print "DATA = %s" % str(data)
except Exception, e:
    print "ERROR: %s" % str(e)
    sys.exit(1)


r = praw.Reddit(user_agent='90DGCheck by /u/mr_nox')
r.login('mr_nox', 'QKdHcQXkAQUKrgtd3iNj')
sub = r.get_subreddit(subreddit).get_new(limit=25)
currtime = time.time()

sql = 'UPDATE status SET last_check = %d' % (int(currtime))
cur.execute(sql)

for s in sub:
    match = re.search(r'Daily Goal', s.title, re.IGNORECASE)
    if match:
        tdiff = currtime - s.created_utc
        hours, rest = divmod(tdiff,3600)
        minutes, secs = divmod(rest, 60)
        #print "Found post: \"{}\" - posted {}:{}:{} ago".format(s.title, int(hours), int(minutes), int(secs))
        #print s, s.title, s.created_utc, s.short_link, s.id
        if s.created_utc > data[2]:
            print ">>> New 90DG Daily Goal post was found.  \"{}\" posted {}:{}:{} ago.  See {}".format(s.title, int(hours), int(minutes), int(secs), s.short_link)
            cur.execute("UPDATE status SET last_found_id=?, last_found_time=?", (s.id, int(s.created_utc)))
        break


if con:
    con.commit()
    con.close()
