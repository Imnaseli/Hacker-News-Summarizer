import config as Email
#import user as Email
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import yagmail

now = datetime.datetime.now()
now = now.strftime("%A %m %Y")

content = ''

def extractNews(url):
    print('Extracting News')
    cnt = ''
    cnt += ('<b>Hacker News Top Stories:</b>\n'+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content , 'html.parser')
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title' , 'valign':''})):
        cnt += ((str(i + 1)+'::'+tag.text +'\n' + '<br>') if tag.text != 'More' else '')
    return (cnt)

cnt = extractNews("https://news.ycombinator.com/")
content += cnt
content += ('<br><br><b>End of Message</b>')
#print(content)

#Send the mail

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = Email.address
TO = Email.recipients
PASS = Email.password

msg = MIMEMultipart()

msg['Subject'] = 'Top Hack News Stories '+str(str(now))
msg['From'] = FROM
msg['To'] = ','.join(TO)


msg.attach(MIMEText(content , 'html'))


text = msg.as_bytes()
textb = msg.as_string()


print('Starting server')
server = smtplib.SMTP_SSL('smtp.gmail.com' , 465 , timeout=120)
print ('Server Created!')
server.set_debuglevel(0)
server.ehlo()
server.login(FROM , PASS)


#I am pretty sure this is unnecessary, because the to_addrs also recieves iterables as a parameter
for to in TO:
    server.sendmail(FROM , to , text)
server.quit()

print("Email Sent")



























 
