"""Various views for some more specific usecases."""

from .additional_configurations_routes import (  # noqa: F401
    additional_configuration_routes,
)
from .additional_devices_routes import additional_devices_routes  # noqa: F401
from .additional_platforms_routes import additional_platforms_routes  # noqa: F401
from .additional_site_routes import additional_site_routes  # noqa: F401
from .docs import docs_routes  # noqa: F401
from .download_files import download_routes  # noqa: F401
from .free_text_field_routes import free_text_field_routes  # noqa: F401
from .login import login_routes  # noqa: F401
from .sensorml import sensor_ml_routes  # noqa: F401
from .upload_files import upload_routes  # noqa: F401
