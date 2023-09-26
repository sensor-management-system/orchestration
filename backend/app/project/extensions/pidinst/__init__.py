# SPDX-FileCopyrightText: 2023
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
#
# SPDX-License-Identifier: HEESIL-1.0

"""Extension for pidinst."""

from flask import current_app

from ...api.models import Configuration, Device, Platform


class Pidinst:
    """
    Flask extension for the pidinst support.

    This should be the way to interact with various
    kinds of pidinst services (depending with one is configured
    to be used).

    First implementations are:
    - usage of b2inst (if we have a token for it)
    - usage of a normal pid (without external metadata) in case we nothing else.
    """

    def __init__(self, pid, b2inst, app=None):
        """
        Init it with the extensions to handle b2inst or normal pids.

        Which one is used later depends on the app config.
        """
        self.pid = pid
        self.b2inst = b2inst

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Init the sub components."""
        self.b2inst.init_app(app)
        self.pid.init_app(app)

    def create_pid(self, instrument):
        """Create a pid for the instrument."""
        if self.b2inst.token:
            return self.b2inst.create_pid(instrument)
        else:
            sms_paths = {
                Device: "devices",
                Platform: "platforms",
                Configuration: "configurations",
            }
            base_url = current_app.config["SMS_FRONTEND_URL"]
            url = f"{base_url}/{sms_paths[type(instrument)]}/{instrument.id}"
            return self.pid.create(url)

    def has_external_metadata(self, instrument):
        """Return true if the instrument has external metadata that may need updates."""
        if self.b2inst.token:
            return self.b2inst.has_external_metadata(instrument)
        else:
            return False

    def update_external_metadata(self, instrument, run_async=True):
        """Update the external metadata."""
        if self.b2inst.token:
            self.b2inst.update_external_metadata(instrument, run_async=run_async)
        else:
            pass

    def check_availability(self):
        """Raise an HTTPError exception if the service is not avaiable."""
        if self.b2inst.token:
            self.b2inst.check_availability()
        else:
            self.pid.list()
