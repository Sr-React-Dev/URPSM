# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ureview', '0003_reviewedorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewedorder',
            name='type',
            field=models.CharField(max_length=1, choices=[(b'U', 'Ticketed and solved for server owner'), (b'S', 'Ticketed and solved for shop owner'), (b'C', 'Ticketed and solved for phone owner'), (b'D', 'Successfully Delivered '), (b'R', 'Successfully Repaired ')]),
        ),
        migrations.AlterField(
            model_name='serverreview',
            name='server',
            field=models.ForeignKey(related_name='review_server', default=False, to='server.Server'),
        ),
        migrations.AlterField(
            model_name='shopreview',
            name='shop',
            field=models.ForeignKey(related_name='review_shop', default=False, to='shop.Shop'),
        ),
    ]
