# Generated by Django 5.1.1 on 2024-11-10 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='average_score',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Average score that users gave the article', max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='total_score_count',
            field=models.IntegerField(blank=True, help_text='total number of users gave score', null=True),
        ),
        migrations.AddField(
            model_name='articlescore',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]