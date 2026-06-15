import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from src.reports.email_sender import (
    EmailConfig,
    build_email_message,
    get_email_config_from_env,
    send_email_report,
    send_message,
)


class EmailSenderTests(unittest.TestCase):
    def test_get_email_config_from_env_reports_missing_values(self):
        with patch.dict(os.environ, {}, clear=True):
            config, missing_vars = get_email_config_from_env()

        self.assertIsNone(config)
        self.assertIn("EMAIL_HOST", missing_vars)
        self.assertIn("EMAIL_PASSWORD", missing_vars)

    def test_get_email_config_from_env_builds_config(self):
        env = {
            "EMAIL_HOST": "smtp.example.com",
            "EMAIL_PORT": "587",
            "EMAIL_USER": "sender@example.com",
            "EMAIL_PASSWORD": "app-password",
            "EMAIL_TO": "one@example.com, two@example.com",
        }

        with patch.dict(os.environ, env, clear=True):
            config, missing_vars = get_email_config_from_env()

        self.assertEqual(missing_vars, [])
        self.assertEqual(config.host, "smtp.example.com")
        self.assertEqual(config.port, 587)
        self.assertEqual(config.recipients, ("one@example.com", "two@example.com"))

    def test_build_email_message_sets_html_alternative(self):
        config = EmailConfig(
            host="smtp.example.com",
            port=587,
            user="sender@example.com",
            password="app-password",
            recipients=("recipient@example.com",),
        )

        message = build_email_message(
            config=config,
            html_content="<h1>Report</h1>",
            markdown_content="# Report",
            subject="Daily Report",
        )

        self.assertEqual(message["Subject"], "Daily Report")
        self.assertEqual(message["From"], "sender@example.com")
        self.assertEqual(message["To"], "recipient@example.com")
        self.assertTrue(message.is_multipart())

    def test_send_message_uses_starttls_for_standard_smtp(self):
        config = EmailConfig(
            host="smtp.example.com",
            port=587,
            user="sender@example.com",
            password="app-password",
            recipients=("recipient@example.com",),
        )
        message = build_email_message(config, "<h1>Report</h1>", "Daily Report")
        server = Mock()
        server.__enter__ = Mock(return_value=server)
        server.__exit__ = Mock(return_value=None)

        with patch("smtplib.SMTP", return_value=server):
            send_message(config, message)

        server.starttls.assert_called_once()
        server.login.assert_called_once_with("sender@example.com", "app-password")
        server.send_message.assert_called_once_with(message)

    def test_send_email_report_skips_when_config_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            result = send_email_report(Path("missing.html"))

        self.assertFalse(result.sent)
        self.assertTrue(result.skipped)
        self.assertIn("Email skipped", result.message)


if __name__ == "__main__":
    unittest.main()
