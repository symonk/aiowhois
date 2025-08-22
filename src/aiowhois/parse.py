import typing


def parse_domain(url: str) -> typing.Tuple[str, str]:
    """parse_domain attempts to read the appropriate domain
    and TLD from the given url."""
    return url, "com"
