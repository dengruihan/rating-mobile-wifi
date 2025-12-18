from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_user_avatar_review_is_anonymous"),
    ]

    operations = [
        migrations.AddField(
            model_name="wifimodel",
            name="approval_status",
            field=models.CharField(
                choices=[("pending", "待审核"), ("approved", "已通过"), ("rejected", "已驳回")],
                default="approved",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="wifimodel",
            name="approved_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="wifimodel",
            name="approved_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="approved_wifi_models",
                to="api.user",
            ),
        ),
        migrations.AddField(
            model_name="wifimodel",
            name="rejection_reason",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="wifimodel",
            name="submitted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="wifimodel",
            name="submitted_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="submitted_wifi_models",
                to="api.user",
            ),
        ),
    ]


