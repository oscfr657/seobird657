from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from wagtail.search import index

from wagtail.admin.edit_handlers import (FieldPanel, StreamFieldPanel)

from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.contrib.settings.models import BaseSetting, register_setting

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from .blocks import (CodeBirdBlock, HTMLBirdBlock, MediaFileBirdBlock)


@register_setting
class SeoSettings(BaseSetting):
    logo = models.ForeignKey(
        'wagtailimages.Image',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='+'
        )

    panels = [
        ImageChooserPanel('logo'),
    ]


class BirdMixin(models.Model):
    author = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = RichTextField(
        blank=True, null=True,
        features=[
            'h2', 'h3', 'h4',
            'bold', 'italic',
            'superscript', 'subscript', 'strikethrough',
            'ol', 'ul', 'hr',
            'link', 'document-link', 'blockquote']
            )
    show_breadcrumbs = models.BooleanField(default=False)
    show_coverImage = models.BooleanField(default=False)
    show_date = models.BooleanField(default=False)
    exclude_from_sitemap = models.BooleanField(default=False)

    class Meta:
        abstract = True

    search_fields = [
        index.SearchField('intro'),
        index.FilterField('author'),
    ]
    content_panels = [
        FieldPanel('author'),
        ImageChooserPanel('cover_image'),
        FieldPanel('intro', classname="full"),
    ]
    settings_panels = [
        FieldPanel('show_breadcrumbs'),
        FieldPanel('show_coverImage'),
        FieldPanel('show_date'),
        FieldPanel('exclude_from_sitemap'),
    ]


class RecipeBirdPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'RecipeBirdPage',
        on_delete=models.CASCADE,
        related_name='tagged_items')


class RecipeBlock(blocks.StructBlock):
    ingredients = blocks.ListBlock(
        blocks.StructBlock([
            ('ingredient', blocks.CharBlock()),
            ('amount', blocks.CharBlock(required=False)),
            ]))
    instructions = blocks.ListBlock(
        blocks.StructBlock([
            ('name', blocks.CharBlock(required=False)),
            ('text', blocks.CharBlock()),
            ('url', blocks.URLBlock(required=False)),
            ('image', ImageChooserBlock(required=False)),
            ]))
    class Meta:
        template = 'blocks/recipe.html'


class RecipeBirdPage(Page, BirdMixin):
    body = StreamField([
        ('recipe', RecipeBlock(
            required=False, null=True
            )),
    ], blank=True, null=True)

    recipe = StreamField([
        ('ingredients', blocks.ListBlock(
            blocks.StructBlock([
                ('ingredient', blocks.CharBlock()),
                ('amount', blocks.CharBlock(required=False)),
                ]))),
        ('instructions', blocks.ListBlock(
            blocks.StructBlock([
                ('name', blocks.CharBlock(required=False)),
                ('text', blocks.CharBlock()),
                ('url', blocks.URLBlock(required=False)),
                ('image', ImageChooserBlock(required=False)),
                ]))),
    ], blank=True, null=True)
    tags = ClusterTaggableManager(through=RecipeBirdPageTag, blank=True)

    search_fields = Page.search_fields + BirdMixin.search_fields + [
        index.SearchField('recipe'),
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels + BirdMixin.content_panels  + [
        StreamFieldPanel('recipe'),
        StreamFieldPanel('body'),
        ]
    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
        ]
    settings_panels = Page.settings_panels + BirdMixin.settings_panels

    def get_sitemap_urls(self, request=None):
        if self.exclude_from_sitemap:
            return []
        else:
            return super(RecipeBirdPage, self).get_sitemap_urls(
                request=request)

    def get_context(self, request):
        context = super().get_context(request)
        context['related'] = RecipeBirdPage.objects.live(
            ).public().not_in_menu().filter(
                tags__in=self.tags.all()).exclude(
                    pk=self.pk).order_by('-go_live_at').distinct()[:3]
        return context


class ArticleBirdPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ArticleBirdPage',
        on_delete=models.CASCADE,
        related_name='tagged_items')


class ArticleBirdPage(Page, BirdMixin):
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(
            required=False, null=True,
            features=[
                'h2', 'h3', 'h4',
                'bold', 'italic',
                'superscript', 'subscript', 'strikethrough',
                'ol', 'ul', 'hr',
                'link', 'document-link',
                'blockquote', 'embed', 'image'])),
        ('media', MediaFileBirdBlock(required=False, null=True)),
        ('code', CodeBirdBlock(required=False, null=True)),
        ('html', HTMLBirdBlock(required=False, null=True)),
    ], blank=True, null=True)
    tags = ClusterTaggableManager(through=ArticleBirdPageTag, blank=True)

    search_fields = Page.search_fields + BirdMixin.search_fields + [
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels + BirdMixin.content_panels  + [
        StreamFieldPanel('body'),
        ]
    promote_panels = Page.promote_panels + [
        FieldPanel('tags'),
        ]
    settings_panels = Page.settings_panels + BirdMixin.settings_panels

    def get_sitemap_urls(self, request=None):
        if self.exclude_from_sitemap:
            return []
        else:
            return super(ArticleBirdPage, self).get_sitemap_urls(
                request=request)

    def get_context(self, request):
        context = super().get_context(request)
        context['related'] = ArticleBirdPage.objects.live(
            ).public().not_in_menu().filter(
                tags__in=self.tags.all()).exclude(
                    pk=self.pk).order_by('-go_live_at').distinct()[:3]
        return context
