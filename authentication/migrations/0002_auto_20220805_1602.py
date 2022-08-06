from django.db import migrations


def autopopulate_roles(apps, schema_editor):
    Role = apps.get_model("authentication", "Role")
    roles = [Role(name="admin"), Role(name="user")]
    for role in roles:
        role.save()


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [migrations.RunPython(autopopulate_roles)]
