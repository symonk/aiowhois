class WhoIsException(Exception): ...


class BadExecutableException(WhoIsException):
    """BadExecutableException is raised when a whois call with a custom
    command to run in the subprocess does not exist on $PATH."""
