# Permission Manager

|               | Read                  | Create               | Update               | Delete   | Download-Attachments|
|---------------|-----------------------|----------------------|----------------------|----------|---------------------|
| Public        | ALL                   | registered users     | PG-MEMBER, PG-ADMIN  | PG-ADMIN | registered users    |
| Internal      | registered users      | PG-MEMBER, PG-ADMIN  | PG-MEMBER, PG-ADMIN  | PG-ADMIN | registered users    |
| Private       | OWNER                 | registered users     | OWNER                | OWNER    | OWNER               |

**Special account: sms superuser**
superuser can manipulate or delete any object.

### Legend:

- PG: Permission Group
- PG-MEMBER: User is a member in a Group.
- PG-ADMIN: User is an admin in a Group.

## How to upgrade/downgrade a users

A normal user can be promoted to a superuser with this command:

```shell
python manage.py users upgradetosuperuser testuser@ufz.de
```

To downgrade a superuser to a normal user this command:

```shell
python manage.py users downgradetoruser testsuperuser@ufz.de
```

