# Permission Manager

|               | Read                  | Create               | Update               | Delete   | Download-Attachments|
|---------------|-----------------------|----------------------|----------------------|----------|---------------------|
| Public        | ALL                   | registered users     | DP-MEMBER, DP-ADMIN  | DP-ADMIN | registered users    |
| Internal      | registered users      | DP-MEMBER, DP-ADMIN  | DP-MEMBER, DP-ADMIN  | DP-ADMIN | registered users    |
| Private       | OWNER                 | registered users     | OWNER                | OWNER    | OWNER               |

**Special account: sms superuser**
superuser can manipulate or delete any object.

## How to upgrade/downgrade a users

A normal user can be promoted to a superuser with this command:

```shell
python manage.py users upgradetosuperuser testuser@ufz.de
```

To downgrade a superuser to a normal user this command:

```shell
python manage.py users downgradetoruser testsuperuser@ufz.de
```