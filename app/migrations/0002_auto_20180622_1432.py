# Generated by Django 2.0.3 on 2018-05-25 09:56

import os

from django.conf import settings
from django.core.files.images import ImageFile
from django.db import migrations

from app.consts import app_config_context
from app.manager.config_manager import cache_config
from app.manager.ct_manager import update_one_to_many_relation_model


def init_config(apps, schema_editor):
    Config = apps.get_model("app", "Config")
    db_alias = schema_editor.connection.alias

    Config.objects.using(db_alias).bulk_create([
        # 顶部图标栏
        Config(name=app_config_context['top_ico'],
               config='{ "left": { "logo": "{%img|name=logo_white %}", "blog_name": "{%text| 文字标题 | style=font-size:18px %}" }, "right": [ { "img": "{%fa|fab fa-github|style=color:#ffffff;font-size:24px %}", "url": "https://github.com/gojuukaze/DeerU" } ] }'),
        # 顶部导航栏
        Config(name=app_config_context['top_menu'],
               config='[ { "url": "/", "name": "首页", "img": "{% fa|fas fa-home %}" }, { "name": "折叠菜单", "img": "{% fa|fas fa-list %}", "children": [ { "name": "默认分类", "url": "{% cat|name=默认分类|url%}" }, { "line": "line" }, { "name": "DeerU", "url": "{% tag|DeerU|url%}" } ] } ]'),
        # 全局变量
        Config(name=app_config_context['global_value'],
               config='{ "title": "Deeru - 开源博客系统", "blog_name": "Deeru - 开源博客系统", "nickname": "gojuukaze" }'),

        # 其他配置
        Config(name=app_config_context['common_config'],
               config='{ "base_theme": "base_theme", "baidu_auto_push": 0 }'),
    ])
    for config in Config.objects.all():
        cache_config(config, True)


def upload_img(model, name, path):
    with open(path, 'rb')as f:
        img = ImageFile(f)
        a = model(name=name)
        a.img.save(name, img)


def init_img(apps, schema_editor):
    Album = apps.get_model("app", "Album")
    base_dir = settings.BASE_DIR
    upload_img(Album, 'logo_white.png', os.path.join(base_dir, 'logo_white.png'))
    upload_img(Album, 'logo_black.png', os.path.join(base_dir, 'logo_black.png'))

    upload_img(Album, 'deeru_green.png', os.path.join(base_dir, 'deeru_green.png'))


def init_content(apps, schema_editor):
    Category = apps.get_model("app", "Category")
    c = Category.objects.create(name='默认分类')

    Tag = apps.get_model("app", "Tag")
    t = Tag.objects.create(name='DeerU')

    Album = apps.get_model("app", "Album")
    logo_black = Album.objects.get(name='logo_black.png')
    deeru_green = Album.objects.get(name='deeru_green.png')

    Article = apps.get_model("app", "Article")
    a = Article.objects.create(title='欢迎使用DeerU',
                               content='<p><img src="%s" data-name="logo_black.png" data-id="2" style="width: 229px;" class="fr-fic fr-dib"></p><p><br></p><hr><p style="text-align: center;"><br></p><p style="text-align: center;"><span style="font-size: 18px;"><strong>感谢你试用DeerU<span class="fr-emoticon fr-deletable">😀</span> </strong> </span></p><p style="text-align: center;"><strong><span style="font-size: 18px;">DeerU是一个开源的博客系统</span></strong></p><p style="text-align: center;"><strong><span style="font-size: 18px;">目前最新版DeerU为Alpha版，可能会存在一些BUG</span></strong></p><p style="text-align: center;"><strong><span style="font-size: 18px;">如果你有什么问题或者建议欢迎联系反馈给我</span></strong></p><p style="text-align: center;"><br></p><p style="text-align: center;"><strong><span style="font-size: 18px;">GITHUB：<a data-fr-linked="true" href="https://github.com/gojuukaze/DeerU​​​">https://github.com/gojuukaze/DeerU</a></span></strong></p><p style="text-align: center;"><strong><span style="font-size: 18px;">ISSUES：<a href="https://github.com/gojuukaze/DeerU/issues" target="_blank">https://github.com/gojuukaze/DeerU/issues</a></span></strong></p>' % logo_black.img.url,
                               summary='感谢你试用DeerU😀<br>DeerU是一个开源的博客系统<br>目前最新版DeerU为Alpha版，可能会存在一些BUG<br>如果你有什么问题或者建议欢迎联系反馈给我<br>...',
                               image=deeru_green.img.url
                               )
    ArticleMeta = apps.get_model("app", "ArticleMeta")
    ArticleMeta.objects.create(article_id=a.id)

    ArticleCategory = apps.get_model("app", "ArticleCategory")
    update_one_to_many_relation_model(ArticleCategory, 'article_id', a.id, 'category_id', [c.id],
                                      lambda x: x, [])
    ArticleTag = apps.get_model("app", "ArticleTag")
    update_one_to_many_relation_model(ArticleTag, 'article_id', a.id, 'tag_id', [t.id],
                                      lambda x: x, [])


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_img),
        migrations.RunPython(init_content),
        migrations.RunPython(init_config),

    ]
