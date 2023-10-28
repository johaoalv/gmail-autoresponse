import imaplib

# Configura la información de tu cuenta de correo
email_user = "johaoalvarado24@gmail.com"
email_pass = "rnjo ldsn qvrq cuka"

try:
    # Conecta con el servidor IMAP
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_user, email_pass)
    
    # Si la conexión y el inicio de sesión fueron exitosos
    print("Conexión exitosa. Las credenciales son válidas.")
    
    # Cierra la conexión
    mail.logout()
except Exception as e:
    # Si se produce un error
    print("Error al conectar o iniciar sesión:", e)
