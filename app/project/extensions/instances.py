"""Instances of flask extensions to be used in the other code."""

from .auth import Auth
from .auth.mechanisms.openidconnect import OpenIdConnectAuthMechanism
from .auth.mechanisms.session import SessionAuthMechanism

session_auth_mechanism = SessionAuthMechanism()
open_id_connect_auth_mechanism = OpenIdConnectAuthMechanism()

auth = Auth(mechanisms=[session_auth_mechanism, open_id_connect_auth_mechanism])
