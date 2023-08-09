# SPDX-FileCopyrightText: 2022
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Instances of flask extensions to be used in the other code."""

from .auth import Auth
from .auth.mechanisms.apikey import ApikeyAuthMechanism
from .auth.mechanisms.openidconnect import OpenIdConnectAuthMechanism
from .auth.mechanisms.session import SessionAuthMechanism
from .b2inst.extension import B2Inst
from .idl import Idl
from .openidconnect import WellKnownUrlConfigLoader
from .pid import Pid
from .pidinst import Pidinst
from .redirect import RemoveSlashRedirectMiddlware

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
pidinst = Pidinst(pid=Pid(), b2inst=B2Inst())
remove_slash_redirect_middlware = RemoveSlashRedirectMiddlware()
