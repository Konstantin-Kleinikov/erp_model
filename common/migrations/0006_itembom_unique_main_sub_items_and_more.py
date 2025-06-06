# Generated by Django 5.2.1 on 2025-05-17 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_itembom'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='itembom',
            constraint=models.UniqueConstraint(fields=('main_item', 'sub_item'), name='unique_main_sub_items'),
        ),
        migrations.AddConstraint(
            model_name='itembom',
            constraint=models.CheckConstraint(condition=models.Q(('main_item', models.F('sub_item')), _negated=True), name='prevent_self_follow'),
        ),
    ]
