# from typing import Optional

# from aiosmtplib.api import DEFAULT_TIMEOUT
# from jinja2 import Environment, FileSystemLoader
# from pydantic import DirectoryPath, EmailStr, conint
# from pydantic_settings import BaseSettings as Settings


# class EmailConfig(Settings):
#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_PORT: int
#     MAIL_SERVER: str
#     MAIL_STARTTLS: bool
#     MAIL_SSL_TLS: bool
#     MAIL_DEBUG: conint(gt=-1, lt=2) = 0  # type: ignore
#     MAIL_FROM: EmailStr
#     MAIL_FROM_NAME: Optional[str] = None
#     TEMPLATE_FOLDER: Optional[DirectoryPath] = None
#     SUPPRESS_SEND: conint(gt=-1, lt=2) = 0  # type: ignore
#     USE_CREDENTIALS: bool = True
#     VALIDATE_CERTS: bool = True
#     TIMEOUT: int = DEFAULT_TIMEOUT

#     def template_engine(self) -> Environment:
#         """
#         Return template environment
#         """
#         folder = self.TEMPLATE_FOLDER
#         if not folder:
#             raise ValueError(
#                 "Class initialization did not include a ``TEMPLATE_FOLDER`` ``PathLike`` object."
#             )
#         template_env = Environment(loader=FileSystemLoader(folder))
#         return template_env
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, DirectoryPath, conint
from aiosmtplib.api import DEFAULT_TIMEOUT
from jinja2 import Environment, FileSystemLoader


class EmailConfig(BaseModel):
    MAIL_USERNAME: str = Field(..., description="The email username")
    MAIL_PASSWORD: str = Field(..., description="The email password")
    MAIL_PORT: int = Field(..., description="The email server port")
    MAIL_SERVER: str = Field(..., description="The email server address")
    MAIL_STARTTLS: bool = Field(False, description="Enable STARTTLS")
    MAIL_SSL_TLS: bool = Field(False, description="Enable SSL/TLS")
    MAIL_DEBUG: conint(gt=-1, lt=2) = Field(0, description="Debug level for mail")
    MAIL_FROM: EmailStr = Field(..., description="The email from address")
    MAIL_FROM_NAME: Optional[str] = Field(None, description="The name of the sender")
    TEMPLATE_FOLDER: Optional[DirectoryPath] = Field(None, description="Path to the template folder")
    SUPPRESS_SEND: conint(gt=-1, lt=2) = Field(0, description="Suppress sending emails")
    USE_CREDENTIALS: bool = Field(True, description="Use credentials for email")
    VALIDATE_CERTS: bool = Field(True, description="Validate certificates")
    TIMEOUT: int = Field(DEFAULT_TIMEOUT, description="Timeout for email operations")

    def template_engine(self) -> Environment:
        """
        Return template environment
        """
        if not self.TEMPLATE_FOLDER:
            raise ValueError("TEMPLATE_FOLDER is not set.")
        return Environment(loader=FileSystemLoader(self.TEMPLATE_FOLDER))
