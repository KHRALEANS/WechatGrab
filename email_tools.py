import smtplib
from email.mime.text import MIMEText
from email.header import Header
from unicodedata import name


def send_qq_smtp_email(WXmsg, contact, config):
    SENDER_USERNAME = config['SENDER_USERNAME']
    SENDER_PASSWORD = config['SENDER_PASSWORD']
    RECEIVER = config['RECEIVER']
    MESSAGE = WXmsg

    message = MIMEText(MESSAGE, 'plain', 'utf-8')
    message['From'] = Header(SENDER_USERNAME, 'utf-8')
    message['To'] = Header("我", 'utf-8')
    message['Subject'] = Header(f"来自<-{contact}->的新消息", 'utf-8')

    err = None
    try:
        session = smtplib.SMTP('smtp.qq.com', 587)
        session.ehlo()
        session.starttls()
        session.login(SENDER_USERNAME, SENDER_PASSWORD)
        session.sendmail(SENDER_USERNAME, RECEIVER, message.as_string())
    except Exception as e:
        err = e

    return err

if __name__ == '__main__':
    print('test')
    result = send_qq_smtp_email("今天真热", 'python')
    print(result)