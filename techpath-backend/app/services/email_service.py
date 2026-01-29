"""Email service for sending notifications via SMTP or Azure Communication Services."""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


async def get_admin_email(db: AsyncSession, setting_key: str = "admin_notification_email") -> str:
    """
    Get admin notification email from app settings.
    
    Falls back to settings.ADMIN_EMAIL if not set in database.
    """
    from app.crud.app_setting import app_setting_crud
    
    value = await app_setting_crud.get_value(db, setting_key)
    if value:
        return value
    
    # Fallback to environment variable
    return getattr(settings, "ADMIN_EMAIL", "admin@techpath.biz")


async def get_contact_form_recipients(db: AsyncSession) -> List[str]:
    """
    Get contact form notification recipients from app settings.
    
    Returns a list of email addresses.
    """
    from app.crud.app_setting import app_setting_crud
    
    value = await app_setting_crud.get_value(db, "contact_form_recipients")
    if value:
        # Split by comma and strip whitespace
        return [email.strip() for email in value.split(",") if email.strip()]
    
    # Fallback to admin email
    admin_email = await get_admin_email(db)
    return [admin_email]


async def get_enrollment_notification_email(db: AsyncSession) -> str:
    """Get enrollment notification email from app settings."""
    from app.crud.app_setting import app_setting_crud
    
    value = await app_setting_crud.get_value(db, "enrollment_notification_email")
    if value:
        return value
    
    return await get_admin_email(db)


class EmailService:
    """Service for sending emails via SMTP or Azure Communication Services."""

    def __init__(self) -> None:
        # SMTP settings
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
        
        # Azure Communication Services - loaded from Key Vault
        self._azure_connection_string: Optional[str] = None
        self._azure_sender: Optional[str] = None

    def _get_azure_config(self) -> tuple[Optional[str], Optional[str]]:
        """Get Azure Communication Services config from runtime secrets."""
        from app.services.secrets_loader import runtime_secrets
        
        connection_string = runtime_secrets.get("AZURE_COMMUNICATION_EMAIL_CONNECTION_STRING")
        sender = runtime_secrets.get("SENDER_ADDRESS")
        return connection_string, sender

    @property
    def is_azure_configured(self) -> bool:
        """Check if Azure Communication Services is configured."""
        connection_string, sender = self._get_azure_config()
        return bool(connection_string and sender)

    @property
    def is_smtp_configured(self) -> bool:
        """Check if SMTP is configured."""
        return settings.has_smtp_config

    @property
    def is_configured(self) -> bool:
        """Check if any email service is configured."""
        return self.is_azure_configured or self.is_smtp_configured

    async def _send_via_azure(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """Send email via Azure Communication Services."""
        try:
            from azure.communication.email import EmailClient
            
            connection_string, sender = self._get_azure_config()
            if not connection_string or not sender:
                logger.error("Azure Communication Services not configured")
                return False
            
            email_client = EmailClient.from_connection_string(connection_string)
            
            message = {
                "senderAddress": sender,
                "recipients": {
                    "to": [{"address": to_email}]
                },
                "content": {
                    "subject": subject,
                    "html": html_content,
                }
            }
            
            if text_content:
                message["content"]["plainText"] = text_content
            
            poller = email_client.begin_send(message)
            result = poller.result()
            
            logger.info(f"Email sent via Azure to {to_email}, message_id: {result.get('id', 'unknown')}")
            return True
            
        except ImportError:
            logger.error("azure-communication-email package not installed")
            return False
        except Exception as e:
            logger.error(f"Error sending email via Azure: {e}")
            raise ExternalServiceError("Azure Email Service", str(e))

    async def _send_via_smtp(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> bool:
        """Send email via SMTP."""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email

            if cc:
                msg["Cc"] = ", ".join(cc)

            if text_content:
                msg.attach(MIMEText(text_content, "plain"))
            msg.attach(MIMEText(html_content, "html"))

            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_email, recipients, msg.as_string())

            logger.info(f"Email sent via SMTP to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email via SMTP: {e}")
            raise ExternalServiceError("SMTP Email Service", str(e))

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
        Send an email using the configured provider.
        
        Prefers Azure Communication Services, falls back to SMTP.
        """
        if not self.is_configured:
            logger.warning("Email service not configured, skipping email send")
            return False

        # Try Azure first, then SMTP
        if self.is_azure_configured:
            logger.info(f"Sending email to {to_email} via Azure Communication Services")
            return await self._send_via_azure(to_email, subject, html_content, text_content)
        elif self.is_smtp_configured:
            logger.info(f"Sending email to {to_email} via SMTP")
            return await self._send_via_smtp(to_email, subject, html_content, text_content, cc, bcc)
        
        return False

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

    async def send_pilot_signup_notification(
        self,
        admin_email: str,
        name: str,
        email: str,
        phone: str,
        business_name: str,
        industry: str,
        message: Optional[str],
    ) -> bool:
        """Send notification about new pilot signup application."""
        subject = f"New Pilot Application: {business_name} ({industry})"

        # Format industry for display
        industry_display = industry.replace("realestate", "Real Estate").title()
        
        # Format message section
        message_section = ""
        if message:
            message_section = f"""
            <h3>Message:</h3>
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                {message}
            </div>
            """

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0ea5e9; border-bottom: 2px solid #0ea5e9; padding-bottom: 10px;">
                    New Pilot Application Received
                </h2>
                
                <div style="background-color: #f9fafb; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1f2937;">Contact Information</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold; width: 150px;">Name:</td>
                            <td style="padding: 8px 0;">{name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Email:</td>
                            <td style="padding: 8px 0;"><a href="mailto:{email}" style="color: #0ea5e9;">{email}</a></td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Phone:</td>
                            <td style="padding: 8px 0;"><a href="tel:{phone}" style="color: #0ea5e9;">{phone}</a></td>
                        </tr>
                    </table>
                </div>

                <div style="background-color: #f9fafb; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #1f2937;">Business Information</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold; width: 150px;">Business Name:</td>
                            <td style="padding: 8px 0;">{business_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Industry:</td>
                            <td style="padding: 8px 0;">
                                <span style="background-color: #0ea5e9; color: white; padding: 4px 12px; 
                                             border-radius: 4px; font-size: 14px;">
                                    {industry_display}
                                </span>
                            </td>
                        </tr>
                    </table>
                </div>

                {message_section}

                <div style="margin: 30px 0; text-align: center;">
                    <a href="{settings.FRONTEND_URL}/admin/pilot-signups" 
                       style="background-color: #0ea5e9; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;
                              font-weight: bold;">
                        View in Admin Panel
                    </a>
                </div>

                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                
                <p style="color: #6b7280; font-size: 12px; text-align: center;">
                    This notification was sent from TechPath Pilot Signup Form.<br>
                    <a href="{settings.FRONTEND_URL}" style="color: #0ea5e9;">techpath.biz</a>
                </p>
            </div>
        </body>
        </html>
        """

        return await self.send_email(admin_email, subject, html_content)


# Global email service instance
email_service = EmailService()
