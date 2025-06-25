"""
Email Redirection Service - Privacy-First Email Interception
Intercepts all outgoing emails and stores them locally instead of sending to external services.
"""

import logging
from typing import Dict, List, Union
from django.utils.html import strip_tags
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class EmailRedirectionService:
    """
    Service that intercepts emails and stores them locally instead of sending externally.
    
    This replaces all external email sending with local storage for privacy protection.
    """
    
    # External services that would have been used for email sending
    EXTERNAL_EMAIL_SERVICES = {
        'smtp.gmail.com': 'Gmail SMTP',
        'smtp.office365.com': 'Office 365 SMTP',
        'api.sendgrid.com': 'SendGrid API',
        'api.mailgun.net': 'Mailgun API',
        'smtp.mailgun.org': 'Mailgun SMTP',
        'smtp.postmarkapp.com': 'Postmark SMTP',
        'smtp.amazonses.com': 'Amazon SES',
        'smtp.mailchimp.com': 'Mailchimp Transactional',
        'smtp.sendinblue.com': 'Brevo/SendinBlue SMTP',
        'api.brevo.com': 'Brevo API',
    }
    
    def __init__(self):
        self.stats = {
            'emails_intercepted': 0,
            'external_services_blocked': set(),
            'sensitive_emails_secured': 0,
        }
    
    def intercept_email(
        self,
        to_email: Union[str, List[str]],
        subject: str,
        html_content: str = None,
        text_content: str = None,
        from_email: str = None,
        email_type: str = 'other',
        headers: Dict = None,
        original_destination: str = 'external-smtp'
    ) -> str:
        """
        Intercept an email and store it locally instead of sending it.
        
        Args:
            to_email: Recipient email address(es)
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text email content
            from_email: Sender email address
            email_type: Type of email (auth, notification, etc.)
            headers: Email headers
            original_destination: External service that would have sent this
            
        Returns:
            str: ID of the stored email
        """
        try:
            # Import here to avoid circular imports
            from plane.db.models.email_redirection import RedirectedEmail
            
            # Handle multiple recipients
            if isinstance(to_email, list):
                to_email = to_email[0] if to_email else 'unknown@localhost'
            
            # Sanitize content and remove external links
            sanitized_html, links_removed = self._sanitize_email_content(html_content)
            
            # Detect sensitive content
            contains_sensitive = self._detect_sensitive_content(subject, sanitized_html, text_content)
            
            # Create redirected email record
            redirected_email = RedirectedEmail.objects.create(
                to_email=to_email,
                from_email=from_email or 'system@localhost',
                subject=subject,
                html_content=sanitized_html or '',
                text_content=text_content or strip_tags(sanitized_html) if sanitized_html else '',
                email_type=email_type,
                original_destination=original_destination,
                status='stored',
                headers=headers or {},
                contains_sensitive_data=contains_sensitive,
                external_links_removed=links_removed,
            )
            
            # Update statistics
            self.stats['emails_intercepted'] += 1
            self.stats['external_services_blocked'].add(original_destination)
            if contains_sensitive:
                self.stats['sensitive_emails_secured'] += 1
            
            logger.info(
                f"📧 EMAIL INTERCEPTED: {subject[:50]}... → Local storage "
                f"(was destined for {original_destination})"
            )
            
            return str(redirected_email.id)
            
        except Exception as e:
            logger.error(f"Failed to intercept email: {e}")
            # Fallback: still don't send the email, just log the attempt
            logger.warning(f"Email blocked but not stored: {subject[:50]}...")
            return "blocked-not-stored"
    
    def _sanitize_email_content(self, html_content: str) -> tuple[str, bool]:
        """
        Remove external links and resources from email content.
        
        Returns:
            tuple: (sanitized_content, links_were_removed)
        """
        if not html_content:
            return html_content, False
        
        links_removed = False
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove external images and replace with placeholders
            for img in soup.find_all('img'):
                src = img.get('src', '')
                if src and (src.startswith('http') or src.startswith('//')):
                    # Replace with placeholder
                    img['src'] = 'data:text/plain;charset=utf-8,[EXTERNAL IMAGE REMOVED]'
                    img['alt'] = f'[External image removed: {src[:50]}...]'
                    links_removed = True
            
            # Remove external links but keep text
            for link in soup.find_all('a'):
                href = link.get('href', '')
                if href and (href.startswith('http') or href.startswith('//')):
                    # Replace link with text and note
                    link_text = link.get_text()
                    new_text = f"{link_text} [External link removed: {href[:30]}...]"
                    link.replace_with(new_text)
                    links_removed = True
            
            # Remove external stylesheets and scripts
            for element in soup.find_all(['link', 'script']):
                href_or_src = element.get('href') or element.get('src', '')
                if href_or_src and (href_or_src.startswith('http') or href_or_src.startswith('//')):
                    element.decompose()
                    links_removed = True
            
            return str(soup), links_removed
            
        except Exception as e:
            logger.warning(f"Failed to sanitize email content: {e}")
            return html_content, False
    
    def _detect_sensitive_content(self, subject: str, html_content: str, text_content: str) -> bool:
        """
        Detect if email contains sensitive information.
        """
        sensitive_keywords = [
            'password', 'token', 'secret', 'key', 'credential',
            'login', 'signin', 'signup', 'reset', 'activation',
            'invitation', 'invite', 'verify', 'confirmation',
            'billing', 'payment', 'invoice', 'subscription'
        ]
        
        content_to_check = f"{subject} {html_content or ''} {text_content or ''}".lower()
        
        return any(keyword in content_to_check for keyword in sensitive_keywords)
    
    def get_interception_stats(self) -> Dict:
        """Get statistics about intercepted emails"""
        return {
            'emails_intercepted': self.stats['emails_intercepted'],
            'external_services_blocked': list(self.stats['external_services_blocked']),
            'sensitive_emails_secured': self.stats['sensitive_emails_secured'],
            'privacy_status': 'SECURE - All emails stored locally',
        }


# Monkey patch Django's email sending to use our redirection service
def redirect_django_email():
    """
    Monkey patch Django's email backend to redirect all emails to local storage.
    """
    
    original_send_messages = None
    
    def patched_send_messages(self, email_messages):
        """
        Patched version that intercepts emails instead of sending them.
        """
        redirection_service = EmailRedirectionService()
        
        for message in email_messages:
            # Determine email type based on subject/content
            email_type = 'other'
            subject_lower = message.subject.lower()
            
            if any(word in subject_lower for word in ['password', 'reset', 'login', 'signin']):
                email_type = 'auth'
            elif any(word in subject_lower for word in ['notification', 'update', 'comment']):
                email_type = 'notification'
            elif any(word in subject_lower for word in ['invitation', 'invite']):
                email_type = 'invitation'
            elif any(word in subject_lower for word in ['system', 'admin', 'error']):
                email_type = 'system'
            elif any(word in subject_lower for word in ['webhook', 'api']):
                email_type = 'webhook'
            
            # Get HTML content
            html_content = None
            if hasattr(message, 'alternatives') and message.alternatives:
                for content, mimetype in message.alternatives:
                    if mimetype == 'text/html':
                        html_content = content
                        break
            
            # Intercept the email
            redirection_service.intercept_email(
                to_email=message.to,
                subject=message.subject,
                html_content=html_content,
                text_content=message.body,
                from_email=message.from_email,
                email_type=email_type,
                original_destination=getattr(self, 'host', 'external-smtp')
            )
        
        # Return success count without actually sending
        return len(email_messages)
    
    # Apply the monkey patch
    try:
        from django.core.mail.backends.smtp import EmailBackend
        if not hasattr(EmailBackend, '_original_send_messages'):
            EmailBackend._original_send_messages = EmailBackend.send_messages
            EmailBackend.send_messages = patched_send_messages
            logger.info("✅ Email redirection service activated - All emails will be stored locally")
    except ImportError:
        logger.warning("Django email backend not available for patching")


# Global email redirection service instance
email_redirection_service = EmailRedirectionService()

# Auto-activate email redirection when module is imported
redirect_django_email() 