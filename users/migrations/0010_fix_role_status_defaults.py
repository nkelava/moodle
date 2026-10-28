from django.db import migrations, models


def fix_role_and_status(apps, schema_editor):
    # The old defaults were enum members, so users created without an explicit
    # value (e.g. by createsuperuser) got 'RoleChoices.STUDENT' as role and an
    # empty status. Rewrite those rows to valid choice keys.
    User = apps.get_model('users', 'User')
    db_alias = schema_editor.connection.alias
    users = User.objects.using(db_alias)
    users.filter(role='RoleChoices.STUDENT').update(role='STUDENT')
    users.filter(role='RoleChoices.PROFESSOR').update(role='PROFESSOR')
    users.filter(status='').update(status='NONE')


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_rename_customusers_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('PROFESSOR', 'professor'), ('STUDENT', 'student')], default='STUDENT', max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('NONE', 'none'), ('FULL_TIME', 'full time'), ('PART_TIME', 'part time')], default='NONE', max_length=16),
        ),
        migrations.RunPython(fix_role_and_status, migrations.RunPython.noop),
    ]
