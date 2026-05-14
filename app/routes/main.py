from flask import Blueprint, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

main_bp = Blueprint('main', __name__)

# ─── Configura aquí tus credenciales ───────────────────────────────────────────
SMTP_EMAIL   = os.environ.get('SMTP_EMAIL',    'byds.dev@gmail.com')
SMTP_PASSWORD= os.environ.get('SMTP_PASSWORD', '')   # <-- Pon tu contraseña de app de Google
DEST_EMAIL   = 'byds.dev@gmail.com'
# ────────────────────────────────────────────────────────────────────────────────

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/contact', methods=['POST'])
def contact():
    data    = request.form
    name    = data.get('name',    '').strip()
    email   = data.get('email',   '').strip()
    message = data.get('message', '').strip()

    if not all([name, email, message]):
        return jsonify({"status": "error", "message": "Por favor completa todos los campos."})

    # ── Construir el correo ──────────────────────────────────────────────────
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'🚀 Nuevo mensaje de {name} — BYDS.DEV'
    msg['From']    = SMTP_EMAIL
    msg['To']      = DEST_EMAIL
    msg['Reply-To'] = email

    body_html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;background:#0a0a0a;color:#fff;padding:40px;border-radius:12px;">
        <h2 style="color:#00d2ff;border-bottom:1px solid #1a1a2e;padding-bottom:16px;">
            📩 Nuevo mensaje desde BYDS.DEV
        </h2>
        <table style="width:100%;border-collapse:collapse;margin-top:24px;">
            <tr><td style="padding:10px 0;color:#a1a1aa;width:120px;">Nombre</td>
                <td style="padding:10px 0;font-weight:700;">{name}</td></tr>
            <tr><td style="padding:10px 0;color:#a1a1aa;">Email</td>
                <td style="padding:10px 0;"><a href="mailto:{email}" style="color:#00d2ff;">{email}</a></td></tr>
        </table>
        <div style="margin-top:24px;padding:24px;background:#111;border-left:4px solid #00d2ff;border-radius:4px;">
            <p style="color:#a1a1aa;margin:0 0 8px;">Mensaje:</p>
            <p style="margin:0;line-height:1.7;">{message}</p>
        </div>
        <p style="margin-top:32px;color:#444;font-size:12px;">
            Enviado desde byds.proyecto.sbs
        </p>
    </div>
    """
    msg.attach(MIMEText(body_html, 'html'))

    # ── Enviar vía Gmail SMTP ────────────────────────────────────────────────
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, DEST_EMAIL, msg.as_string())
        return jsonify({"status": "success",
                        "message": f"¡Gracias {name}! Tu mensaje llegó correctamente. Te responderé pronto 🚀"})
    except Exception as e:
        print(f"[SMTP ERROR] {e}")
        return jsonify({"status": "error",
                        "message": "Hubo un problema al enviar el mensaje. Escríbenos directamente a byds.dev@gmail.com"})
