# Permissions-Management in SMS

**Special account: sms superuser**
superuser can manipulate or delete any object.

## Visibility

SMS distinguishes between three types of`Visibility` listed as follows:

- Public: No sign in is required to view.
- Internal: sign in is required to view.
- Private: Only owner can view. of course beside the SMS-super-admin ;)

This Visibility level only effect the view of the object.

<span style="color:red"> Note: Private device can't be used in a Configuration. And a very Important thing to mention is that the private objects can be switched to internal or public but not the other way.</span>

### Permissions for private Objects

Only the Owner and SMS_superuser may delete or alter a private Object.

## Permissions for Platforms & Devices

The Permission-Groups `PG` come from the `IDL` Institute Decoupling Layer .

- Devices and Platforms may have more than one Group But a configuration has only one.
- Configuration can only be created with a corresponding Permission-Group.
- Devices and Platform, which has no group can be changed from all registered users and only be deleted from owner or sms-admin


<table>
<thead>
<tr>
<th>Action
</th><th>Not registered User
</th><th>Registered User
</th><th>PG-Member
</th><th>PG-Admin
</th><th>SMS-admin
</th></tr></thead><tbody>
<tr>
<td>
<b>Devices/Platform</b>:<br>View
</td><td>✓
</td><td>✓
</td><td>✓
</td><td>✓
</td><td>✓
</td></tr><tr>
<td>
<b>Devices/Platform</b>:<br>Create
</td><td>
</td><td>✓
</td><td>✓
</td><td>✓
</td><td>✓
</td></tr><tr>
<td>
 <b>Devices/Platform</b>:<br>Alter
   
</td><td>
</td><td>
</td><td>✓
</td><td>✓
</td><td>✓
</td></tr><tr>
<td>
 <b>Devices/Platform</b>:<br>Delete
</td><td>
</td><td>
</td><td>
</td><td>✓
</td><td>✓
</td>
</tbody></table>

<span style="color:green"> Note: all object underneath a parent will be treated as a part of this parent. So users need 
only to be in the parent-permission-group to alter or delete this object. An Example for such an Object is a 
custom-filed related to a device. </span>

### Permission for Configuration

To mount a device/platform on a configuration user **should** have the right to edit the Configuration and **should** 
be included in the related permission-group of them. <span style="color:red"> After this Step this 
device/platform will be active in a
configuration and due to this only the permission-group related to this configuration is the active and the groups of the device/platforms will be suspended till they will unmounted.</span>

## How to upgrade/downgrade a users

A normal user can be promoted to a superuser with this command:

```shell
python manage.py users upgrade-to-superuser testuser@ufz.de
```

To downgrade a superuser to a normal user this command:

```shell
python manage.py users downgrade-to-user testsuperuser@ufz.de
```

