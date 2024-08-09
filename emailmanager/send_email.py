import resend

from TaskEqualizer.settings import (
    CONFIRMATION_URL,
    DOMAIN_EMAIL,
    MY_EMAIL,
    RESEND_API_KEY,
)

resend.api_key = RESEND_API_KEY


def html_wrapper_for_mail(message: str) -> str:
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Contact Form Message</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 20px;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            .message {{
                background-color: #ffffff;
                border-left: 4px solid #3498db;
                padding: 15px;
                margin-top: 20px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 0.8em;
                color: #7f8c8d;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>New Contact Form Message</h1>
            <p>You have received a new message from your website's contact form:</p>
            <div class="message">
                {message}
            </div>
            <div class="footer">
                <p>This email was sent from your website's contact form.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def html_wrapper_for_confirmation_email_with_token(token: str) -> str:
    html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmation de votre adresse e-mail</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 20px;
            }}
            h1 {{
                color: #0056b3;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #0056b3;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 0.8em;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Confirm your email address</h1>
            <p>Hello,</p>
            <p>Thank you for registering your email address. Note that this email address is encrypted in my database. To confirm your email address, please click on the button below :</p>
            <p style="text-align: center;">
                <a href="{CONFIRMATION_URL}/{token}" class="btn">Confirm my email</a>
            </p>
            <p>If the button does not work, you can copy and paste the following link in your browser :</p>
            <p>{CONFIRMATION_URL}/{token}</p>
            <p>If you did not request this confirmation, you can ignore this email.</p>
            <p>Best regards,<br>Task Equalizer, by AlexTraveylan</p>
        </div>
        <div class="footer">
            <p>This email was sent automatically. Please do not reply.</p>
        </div>
    </body>
    </html>
    """
    return html


def send_contact_message(subject: str, html: str, *, to: str = MY_EMAIL):
    payload = {
        "from": DOMAIN_EMAIL,
        "to": [to],
        "subject": subject,
        "html": html,
    }

    return resend.Emails.send(payload)
