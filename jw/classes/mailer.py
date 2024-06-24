from mailersend import emails

# assigning NewEmail() without params defaults to MAILERSEND_API_KEY env var
mailer = emails.NewEmail()

# define an empty dict to populate with mail values
mail_body = {}

print(mailer.send(mail_body))

mail_from = {
    "name": "Your Name",
    "email": "your@domain.com",
}

recipients = [
    {
        "name": "george",
        "email": "georgepanglili@qq.com",
    }
]

reply_to = {
    "name": "Name",
    "email": "reply@domain.com",
}

print(mailer.send(mail_body))

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello!", mail_body)
mailer.set_html_content("This is the HTML content", mail_body)
mailer.set_plaintext_content("This is the text content", mail_body)
mailer.set_reply_to(reply_to, mail_body)

print(mailer.send(mail_body))

# using print() will also return status code and data
mailer.send(mail_body)
