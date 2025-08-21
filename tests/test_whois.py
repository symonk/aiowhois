import pytest

from aiowhois import whois


@pytest.mark.asyncio
async def test_whois_placeholder():
    result = await whois("google.com", subprocess=True)
    assert result is not None, "foo"
