from urllib import urlencode
import httplib2

class Email:
    def __init__(self, address, subject, body):
        self.address=address
        self.subject=subject
        self.body=body

def sendEmails(email_subject, email_template, contact_names, contact_emails, sender):
    emails = []
    contact_names = contact_names.splitlines()
    contact_emails = contact_emails.splitlines()
    if (len(contact_names) != len(contact_emails)):
        return

    http = httplib2.Http()
    http.add_credentials('api', 'key-f2af758e59ed0ccc8cfdddd098691279')

    url = 'https://api.mailgun.net/v3/valleyconsultinggroup.org/messages'
    for i in range(len(contact_names)):
        contact_name = contact_names[i].split()[0]
        contact_email = contact_emails[i]
        body = email_template.replace("%NAME%", contact_name)
        data = {
            'from': sender,
            'to': contact_email,
            'subject': email_subject,
            'text': body
        }

        resp, content = http.request(url, 'POST', urlencode(data))

        if resp.status != 200:
            raise RuntimeError(
                'Mailgun API error: {} {}'.format(resp.status, content))
        else:
            emails.append(Email(contact_email, email_subject, body))
    return { 'emails':emails }