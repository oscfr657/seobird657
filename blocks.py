# -*- coding: utf-8 -*-

from wagtail.core import blocks

from wagtailmedia.blocks import AbstractMediaChooserBlock


class CodeBirdBlock(blocks.StructBlock):

    code = blocks.TextBlock(required=True)

    class Meta:
        label = 'Code'
        icon = 'code'
        template = 'blocks/code.html'


class HTMLBirdBlock(blocks.StructBlock):

    html = blocks.RawHTMLBlock()

    class Meta:
        label = 'HTML'
        icon = 'code'
        template = 'blocks/html.html'


class MediaFileBirdBlock(blocks.StructBlock):
    muted = blocks.BooleanBlock(required=False, default=True, help_text='Muted')
    autoplay = blocks.BooleanBlock(required=False, default=False, help_text='Autoplay')
    loop = blocks.BooleanBlock(required=False, default=False, help_text='Loop')
    controls = blocks.BooleanBlock(required=False, default=True, help_text='Controls')
    block_media = AbstractMediaChooserBlock()

    class Meta:
        label = 'MediaFile'
        icon = 'media'
        template = 'blocks/media_file.html'
