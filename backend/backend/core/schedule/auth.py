import html
import re
import urllib.parse
import requests

from .utils import (
    ScheduleError,
    timed_cache,
    generate_code_verifier,
    get_code_challenge,
)

_CLIENT_ID = "student-personal-cabinet"
_REDIRECT_URI = "https://my.itmo.ru/login/callback"
_PROVIDER = "https://id.itmo.ru/auth/realms/itmo"


@timed_cache(minutes=55)
def get_access_token(username: str, password: str):
    code_verifier = generate_code_verifier()
    code_challenge = get_code_challenge(code_verifier)

    try:
        auth_resp = requests.get(
            _PROVIDER + "/protocol/openid-connect/auth",
            params=dict(
                protocol="oauth2",
                response_type="code",
                client_id=_CLIENT_ID,
                redirect_uri=_REDIRECT_URI,
                scope="openid",
                state="im_not_a_browser",
                code_challenge_method="S256",
                code_challenge=code_challenge,
            ),
        )
    except requests.exceptions.ConnectionError:
        raise ScheduleError("Could not connect to the authentication server.")
    auth_resp.raise_for_status()

    form_action = html.unescape(
        re.search('<form\s+.*?\s+action="(.*?)"', auth_resp.text, re.DOTALL).group(1)
    )

    form_resp = requests.post(
        url=form_action,
        data=dict(username=username, password=password),
        cookies=auth_resp.cookies,
        allow_redirects=False,
    )
    if form_resp.status_code != 302:
        # raise ValueError(
        #     f"Wrong Keycloak form response: {form_resp.status_code} {form_resp.text}"
        # )
        raise ScheduleError(
            "Authentication failed. Please check your username and password."
        )

    url_redirected_to = form_resp.headers["Location"]
    query = urllib.parse.urlparse(url_redirected_to).query
    redirect_params = urllib.parse.parse_qs(query)
    auth_code = redirect_params["code"][0]

    token_resp = requests.post(
        url=_PROVIDER + "/protocol/openid-connect/token",
        data=dict(
            grant_type="authorization_code",
            client_id=_CLIENT_ID,
            redirect_uri=_REDIRECT_URI,
            code=auth_code,
            code_verifier=code_verifier,
        ),
        allow_redirects=False,
    )
    token_resp.raise_for_status()
    result = token_resp.json()
    return result["access_token"]
