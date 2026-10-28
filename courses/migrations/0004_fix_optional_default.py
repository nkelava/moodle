from django.db import migrations, models


def fix_optional(apps, schema_editor):
    # The old default was the enum member itself, stored as 'OptionalChoices.NO'.
    Course = apps.get_model('courses', 'Course')
    db_alias = schema_editor.connection.alias
    courses = Course.objects.using(db_alias)
    courses.filter(optional='OptionalChoices.NO').update(optional='NO')
    courses.filter(optional='OptionalChoices.YES').update(optional='YES')


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_rename_courses_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='optional',
            field=models.CharField(choices=[('YES', 'yes'), ('NO', 'no')], default='NO', max_length=8),
        ),
        migrations.RunPython(fix_optional, migrations.RunPython.noop),
    ]
