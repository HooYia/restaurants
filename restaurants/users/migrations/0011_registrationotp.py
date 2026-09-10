from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_client_loyalty_points"),
    ]

    operations = [
        migrations.CreateModel(
            name="RegistrationOtp",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        unique=True,
                        help_text="Identifiant UUID unique pour la vérification OTP.",
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("data", models.JSONField()),
                ("otp_code", models.CharField(max_length=6)),
                ("purpose", models.CharField(default="register", max_length=50)),
                ("expires_at", models.DateTimeField()),
                ("is_verified", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.AddIndex(
            model_name="registrationotp",
            index=models.Index(fields=["email", "purpose"], name="users_registrat_email_purpose_idx"),
        ),
        migrations.AddIndex(
            model_name="registrationotp",
            index=models.Index(fields=["expires_at"], name="users_registrat_expires_at_idx"),
        ),
    ]
