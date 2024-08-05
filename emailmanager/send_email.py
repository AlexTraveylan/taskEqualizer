import resend

from TaskEqualizer.settings import DOMAIN_EMAIL, MY_EMAIL, RESEND_API_KEY

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


def send_contact_message(subject: str, html: str):
    payload = {
        "from": DOMAIN_EMAIL,
        "to": [MY_EMAIL],
        "subject": subject,
        "html": html,
    }

    return resend.Emails.send(payload)
