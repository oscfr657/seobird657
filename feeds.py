from django.template.loader import render_to_string
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator


class RSSFeed(Feed):

    feed_type = feedgenerator.Rss201rev2Feed
    description_template = 'seobird657/feed_item_description.html'

    def __init__(self, page):
        super(RSSFeed, self).__init__()
        self.page = page
        self.title = page.title
        self.link = page.specific.index_page.full_url
        self.feed_url = page.full_url
        self.language = str(page.specific.language) if page.specific.language else 'en'

    def description(self):
        return render_to_string('seobird657/feed_description.html', {'obj': self.page})

    def author_name(self):
        return self.page.owner.get_full_name()

    def author_email(self):
        return self.page.owner.email

    def author_link(self):
        try:
            if self.page.specific.author_link:
                return self.page.specific.author_link
            else:
                return (
                    self.page.specific.author_page.full_url
                    if self.page.specific.author_page
                    else '/'
                )
        except AttributeError:
            return '/'

    def categories(self):
        try:
            return [tag.name for tag in self.page.specific.tags.all()]
        except AttributeError:
            return []

    def feed_copyright(self):
        try:
            return self.page.specific.feed_copyright
        except AttributeError:
            return (
                'Copyright (c) '
                + str(self.page.go_live_at.year)
                + ', '
                + self.page.owner.get_full_name()
            )

    def items(self):
        return (
            self.page.specific.index_page.get_descendants()
            .live()
            .public()
            .not_in_menu()
            .filter(go_live_at__isnull=False)
            .order_by('-first_published_at')
        )

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.full_url

    def item_guid(self, item):
        return item.full_url

    item_guid_is_permalink = True

    def item_author_name(self, item):
        return item.owner.get_full_name()

    def item_author_email(self, item):
        return item.owner.email

    def item_author_link(self, item):
        try:
            if item.specific.author_link:
                return item.specific.author_link
            else:
                return (
                    item.specific.author_page.full_url
                    if item.specific.author_page
                    else '/'
                )
        except AttributeError:
            return '/'

    # def item_enclosure_url(self, item):
    #    try:
    #        return item.
    #    except:
    #        return

    # def item_enclosure_length(self, item):
    #    try:
    #        return item.
    #    except:
    #        return

    # def item_enclosure_mime_type(self, item):
    #    try:
    #        return item.
    #    except:
    #        return

    def item_pubdate(self, item):
        if item.go_live_at:
            return item.go_live_at
        return item.first_published_at

    def item_updateddate(self, item):
        return item.last_published_at

    def item_categories(self, item):
        try:
            return [tag.name for tag in item.specific.tags.all()]
        except:
            return []

    def item_copyright(self, item):
        try:
            return item.specific.feed_copyright
        except AttributeError:
            return self.page.specific.feed_copyright
        except:
            return (
                'Copyright (c) '
                + str(item.first_published_at.year)
                + ', '
                + item.owner.get_full_name()
            )
