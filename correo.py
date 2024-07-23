from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText#
 
  
app = Flask(__name__)
smtp_user = "turiiiiin24@gmail.com"  # Reemplaza con tu dirección de correo
smtp_password = "rwoh pkql zwfz ckhv"  # Reemplaza con tu contraseña


@app.route('/send-email', methods=['POST'])
def send_email():
    
    data = request.get_json()
    
    # Verificar que los datos necesarios están presentes
    if not all(k in data for k in ("to_email", "subject", "message")):
        return jsonify({"error": "Faltan datos"}), 400
    
    if not smtp_user or not smtp_password:
        return jsonify({"error": "Las variables de entorno SMTP_USER o SMTP_PASSWORD no están configuradas."}), 500

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    to_email = data['to_email']
    subject = data['subject']
    message_content = data['message']

    # Crear el contenido HTML del mensaje
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding-bottom: 20px;
            }}
            .header h1 {{
                color: #007BFF;
            }}
            .content {{
                font-size: 16px;
                line-height: 1.6;
                color: #333333;
            }}
            .footer {{
                text-align: center;
                font-size: 14px;
                color: #777777;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Se Ha Registrado ¡Un Nuevo Pedido!</h1>
            </div>
            <div class="content">
                <p>{message_content}</p>
            </div>
            <div class="footer">
                <p>Gracias por su atención.</p>
                <p>Atentamente,<br>Nuestro Equipo</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

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