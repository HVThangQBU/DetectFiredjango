

import telegram
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from twilio.rest import Client
from canhbao.readConfig import args

class SendWarning:
  def __init__(self):
    pass
  def sendEmail(self, toaddr, filename):
    try:
      email_address = args["EMAIL_ADDRESS"]
      email_password = args["EMAIL_PASSWORD"]
      if email_address is None or email_password is None:
        # no email address or password
        # something is not configured properly
        print("Did you set email address and password correctly?")
        return False
      msg = MIMEMultipart()
      msg['From'] = email_address
      msg['To'] = toaddr
      msg['Subject'] = "CẢNH BÁO SỰ CỐ"
      body = "Khu vực đang  có sự cố"
      msg.attach(MIMEText(body, 'plain'))
      attachment = filename
      p = MIMEBase('application', 'octet-stream')
      p.set_payload((attachment).read())
      encoders.encode_base64(p)
      p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
      msg.attach(p)
      s = smtplib.SMTP('smtp.gmail.com', 587)
      s.starttls()
      s.login(email_address, email_password)
      text = msg.as_string()
      s.sendmail(email_address, toaddr, text)
      s.quit()

    except Exception as e:
      print("Problem during send email")
      print(str(e))
    return False

  def sendTelegram(self, chatId, text, photo, caption):
    my_token = args["MY_TOKEN"]
    bot = telegram.Bot(token=my_token)
    bot.send_message(chat_id=chatId, text=text)
    bot.sendPhoto(chat_id=chatId, photo=photo, caption=caption)
  def sendSMS(self):
    # Your Account Sid and Auth Token from twilio.com / console
    account_sid = 'AC4ee5b584a317a57b13408c3a0d55f8de'
    auth_token = '9308b0f5ad20578fee1910e495b7c7a6'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
      from_='+13149476335',
      body='test sms',
      to='+84862427726'
    )
    print(message.sid)

