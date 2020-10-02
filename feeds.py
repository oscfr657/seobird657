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
        self.link = page.get_parent().full_url
        self.feed_url = page.full_url

    def description(self):
        rendered = render_to_string('seobird657/feed_description.html', { 'obj': self.page })
        return rendered

    def author_name(self):
        return str(self.page.specific.author) if self.page.specific.author else self.page.owner.username
    
    def author_email(self):
        try:
            return str(self.page.specific.author_email) if self.page.specific.author_email else self.page.owner.email
        except AttributeError:
            return self.page.owner.email
    
    def author_link(self):
        try:
            return (self.page.specific.author_link) if self.page.specific.author_link else '/'
        except AttributeError:
            return '/'
    
    def categories(self):
        try:
            return [ tag.name for tag in self.page.specific.tags.all() ]
        except AttributeError:
            return []
    
    def feed_copyright(self):
        try:
            return self.page.specific.feed_copyright
        except AttributeError:
            try:
                return 'Copyright (c) ' + str(self.page.go_live_at.year) + ', ' + self.page.specific.author
            except AttributeError:
                return 'Copyright (c) ' + str(self.page.go_live_at.year) + ', ' + self.page.owner.username

    def items(self):
        return self.page.get_parent().get_descendants().live(
            ).public().not_in_menu().filter(go_live_at__isnull=False).order_by(
                            '-first_published_at')

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.full_url

    def item_guid(self, item):
        return item.full_url
    
    item_guid_is_permalink = True

    def item_author_name(self, item):
        try:
            return str(item.specific.author) if item.specific.author else item.owner.username
        except AttributeError:
            return item.owner.username
        
    def item_author_email(self, item):
        try:
            return str(item.specific.author_email) if item.specific.author_email else item.owner.email
        except AttributeError:
            return item.owner.email
        

    def item_author_link(self, item):
        try:
            return (item.specific.author_link) if item.specific.author_link else '/'
        except AttributeError:
            return '/'
        
    
    #def item_enclosure_url(self, item):
    #    try:
    #        return item.
    #    except:
    #        return
    
    #def item_enclosure_length(self, item):
    #    try:
    #        return item.
    #    except:
    #        return
    
    #def item_enclosure_mime_type(self, item):
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
            return [ tag.name for tag in item.specific.tags.all() ]
        except:
            return []
    
    def item_copyright(self, item):
        try:
            return item.specific.feed_copyright
        except:
            try:
                return 'Copyright (c) ' + str(item.go_live_at.year) + ', ' + str(item.specific.author)
            except:
                return 'Copyright (c) ' + str(item.first_published_at.year) + ', ' + item.owner.username

