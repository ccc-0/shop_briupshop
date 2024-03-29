# Generated by Django 2.2.6 on 2019-10-11 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='created_times',
            field=models.DateTimeField(verbose_name='录入时间'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='one_typename',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='one', to='goods.GoodsType', verbose_name='一级分类'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='sale_nums',
            field=models.IntegerField(verbose_name='销量'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='three_typename',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='three', to='goods.GoodsType', verbose_name='三级分类'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='two_typename',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='two', to='goods.GoodsType', verbose_name='二级分类'),
        ),
        migrations.AlterField(
            model_name='goodstype',
            name='uper_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsType', verbose_name='上级编号'),
        ),
    ]
