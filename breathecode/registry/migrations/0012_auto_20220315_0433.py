# Generated by Django 3.2.12 on 2022-03-15 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0011_alter_asset_readme_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='last_synch_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='last_test_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='sync_status',
            field=models.CharField(blank=True,
                                   choices=[('PENDING', 'Pending'), ('ERROR', 'Error'), ('OK', 'Ok'),
                                            ('WARNING', 'Warning')],
                                   default=None,
                                   help_text='Internal state automatically set by the system based on sync',
                                   max_length=20,
                                   null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='test_status',
            field=models.CharField(blank=True,
                                   choices=[('PENDING', 'Pending'), ('ERROR', 'Error'), ('OK', 'Ok'),
                                            ('WARNING', 'Warning')],
                                   default=None,
                                   help_text='Internal state automatically set by the system based on test',
                                   max_length=20,
                                   null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('UNNASIGNED', 'Unnasigned'), ('DRAFT', 'Draft'), ('OK', 'Ok')],
                                   default='DRAFT',
                                   help_text='Related to the publishing of the asset',
                                   max_length=20),
        ),
        migrations.AlterField(
            model_name='asset',
            name='status_text',
            field=models.TextField(blank=True,
                                   default=None,
                                   help_text='Used by the sych status to provide feedback',
                                   null=True),
        ),
    ]
