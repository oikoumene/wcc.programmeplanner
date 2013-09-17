from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.multilingualbehavior.directives import languageindependent

from wcc.programmeplanner import MessageFactory as _
from collective import dexteritytextindexer


# Interface class; used to define content-type schema.

class IProgramme(form.Schema, IImageScaleTraversable):
    """
    
    """

    languageindependent('startDate')
    startDate = schema.Datetime(title=_(u'Start Date'))

    languageindependent('endDate')
    endDate = schema.Datetime(title=_(u'End Date'))

    languageindependent('event_type')
    event_type = schema.Choice(
        title=_(u'Event Type'),
        vocabulary='wcc.programmeplanner.event_type'
    )

    languageindependent('focus_group')
    focus_group = schema.List(
        title=_(u'Focus Group'),
        value_type=schema.Choice(
            vocabulary='wcc.programmeplanner.focus_group'
        )
    )

    dexteritytextindexer.searchable('text')
    form.widget(text="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    text = schema.Text(
        title=_(u"Body Text"),
        description=u'',
        required=False,
    )
