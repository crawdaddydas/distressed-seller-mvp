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
        address = lead.get('address', 'your property').split(',')[0]  # Just street address

        subjects = {
            'initial': f"Quick question about {address}",
            'followup': f"Following up - {address}",
            'cash_offer': f"Cash offer for {address}",
            'urgent': f"Urgent - {address}",
            'data_point': f"Data point for {address}",
        }
        return subjects.get(template, subjects['initial'])

    def _get_body(self, lead, template):
        """Generate email body based on template"""
        agent_name = lead.get('agent_name', 'there').split()[0]  # First name only
        address = lead.get('address', 'your property')
        price = lead.get('current_price', 0)
        days = lead.get('listing_days', 0)
        score = lead.get('score', 0)
        category, _ = self._get_category(score)

        templates = {
            'initial': f"""Hi {agent_name},

I noticed the property at {address} has been on the market for {days} days.

As a local real estate investor, I work with sellers who need flexibility and speed. If your client is open to exploring options, I'd love to discuss how I might help.

I'm not looking to list the property — I'm interested in a direct purchase that could close in as little as 7 days.

Would you have 2 minutes for a quick call this week?

Best regards

{EMAIL_SIGNATURE}""",

            'followup': f"""Hi {agent_name},

Following up on my email about {address}.

I understand the market can be challenging, and I'm here to help if your client is looking for alternatives to the traditional listing process.

If you're open to it, I'd welcome the chance to discuss how I might be able to help your client sell quickly.

No pressure at all — just wanted to make sure you saw my initial message.

Best regards

{EMAIL_SIGNATURE}""",

            'cash_offer': f"""Hi {agent_name},

I wanted to reach out directly about {address}.

I'm prepared to make a fair, all-cash offer with a quick closing timeline — as fast as 7 days if needed. No listing, no showings, no hassle.

Given that the property has been on the market for {days} days, I thought your client might be open to a different approach.

Would you be available for a brief call to discuss?

Best regards

{EMAIL_SIGNATURE}""",

            'urgent': f"""Hi {agent_name},

I'm reaching out urgently about {address} — I know time matters when a property has been on the market for {days} days.

I'm a cash buyer who can close this week. No contingencies, no financing delays.

If your client is motivated to sell, I can make this happen quickly and cleanly.

Can we talk today?

Best regards

{EMAIL_SIGNATURE}""",

            'data_point': f"""Hi {agent_name},

I wanted to share some data about {address} that's on the market for {days} days at ${price:,}.

As a local investor, I'm tracking properties in this area and wanted to reach out before your client considers another price reduction.

If you're open to it, I'd welcome the opportunity to discuss a direct purchase option that could save your client time and uncertainty.

Best regards

{EMAIL_SIGNATURE}"""
        }

        return templates.get(template, templates['initial'])

    def _get_category(self, score):
        """Get category based on score"""
        if score >= 85:
            return 'URGENT', 'Contact immediately'
        elif score >= 70:
            return 'HIGH', 'Reach out within 24-48hrs'
        elif score >= 50:
            return 'MODERATE', 'Monitor'
        else:
            return 'LOW', 'Not a priority'

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