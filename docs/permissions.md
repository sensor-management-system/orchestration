# Permission Manager

|               | Read                  | Create               | Update               | Delete   |
|---------------|-----------------------|----------------------|----------------------|----------|
| Public        | ALL                   | registered users     | PG-MEMBER, PG-ADMIN  | PG-ADMIN | 
| Internal      | registered users      | PG-MEMBER, PG-ADMIN  | PG-MEMBER, PG-ADMIN  | PG-ADMIN | 
| Private       | OWNER                 | registered users     | OWNER                | OWNER    |

**Special account: sms superuser**
superuser can manipulate or delete any object.

### Legend:

- PG: Permission Group
- PG-MEMBER: User is a member in a Group.
- PG-ADMIN: User is an admin in a Group.

## How to upgrade/downgrade a users

A normal user can be promoted to a superuser with this command:

```shell
python manage.py users upgrade-to-superuser testuser@ufz.de
```

To downgrade a superuser to a normal user this command:

```shell
python manage.py users downgrade-to-user testsuperuser@ufz.de
```

