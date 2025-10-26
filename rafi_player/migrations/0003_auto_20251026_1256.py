from django.db import migrations, models
import django.db.models.deletion
from django.contrib.auth.models import User

class Migration(migrations.Migration):

    dependencies = [
        ('rafi_player', '0002_alter_player_posisi'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
