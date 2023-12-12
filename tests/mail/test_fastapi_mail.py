from nextpy.backend.module.mail.config import EmailConfig


def test_configuration(mail_config):
    conf = EmailConfig(**mail_config)
    assert conf.MAIL_USERNAME == "example@test.com"
    assert conf.MAIL_PORT == 25
