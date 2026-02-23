import imaplib
import smtplib
import email
from email.mime.text import MIMEText
import time 

# Fonksiyon artık iki parametre (user, password) alıyor
def get_latest_email(email_user, email_pass):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_pass) # Giriş bilgileri buradan geliyor
        mail.select("inbox")
        
        status, messages = mail.search(None, 'UNSEEN')
        if not messages[0]:
            return None, None, "No emails found in inbox."
            
        # messages[0] içindeki ID listesinden en sondakini (en yeniyi) seçiyoruz
        mail_ids = messages[0].split()
        last_msg_id = mail_ids[-1]
        
        # Mail içeriğini çekiyoruz
        status, data = mail.fetch(last_msg_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Header bilgilerini alalım 
        subject = msg["Subject"]
        sender = msg["From"]
        
        # Mail gövdesini (Body) çıkarma
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                # Sadece düz metin kısmını alıyoruz (HTML değil)
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
       # Bağlantıyı kapat
        mail.logout()
        
        return sender, subject, body

    except Exception as e:
        return None, None, f"Error: {str(e)}"

# Gönderme fonksiyonunu da parametreli yapalım
def send_gmail(email_user, email_pass, to_email, subject, content):
    msg = MIMEText(content)
    msg['Subject'] = f"Re: {subject}"
    msg['From'] = email_user
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)