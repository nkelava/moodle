from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20210130_0051'),
        # Run after the foreign key to Courses exists so RenameModel updates it.
        ('enrollments', '0001_initial'),
        # Keep the three model renames in one fixed order (users, courses, enrollments).
        ('users', '0009_rename_customusers_user'),
    ]

    operations = [
        migrations.RenameModel('Courses', 'Course'),
    ]
