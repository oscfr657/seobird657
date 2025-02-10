
# SEOBird657 #

A small Wagtail app

## Compatible ##

### Tested with ###

``` Python
django==5.0.4
wagtail==6.0.2
wagtailmedia==0.15.1
```

## Installation ###
  
### Pip requirements ###

> pip install -r requirements.txt

### Django settings ###

To your settings file,

add to the INSTALLED_APPS

``` Python
    # wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',  # extra
    'wagtail.contrib.search_promotions',  # extra
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',

    # custom
    'seobird657',
    # seobird657 media file block
    'wagtailmedia',

```

add to the MIDDLEWARE settings

``` python
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
```

add to the TEMPLATES settings

``` python
    TEMPLATES = [
        {
            'OPTIONS': {
                'context_processors': [
                    'wagtail.contrib.settings.context_processors.settings',
            },
        },
    ]
```

#### I recommend ####

and set the WAGTAILIMAGES_FORMAT_CONVERSIONS setting

``` python
WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    'bmp': 'webp',
    'jpeg': 'webp',
    'jpg': 'webp',
    'JPG':'webp',
    'webp':'webp',
}
```

### Database configuration ###

> python3 manage.py migrate

### Search Index setup ###

> python3 manage.py update_index

### Django url ###

To the django projects' url.py add

``` python
from django.urls import path, re_path, include

# Wagtail
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from wagtail.contrib.sitemaps.views import sitemap
```

and

``` python
urlpatterns += [
    re_path('sitemap.xml', sitemap),
    #  Wagtail
    re_path(r'^wagtail/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),
  ]
```

### Collectstatic ###

> python3 manage.py collectstatic

### [Management commands](https://docs.wagtail.io/en/stable/reference/management_commands.html) ###

Some commands is good to have in cron to run once every hour.

``` bash
crontab -e
0 * * * * /path/to/env/bin/python3 /path/to/project/manage.py publish_scheduled_pages
0 * * * * /path/to/env/bin/python3 /path/to/project/manage.py search_garbage_collect
crontab -l
```

## For development ##

To the Django settings.py add

``` python
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

To the Django project url.py add

``` python
from django.conf import settings
from django.conf.urls.static import static
```

and at the bottom of the file add

``` python

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

### Build a new release ###

``` bash
    pip install black
    black . --skip-string-normalization
```

``` python
python3 -m build --sdist
```
