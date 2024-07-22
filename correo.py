from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    
    # Verificar que los datos necesarios están presentes
    if not all(k in data for k in ("to_email", "subject", "message")):
        return jsonify({"error": "Faltan datos"}), 400
 
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "turiiiiin24@gmail.com"  # Reemplaza con tu dirección de correo
    smtp_password = "rwoh pkql zwfz ckhv"  # Reemplaza con tu contraseña

    to_email = data['to_email']
    subject = data['subject']
    message = data['message']

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Conectar al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar la conexión TLS
        server.login(smtp_user, smtp_password)

        # Enviar el correo
        server.send_message(msg)
        server.quit()
        return jsonify({"message": "Correo enviado exitosamente!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)