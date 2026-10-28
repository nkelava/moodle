from django.db import migrations


def rename_content_type(apps, schema_editor, old_model, new_model):
    # The model was renamed in the earlier migrations (a swappable user model
    # cannot go through RenameModel), so move its content type by hand to keep
    # permissions and admin log entries attached to it.
    ContentType = apps.get_model('contenttypes', 'ContentType')
    db_alias = schema_editor.connection.alias
    if ContentType.objects.using(db_alias).filter(app_label='users', model=new_model).exists():
        return
    ContentType.objects.using(db_alias).filter(app_label='users', model=old_model).update(model=new_model)


def forwards(apps, schema_editor):
    rename_content_type(apps, schema_editor, 'customusers', 'user')


def backwards(apps, schema_editor):
    rename_content_type(apps, schema_editor, 'user', 'customusers')


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('users', '0008_auto_20210209_1816'),
    ]

    operations = [
        migrations.AlterModelTable(name='user', table=None),
        migrations.RunPython(forwards, backwards),
    ]
