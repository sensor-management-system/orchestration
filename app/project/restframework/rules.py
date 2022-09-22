"""Rules that can be used in the views for permissions and preconditions."""

from ..extensions.idl.roles import PermissionGroupRole
from .permissions.dsl import (
    GetPermissionGroupForConfiguration,
    GetPermissionGroupsFromDeviceOrPlatform,
    NoPrivateEntity,
    OwnerOfPrivateEntity,
    RequireUserForRequest,
    RestrictObjectTo,
    RoleInPermissionGroup,
    SuperUser,
)
from .preconditions.configurations import (
    AllDeviceMountsForConfigurationAreFinishedInThePast,
    AllDynamicLocationsForConfigurationAreFinishedInThePast,
    AllPlatformMountsForConfigurationAreFinishedInThePast,
    AllStaticLocationsForConfigurationAreFinishedInThePast,
)
from .preconditions.devices import AllMountsOfDeviceAreFinishedInThePast
from .preconditions.platforms import (
    AllMountsOfPlatformAreFinishedInThePast,
    AllUsagesAsParentPlatformInDeviceMountsFinishedInThePast,
    AllUsagesAsParentPlatformInPlatformMountsFinishedInThePast,
)

archive_device_permissions = RequireUserForRequest() & (
    RestrictObjectTo(
        SuperUser()
        | OwnerOfPrivateEntity()
        # We have the NoPrivateEntity test here so that
        # we don't need to ask for the groups & roles anymore.
        # (They should be fully covered by the Owner & SuperUser rules)
        | (
            NoPrivateEntity()
            & RoleInPermissionGroup(
                PermissionGroupRole.ADMIN, GetPermissionGroupsFromDeviceOrPlatform()
            )
        )
    )
)

archive_device_preconditions = AllMountsOfDeviceAreFinishedInThePast()

restore_device_permissions = RequireUserForRequest() & (
    RestrictObjectTo(
        SuperUser()
        | OwnerOfPrivateEntity()
        | (
            NoPrivateEntity()
            & RoleInPermissionGroup(
                PermissionGroupRole.ADMIN, GetPermissionGroupsFromDeviceOrPlatform()
            )
        )
    )
)

# There are no preconditions for restoring the devices.

archive_platform_permissions = RequireUserForRequest() & (
    RestrictObjectTo(
        SuperUser()
        | OwnerOfPrivateEntity()
        | (
            NoPrivateEntity()
            & RoleInPermissionGroup(
                PermissionGroupRole.ADMIN, GetPermissionGroupsFromDeviceOrPlatform()
            )
        )
    )
)

archive_platform_preconditions = (
    AllMountsOfPlatformAreFinishedInThePast()
    & AllUsagesAsParentPlatformInDeviceMountsFinishedInThePast()
    & AllUsagesAsParentPlatformInPlatformMountsFinishedInThePast()
)

restore_platform_permissions = RequireUserForRequest() & (
    RestrictObjectTo(
        SuperUser()
        | OwnerOfPrivateEntity()
        | (
            NoPrivateEntity()
            & RoleInPermissionGroup(
                PermissionGroupRole.ADMIN, GetPermissionGroupsFromDeviceOrPlatform()
            )
        )
    )
)

archive_configuration_permissions = RequireUserForRequest() & (
    RestrictObjectTo(
        SuperUser()
        | RoleInPermissionGroup(
            PermissionGroupRole.ADMIN, GetPermissionGroupForConfiguration()
        )
    )
)

restore_configuration_permissions = RequireUserForRequest() & (
    RestrictObjectTo(
        SuperUser()
        | RoleInPermissionGroup(
            PermissionGroupRole.ADMIN, GetPermissionGroupForConfiguration()
        )
    )
)

archive_configuration_preconditions = (
    AllDeviceMountsForConfigurationAreFinishedInThePast()
    & AllPlatformMountsForConfigurationAreFinishedInThePast()
    & AllStaticLocationsForConfigurationAreFinishedInThePast()
    & AllDynamicLocationsForConfigurationAreFinishedInThePast()
)
