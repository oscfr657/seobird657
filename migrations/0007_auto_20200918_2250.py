# Generated by Django 3.1 on 2020-09-18 20:50

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('wagtailcore', '0052_pagelogentry'),
        ('seobird657', '0006_auto_20200629_2004'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSSBirdPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('language', models.CharField(blank=True, max_length=5, null=True)),
                ('author', models.CharField(blank=True, max_length=128, null=True)),
                ('author_email', models.CharField(blank=True, max_length=128, null=True)),
                ('author_link', models.URLField(blank=True, null=True)),
                ('feed_copyright', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RSSBirdPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='seobird657.rssbirdpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seobird657_rssbirdpagetag_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='rssbirdpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='seobird657.RSSBirdPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
