import functools
from datetime import datetime, timedelta
from base64 import b64encode, urlsafe_b64encode
from hashlib import sha256
from dataclasses import dataclass
import os
import re


def timed_cache(**timedelta_kwargs):
    """
    Decorator that caches a function's return value each time it is called.
    If called within the timedelta, the cached value is returned instead.

    Source: https://gist.github.com/Morreski/c1d08a3afa4040815eafd3891e16b945
    """

    def _wrapper(f):
        update_delta = timedelta(**timedelta_kwargs)
        next_update = datetime.utcnow() - update_delta
        # Apply @lru_cache to f with no cache size limit
        f = functools.lru_cache(None)(f)

        @functools.wraps(f)
        def _wrapped(*args, **kwargs):
            nonlocal next_update
            now = datetime.utcnow()
            if now >= next_update:
                f.cache_clear()
                next_update = now + update_delta
            return f(*args, **kwargs)

        return _wrapped

    return _wrapper


def get_creds_hash(username: str, password: str) -> str:
    """
    Generates a hash of the username and password to be used for authentication.

    :param username: The username to hash.
    :param password: The password to hash.
    :return: The hash of the username and password.
    """
    return (
        b64encode(sha256((username + password).encode("utf8")).digest(), altchars=b"ab")
        .decode("ascii")
        .strip("=")
    )


def generate_code_verifier():
    """
    Generates a code verifier to be used in the OAuth2 authentication process.

    :return: The code verifier.
    """
    code_verifier = urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    return re.sub("[^a-zA-Z0-9]+", "", code_verifier)


def get_code_challenge(code_verifier: str):
    """
    Generates a code challenge to be used in the OAuth2 authentication process.

    :param code_verifier: The code verifier to generate the code challenge from.
    :return: The code challenge.
    """
    code_challenge = sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = urlsafe_b64encode(code_challenge).decode("utf-8")
    return code_challenge.replace("=", "")


class ScheduleError(Exception):
    """Raised when authentication fails."""

    pass


@dataclass
class ITMOEvent:
    date: str
    pair_id: int
    subject: str
    subject_id: int
    note: str | None
    type: str
    time_start: str
    time_end: str
    teacher_id: int
    teacher_name: str
    room: str
    building: str
    format: str
    work_type: str
    work_type_id: int
    group: str
    flow_type_id: int
    flow_id: int
    zoom_url: str | None
    zoom_password: str | None
    zoom_info: str | None
    bld_id: int
    format_id: int
    main_bld_id: int
