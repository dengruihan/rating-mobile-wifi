from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_wifi_model_approval_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]