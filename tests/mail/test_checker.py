import pytest
from nextpy.backend.module.mail.email_utils.email_check import EmailNotValidError
# test_checker.py and other test files


from nextpy.backend.module.mail.errors import DBProvaiderError
from jinja2 import Environment, FileSystemLoader 

@pytest.mark.asyncio
async def test_default_checker(default_checker):
    await default_checker.fetch_temp_email_domains()
    assert default_checker.TEMP_EMAIL_DOMAINS != []

    email = "jaeebawdekar2511@gmail.com"
    domain = email.split("@")[-1]

    assert await default_checker.is_disposable(email) is False
    assert await default_checker.is_blocked_domain(domain) is False
    assert await default_checker.is_blocked_address(email) is False
    assert await default_checker.check_mx_record(domain) is True

    with pytest.raises(NotImplementedError):
        default_checker.catch_all_check()

    await default_checker.add_temp_domain([domain])

    assert await default_checker.is_disposable(email) is True
    assert await default_checker.is_blocked_domain(domain) is False
    assert await default_checker.is_blocked_address(email) is False
    assert await default_checker.check_mx_record(domain) is True

    await default_checker.blacklist_add_domain(domain)

    assert await default_checker.is_blocked_domain(domain) is True
    assert await default_checker.is_blocked_address(email) is False
    assert await default_checker.check_mx_record(domain) is True

    await default_checker.blacklist_add_email(email)

    assert await default_checker.is_blocked_address(email) is True
    assert await default_checker.check_mx_record(domain) is True

    assert default_checker.validate_email(email) is True

    with pytest.raises(EmailNotValidError):
        default_checker.validate_email("test#mail.com")

    with pytest.raises(DBProvaiderError):
        await default_checker.close_connections()
