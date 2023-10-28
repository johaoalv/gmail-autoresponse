import imaplib
import email
import smtplib

# Configura la información de tu cuenta de correo
email_user = "johaoalvarado24@gmail.com"
email_pass = "rnjo ldsn qvrq cuka"
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Establece las palabras clave y respuestas correspondientes
keywords = {
    "bloque pc": "Para desbloquear la PC, debes seguir este manual.",
    "se me bloqueo la cuenta de okta": "Para solicitar una nueva clave, hazlo por este enlace.",
}

# Conecta con el servidor IMAP y recupera los correos electrónicos
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(email_user, email_pass)
mail.select("inbox")

status, email_ids = mail.search(None, "UNSEEN")

if status == "OK":
    email_id_list = email_ids[0].split()
    for email_id in email_id_list:
        try:
            status, email_data = mail.fetch(email_id, "(RFC822)")
            if status == "OK":
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)
                for keyword, response in keywords.items():
                    subject = str(msg.get("subject", "")).lower()
                    payload = b""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    payload += part.get_payload(decode=True)
                                except Exception as e:
                                    print("Error al decodificar contenido:", e)
                    else:
                        payload = msg.get_payload(decode=True)
                    if keyword in subject or keyword in payload.decode("utf-8", errors="ignore").lower():
                        # Envia una respuesta automática
                        server = smtplib.SMTP(smtp_server, smtp_port)
                        server.starttls()
                        server.login(email_user, email_pass)
                        subject = "Re: " + msg["subject"]
                        body = response
                        reply = f"Subject: {subject}\n\n{body}"
                        server.sendmail(email_user, msg["from"], reply)
                        server.quit()
        except Exception as e:
            print("Error al interactuar con el servidor IMAP:", e)

mail.logout()
