"""Instances of flask extensions to be used in the other code."""

from .auth import Auth
from .auth.mechanisms.apikey import ApikeyAuthMechanism
from .auth.mechanisms.openidconnect import OpenIdConnectAuthMechanism
from .auth.mechanisms.session import SessionAuthMechanism
from .idl import Idl
from .openidconnect import WellKnownUrlConfigLoader

well_known_url_config_loader = WellKnownUrlConfigLoader()
session_auth_mechanism = SessionAuthMechanism()
apikey_auth_mechanism = ApikeyAuthMechanism()
open_id_connect_auth_mechanism = OpenIdConnectAuthMechanism()
auth = Auth(
    mechanisms=[
        session_auth_mechanism,
        apikey_auth_mechanism,
        open_id_connect_auth_mechanism,
    ]
)
idl = Idl()
