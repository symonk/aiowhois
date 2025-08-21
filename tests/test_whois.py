import pytest
from aiowhois import whois


@pytest.mark.asyncio
async def test_whois_placeholder():
    await whois("google.com", subprocess=True)
