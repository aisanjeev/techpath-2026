"""Email service for sending notifications."""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from app.core.config import settings
from app.core.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SMTP."""

    def __init__(self) -> None:
        self.server = settings.SMTP_SERVER
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL

    @property
    def is_configured(self) -> bool:
        """Check if email service is configured."""
        return settings.has_smtp_config

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> bool:
        """
        Send an email.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML body content
            text_content: Plain text body (optional, derived from HTML if not provided)
            cc: CC recipients
            bcc: BCC recipients

        Returns:
            True if sent successfully
        """
        if not self.is_configured:
            logger.warning("Email service not configured, skipping email send")
            return False

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email

            if cc:
                msg["Cc"] = ", ".join(cc)

            # Add text and HTML parts
            if text_content:
                msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            # Build recipients list
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)

            # Send email
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.from_email, recipients, msg.as_string())

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise ExternalServiceError("Email Service", str(e))

    async def send_contact_notification(
        self,
        admin_email: str,
        inquiry_name: str,
        inquiry_email: str,
        inquiry_subject: Optional[str],
        inquiry_message: str,
    ) -> bool:
        """Send notification about new contact inquiry."""
        subject = f"New Contact Inquiry: {inquiry_subject or 'General Inquiry'}"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>New Contact Inquiry</h2>
            <p><strong>From:</strong> {inquiry_name} ({inquiry_email})</p>
            <p><strong>Subject:</strong> {inquiry_subject or 'Not specified'}</p>
            <h3>Message:</h3>
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
                {inquiry_message}
            </div>
            <hr>
            <p style="color: #666; font-size: 12px;">
                This notification was sent from TechPath contact form.
            </p>
        </body>
        </html>
        """

        return await self.send_email(admin_email, subject, html_content)

    async def send_contact_confirmation(
        self,
        to_email: str,
        name: str,
    ) -> bool:
        """Send confirmation email to contact form submitter."""
        subject = "Thank you for contacting TechPath"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Thank You, {name}!</h2>
            <p>We have received your message and will get back to you as soon as possible.</p>
            <p>Our team typically responds within 24-48 business hours.</p>
            <p>In the meantime, feel free to explore our services at 
               <a href="{settings.FRONTEND_URL}/services">techpath.biz/services</a>
            </p>
            <hr>
            <p style="color: #666; font-size: 12px;">
                TechPath - AI-Powered IT Solutions for Modern Enterprises
            </p>
        </body>
        </html>
        """

        return await self.send_email(to_email, subject, html_content)

    async def send_newsletter_welcome(
        self,
        to_email: str,
        name: Optional[str] = None,
    ) -> bool:
        """Send welcome email to new newsletter subscriber."""
        subject = "Welcome to TechPath Newsletter!"
        greeting = f"Hi {name}," if name else "Hi there,"

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>{greeting}</h2>
            <p>Thank you for subscribing to the TechPath newsletter!</p>
            <p>You'll receive updates on:</p>
            <ul>
                <li>Latest tech trends and insights</li>
                <li>AI and cloud computing news</li>
                <li>Tips for digital transformation</li>
                <li>Exclusive offers and resources</li>
            </ul>
            <p>
                <a href="{settings.FRONTEND_URL}/blog" 
                   style="background-color: #0ea5e9; color: white; padding: 10px 20px; 
                          text-decoration: none; border-radius: 5px;">
                    Read Our Latest Articles
                </a>
            </p>
            <hr>
            <p style="color: #666; font-size: 12px;">
                You can unsubscribe at any time by clicking the link in our emails.
            </p>
        </body>
        </html>
        """

        return await self.send_email(to_email, subject, html_content)


# Global email service instance
email_service = EmailService()

