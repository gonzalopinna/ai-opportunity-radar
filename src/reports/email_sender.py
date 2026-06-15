import os
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path


try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


REQUIRED_EMAIL_ENV_VARS = (
    "EMAIL_HOST",
    "EMAIL_PORT",
    "EMAIL_USER",
    "EMAIL_PASSWORD",
    "EMAIL_TO",
)


@dataclass(frozen=True)
class EmailConfig:
    host: str
    port: int
    user: str
    password: str
    recipients: tuple[str, ...]


@dataclass(frozen=True)
class EmailSendResult:
    sent: bool
    skipped: bool
    message: str


def load_environment() -> None:
    """Load .env values when python-dotenv is installed."""
    if load_dotenv is not None:
        load_dotenv()


def missing_email_env_vars() -> list[str]:
    """Return the email environment variables that are missing or empty."""
    return [name for name in REQUIRED_EMAIL_ENV_VARS if not os.getenv(name)]


def get_email_config_from_env() -> tuple[EmailConfig | None, list[str]]:
    """Build email config from environment variables."""
    load_environment()
    missing_vars = missing_email_env_vars()
    if missing_vars:
        return None, missing_vars

    recipients = tuple(
        recipient.strip()
        for recipient in os.environ["EMAIL_TO"].split(",")
        if recipient.strip()
    )

    if not recipients:
        return None, ["EMAIL_TO"]

    return (
        EmailConfig(
            host=os.environ["EMAIL_HOST"],
            port=int(os.environ["EMAIL_PORT"]),
            user=os.environ["EMAIL_USER"],
            password=os.environ["EMAIL_PASSWORD"],
            recipients=recipients,
        ),
        [],
    )


def build_email_message(
    config: EmailConfig,
    html_content: str,
    subject: str,
    markdown_content: str | None = None,
) -> EmailMessage:
    """Build an HTML email message with an optional Markdown fallback."""
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = config.user
    message["To"] = ", ".join(config.recipients)

    plain_text = markdown_content or "AI Opportunity Radar report attached as HTML."
    message.set_content(plain_text)
    message.add_alternative(html_content, subtype="html")

    return message


def send_message(config: EmailConfig, message: EmailMessage) -> None:
    """Send an email message through SMTP."""
    if config.port == 465:
        with smtplib.SMTP_SSL(config.host, config.port) as server:
            server.login(config.user, config.password)
            server.send_message(message)
        return

    with smtplib.SMTP(config.host, config.port) as server:
        server.starttls()
        server.login(config.user, config.password)
        server.send_message(message)


def send_email_report(
    html_report_path: Path,
    markdown_report_path: Path | None = None,
    subject: str = "AI Opportunity Radar Daily Report",
) -> EmailSendResult:
    """Send the generated HTML report by email when configuration is available."""
    config, missing_vars = get_email_config_from_env()
    if config is None:
        missing = ", ".join(missing_vars)
        return EmailSendResult(
            sent=False,
            skipped=True,
            message=f"Email skipped because configuration is missing: {missing}",
        )

    if not html_report_path.exists():
        raise FileNotFoundError(f"HTML report not found: {html_report_path}")

    html_content = html_report_path.read_text(encoding="utf-8")
    markdown_content = None

    if markdown_report_path is not None and markdown_report_path.exists():
        markdown_content = markdown_report_path.read_text(encoding="utf-8")

    message = build_email_message(
        config=config,
        html_content=html_content,
        markdown_content=markdown_content,
        subject=subject,
    )
    send_message(config, message)

    return EmailSendResult(
        sent=True,
        skipped=False,
        message=f"Email sent to {', '.join(config.recipients)}",
    )
