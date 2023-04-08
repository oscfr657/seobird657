from django.db import models
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail.search import index

from wagtail.admin.panels import FieldPanel, PageChooserPanel

from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from .blocks import CodeBirdBlock, HTMLBirdBlock, MediaFileBirdBlock

from .feeds import RSSFeed


@register_setting
class SeoSettings(BaseSiteSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        FieldPanel('logo'),
    ]


class BirdMixin(models.Model):
    author_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    intro = RichTextField(
        blank=True,
        null=True,
        features=[
            'h2',
            "h3",
            "h4",
            "bold",
            "italic",
            "superscript",
            "subscript",
            "strikethrough",
            "ol",
            "ul",
            "hr",
            "link",
            "document-link",
            "blockquote",
        ],
    )
    show_breadcrumbs = models.BooleanField(default=False)
    show_cover = models.BooleanField(default=False)
    show_date = models.BooleanField(default=False)
    exclude_from_sitemap = models.BooleanField(default=False)

    class Meta:
        abstract = True

    search_fields = [
        index.SearchField('intro'),
    ]
    content_panels = [
        FieldPanel('owner'),
        PageChooserPanel('author_page'),
        FieldPanel('image'),
        FieldPanel('intro', classname="full"),
    ]
    settings_panels = [
        FieldPanel('show_breadcrumbs'),
        FieldPanel('show_cover'),
        FieldPanel('show_date'),
        FieldPanel('exclude_from_sitemap'),
    ]


class RecipeBirdPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'RecipeBirdPage', on_delete=models.CASCADE, related_name='tagged_items'
    )


class RecipeBlock(blocks.StructBlock):
    ingredients = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('ingredient', blocks.CharBlock()),
                ('amount', blocks.CharBlock(required=False)),
            ]
        )
    )
    instructions = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('name', blocks.CharBlock(required=False)),
                ('text', blocks.CharBlock()),
                ('url', blocks.URLBlock(required=False)),
                ('image', ImageChooserBlock(required=False)),
            ]
        )
    )

    class Meta:
        template = 'blocks/recipe.html'


class RecipeBirdPage(Page, BirdMixin):
    body = StreamField(
        [
            (
                'paragraph',
                blocks.RichTextBlock(
                    required=False,
                    null=True,
                    features=[
                        "h2",
                        "h3",
                        "h4",
                        "bold",
                        "italic",
                        "superscript",
                        "subscript",
                        "strikethrough",
                        "ol",
                        "ul",
                        "hr",
                        "link",
                        "document-link",
                        "blockquote",
                        "embed",
                        "image",
                    ],
                ),
            ),
            ('recipe', RecipeBlock(required=False, null=True)),
        ],
        blank=True,
        null=True,
        block_counts={
            'recipe': {'max_num': 1},
        },
    )

    tags = ClusterTaggableManager(through=RecipeBirdPageTag, blank=True)

    search_fields = (
        Page.search_fields
        + BirdMixin.search_fields
        + [
            index.SearchField('body'),
        ]
    )
    content_panels = (
        Page.content_panels
        + BirdMixin.content_panels
        + [
            FieldPanel('body'),
        ]
    )
    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]
    settings_panels = Page.settings_panels + BirdMixin.settings_panels

    def get_sitemap_urls(self, request=None):
        if self.exclude_from_sitemap:
            return []
        else:
            return super(RecipeBirdPage, self).get_sitemap_urls(request=request)

    def get_context(self, request):
        context = super().get_context(request)
        related = (self.get_parent().get_descendants().live()
            .public()
            .not_in_menu()
            .exclude(pk=self.pk)
            .order_by('-go_live_at')
            .distinct()[:3]
        )
        context['related'] = related
        return context


class ArticleBirdPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticleBirdPage', on_delete=models.CASCADE, related_name='tagged_items'
    )


class ArticleBirdPage(Page, BirdMixin):
    body = StreamField(
        [
            (
                'paragraph',
                blocks.RichTextBlock(
                    required=False,
                    null=True,
                    features=[
                        "h2",
                        "h3",
                        "h4",
                        "bold",
                        "italic",
                        "superscript",
                        "subscript",
                        "strikethrough",
                        "ol",
                        "ul",
                        "hr",
                        "link",
                        "document-link",
                        "blockquote",
                        "embed",
                        "image",
                    ],
                ),
            ),
            ('media', MediaFileBirdBlock(required=False, null=True)),
            ('code', CodeBirdBlock(required=False, null=True)),
            ('html', HTMLBirdBlock(required=False, null=True)),
        ],
        blank=True,
        null=True,
    )
    tags = ClusterTaggableManager(through=ArticleBirdPageTag, blank=True)

    search_fields = (
        Page.search_fields
        + BirdMixin.search_fields
        + [
            index.SearchField('body'),
        ]
    )
    content_panels = (
        Page.content_panels
        + BirdMixin.content_panels
        + [
            FieldPanel('body'),
        ]
    )
    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]
    settings_panels = Page.settings_panels + BirdMixin.settings_panels

    def get_sitemap_urls(self, request=None):
        if self.exclude_from_sitemap:
            return []
        else:
            return super(ArticleBirdPage, self).get_sitemap_urls(request=request)

    def get_context(self, request):
        context = super().get_context(request)
        related = (self.get_parent().get_descendants().live()
            .public()
            .not_in_menu()
            .exclude(pk=self.pk)
            .order_by('-go_live_at')
            .distinct()[:3]
        )
        context['related'] = related
        return context


class ListBirdPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ListBirdPage', on_delete=models.CASCADE, related_name='tagged_items'
    )


class ListBirdPage(Page, BirdMixin):
    tags = ClusterTaggableManager(through=ListBirdPageTag, blank=True)
    transparent_header = models.BooleanField(default=False)

    search_fields = Page.search_fields + BirdMixin.search_fields
    content_panels = Page.content_panels + BirdMixin.content_panels
    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]
    settings_panels = (
        Page.settings_panels
        + [
            FieldPanel('transparent_header'),
        ]
        + BirdMixin.settings_panels
    )

    def get_sitemap_urls(self, request=None):
        if self.exclude_from_sitemap:
            return []
        else:
            return super().get_sitemap_urls(request=request)

    def get_context(self, request):
        context = super().get_context(request)
        all_posts = (
            self.get_descendants()
            .live()
            .public()
            .filter(
                Q(content_type__model='articlebirdpage')
                | Q(content_type__model='recipebirdpage')
            )
            .order_by('-go_live_at')
            .distinct()
        )
        paginator = Paginator(all_posts, 5)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.get_page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context


class GridBirdPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'GridBirdPage', on_delete=models.CASCADE, related_name='tagged_items'
    )


class GridBirdPage(Page, BirdMixin):
    tags = ClusterTaggableManager(through=GridBirdPageTag, blank=True)
    transparent_header = models.BooleanField(default=False)

    search_fields = Page.search_fields + BirdMixin.search_fields
    content_panels = Page.content_panels + BirdMixin.content_panels
    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]
    settings_panels = (
        Page.settings_panels
        + [
            FieldPanel('transparent_header'),
        ]
        + BirdMixin.settings_panels
    )

    def get_sitemap_urls(self, request=None):
        if self.exclude_from_sitemap:
            return []
        else:
            return super().get_sitemap_urls(request=request)

    def get_context(self, request):
        context = super().get_context(request)
        all_posts = (
            self.get_descendants()
            .live()
            .public()
            .filter(
                Q(content_type__model='articlebirdpage')
                | Q(content_type__model='recipebirdpage')
            )
            .order_by('-go_live_at')
            .distinct()
        )
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.get_page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context


class RSSBirdPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'RSSBirdPage', on_delete=models.CASCADE, related_name='tagged_items'
    )


class RSSBirdPage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    language = models.CharField(max_length=5, blank=True, null=True)

    author_link = models.URLField(blank=True, null=True)

    index_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    tags = ClusterTaggableManager(through=RSSBirdPageTag, blank=True)

    feed_copyright = models.CharField(max_length=128, blank=True, null=True)

    # exclude_from_sitemap = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        PageChooserPanel('index_page'),
        FieldPanel('language'),
        FieldPanel('owner'),
        FieldPanel('author_link'),
        FieldPanel('feed_copyright'),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
    ]
    # settings_panels = Page.settings_panels + [
    #    FieldPanel('exclude_from_sitemap'),
    # ]

    def serve(self, request):
        return RSSFeed(self)(request)

    def get_sitemap_urls(self, request=None):
        return []
        # if self.exclude_from_sitemap:
        #    return []
        # else:
        #    return super(RSSBirdPage, self).get_sitemap_urls(request=request)
