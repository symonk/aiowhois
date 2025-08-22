from __future__ import annotations

import asyncio
import shutil

from .exceptions import BadExecutableException
from .exceptions import WhoIsException
from .parse import parse_domain
from .result import WhoisResult


async def whois(
    url: str,
    subprocess: bool = False,
    command: str = "whois",
) -> WhoisResult | None:
    """whois dispatches an asynchronous WHOIS protocol query.
    The query is typically dispatched over a TCP socket on port
    43 to the whois server responsible for TLDs.

    In cases of `thin` responses, the returned server of the registrar
    will be implicitly looked up.

    whois can use an arbitrary command available on $PATH to call out to for
    handling the lookup, alternatively it exposes a pure python client to
    establish the socket and handle communication.  By default the command
    to run is `whois`.
    """
    domain = parse_domain(url)
    if subprocess:
        executable = await asyncio.to_thread(shutil.which, command)
        if executable is None:
            raise BadExecutableException
        positional = (executable, domain)
        try:
            proc = await asyncio.create_subprocess_exec(
                *positional,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except Exception as exc:  # TODO: Narrow in scope later
            raise WhoIsException from exc
        out, err = await proc.communicate()
        if proc.returncode != 0 or out is None or not err:
            raise WhoIsException("error querying whois server")
        return WhoisResult.from_bytes(out)
    else:
        # TODO: Write an actual python client.
        ...
    return None
