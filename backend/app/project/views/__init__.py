# SPDX-FileCopyrightText: 2024
# - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
# - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
# - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
# - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
#
# SPDX-License-Identifier: EUPL-1.2

"""Various views for some more specific usecases."""

from .activity_routes import activity_routes  # noqa: F401
from .additional_configurations_routes import (
    additional_configuration_routes,
)  # noqa: F401
from .additional_devices_routes import additional_devices_routes  # noqa: F401
from .additional_platforms_routes import additional_platforms_routes  # noqa: F401
from .additional_site_routes import additional_site_routes  # noqa: F401
from .docs import docs_routes  # noqa: F401
from .download_files import download_routes  # noqa: F401
from .free_text_field_routes import free_text_field_routes  # noqa: F401
from .login import login_routes  # noqa: F401
from .proxy import proxy_routes  # noqa: F401
from .sensorml import sensor_ml_routes  # noqa: F401
from .upload_files import upload_routes  # noqa: F401
