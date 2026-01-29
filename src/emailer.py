"""Email outreach for distressed seller leads"""
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
from config import GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_SIGNATURE

class Emailer:
    """Send outreach emails to leads"""

    def __init__(self, user=GMAIL_USER, password=GMAIL_APP_PASSWORD):
        self.user = user
        self.password = password

    def send_outreach(self, to_email, lead_data, template='initial'):
        """Send outreach email to property agent"""
        if not self.user or not self.password:
            print("⚠️  Gmail not configured - email not sent")
            return None

        subject = self._get_subject(lead_data, template)
        body = self._get_body(lead_data, template)

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = formataddr(("Distressed Seller System", self.user))
        msg['To'] = to_email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.user, self.password)
                server.sendmail(self.user, to_email, msg.as_string())
            print(f"✅ Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"❌ Email failed: {e}")
            return False

    def _get_subject(self, lead, template):
        """Generate email subject"""
        score = lead.get('score', 0)
        if template == 'initial':
            return f"Interested in {lead.get('address', 'your property')}"
        elif template == 'followup':
            return f"Following up - {lead.get('address', 'property')}"
        else:
            return f"Cash offer for {lead.get('address', 'your property')}"

    def _get_body(self, lead, template):
        """Generate email body based on template"""
        score = lead.get('score', 0)
        address = lead.get('address', 'your property')
        agent_name = lead.get('agent_name', 'there')

        templates = {
            'initial': f"""Hi {agent_name},

I noticed the property at {address} has been on the market for a while and may not be getting the attention it deserves.

I'm a real estate investor who works with motivated sellers in the St. Petersburg area. If your client is open to exploring options, I'd love to discuss how I might help.

I'm particularly interested in properties where the seller needs a quick, hassle-free solution.

Would you have a few minutes for a quick call this week?

Best regards

{EMAIL_SIGNATURE}""",

            'followup': f"""Hi {agent_name},

Following up on my previous email about {address}.

I understand the market can be challenging, and I'm here to help if your client is looking for options.

Would you be open to a brief conversation?

Best regards

{EMAIL_SIGNATURE}""",

            'cash_offer': f"""Hi {agent_name},

I'm prepared to make a fair cash offer on {address} with a quick closing.

If your client is looking to sell without the traditional listing process, I can provide a straightforward solution.

Are you available for a quick call?

Best regards

{EMAIL_SIGNATURE}"""
        }

        return templates.get(template, templates['initial'])

    def send_batch(self, leads, template='initial'):
        """Send emails to multiple leads"""
        results = []
        for lead in leads:
            if lead.get('agent_email'):
                success = self.send_outreach(lead['agent_email'], lead, template)
                results.append({
                    'email': lead['agent_email'],
                    'success': success,
                    'property_id': lead.get('property_id')
                })
        return results


if __name__ == '__main__':
    # Test email
    emailer = Emailer()

    test_lead = {
        'property_id': 'test-123',
        'address': '123 Main St, St. Petersburg, FL 33701',
        'score': 85,
        'agent_name': 'John Smith',
        'agent_email': 'dasgoswami@gmail.com',
    }

    if GMAIL_USER:
        emailer.send_outreach(GMAIL_USER, test_lead)
    else:
        print("⚠️  Gmail not configured - skipping test")