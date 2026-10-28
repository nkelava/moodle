from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0001_initial'),
        ('courses', '0003_rename_courses_course'),
    ]

    operations = [
        migrations.RenameModel('Enrollments', 'Enrollment'),
    ]
