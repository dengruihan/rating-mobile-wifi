from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="review",
            name="is_anonymous",
            field=models.BooleanField(default=False),
        ),
    ]


