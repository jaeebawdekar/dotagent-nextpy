import aiosmtplib

from .config import EmailConfig
from .errors import ConnectionErrors, PydanticClassRequired


class Connection:
    """
    Manages Connection to provided email service with its credentials
    """

    def __init__(self, settings: EmailConfig) -> None:
        if not isinstance(settings, EmailConfig):
            raise PydanticClassRequired(
                "Configuration should be provided from EmailConfig class"
            )
        self.settings = settings

    async def __aenter__(self) -> "Connection":
        """
        Setting up a connection
        """
        await self._configure_connection()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Closing the connection
        """
        if not self.settings.SUPPRESS_SEND:  # for test environ
            await self.session.quit()

    async def _configure_connection(self) -> None:
        try:
            self.session = aiosmtplib.SMTP(
                hostname=self.settings.MAIL_SERVER,
                timeout=self.settings.TIMEOUT,
                port=self.settings.MAIL_PORT,
                use_tls=self.settings.MAIL_SSL_TLS,
                start_tls=self.settings.MAIL_STARTTLS,
                validate_certs=self.settings.VALIDATE_CERTS,
            )

            if not self.settings.SUPPRESS_SEND:  # for test environ
                await self.session.connect()

                if self.settings.USE_CREDENTIALS:
                    await self.session.login(
                        self.settings.MAIL_USERNAME, self.settings.MAIL_PASSWORD
                    )

        except Exception as error:
            raise ConnectionErrors(
                f"Exception raised {error}, check your credentials or email service configuration"
            )
