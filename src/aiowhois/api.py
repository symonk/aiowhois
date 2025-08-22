from __future__ import annotations

import asyncio
import logging
import shutil

from .exceptions import BadExecutableException
from .exceptions import WhoIsException
from .parse import parse_domain
from .result import _tld_registry

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


# TODO: Error handling, narrow types etc.


async def whois(
    url: str,
    subprocess: bool = False,
    command: str = "whois",
) -> dict[str, str]:
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
    domain, tld = parse_domain(url)
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
        except Exception as exc:
            raise WhoIsException from exc
        out, err = await proc.communicate()
        if proc.returncode != 0 or out is None or err:
            raise WhoIsException("error querying whois server")
        cls = _tld_registry.get(tld)
        if cls is None:
            raise Exception("unsupported tld")
        parser = cls()
        parser.parse(out)
        return parser.as_dict()
    else:
        # TODO: Write an actual python client (need to store/generate) whois servers
        # per TLDs, stuff on $PATH i.e `whois` will be storing that internally.
        ...
    return {}
