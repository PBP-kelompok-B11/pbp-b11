from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('rafi_player', '0003_auto_20251026_1256'),  # sesuaikan
    ]

    operations = [

        migrations.AddField(
            model_name='player',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='thumbnails/'),
        ),
    ]
