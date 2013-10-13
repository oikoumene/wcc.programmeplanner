from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form

from z3c.form import field

from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationList, RelationChoice

from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wcc.programmeplanner import MessageFactory as _
from zope.component.hooks import getSite

class IUpcomingProgrammes(IPortletDataProvider):
    """
    Define your portlet schema here
    """

    portlet_title = schema.TextLine(title=_(u'Title'), required=True)
    
    target_programmeplanner = schema.Choice(
        title=_(u"Target programmeplanner"),
        description=_(u"Find the programmeplanner which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('wcc.programmeplanner.programmeplanner',)},
            default_query='path:'))


class Assignment(base.Assignment):
    implements(IUpcomingProgrammes)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def title(self):
        return getattr(self, 'portlet_title', 'Upcoming programmes')

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/upcomingprogrammes.pt')

    @property
    def available(self):
        return True


    def upcoming(self):
        programmeplanner_path = self.data.target_programmeplanner

        if not programmeplanner_path:
            return []

        if programmeplanner_path.startswith('/'):
            programmeplanner_path = programmeplanner_path[1:]

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()

        portal_path = '/'.join(portal.getPhysicalPath())
        programmeplanner_path = '/'.join([portal_path, programmeplanner_path])

        brains = self.context.portal_catalog({
            'path': {
                'query': programmeplanner_path,
                'depth': 5
            }, 
            'portal_type': 'wcc.programmeplanner.programme',
            'sort_on': 'start', 'sort_order': 'descending'
        })

        return [b.getObject() for b in brains[:5]]

    def event_type_icon(self, event_type):
        site = getSite()
        return '%s/++resource++wcc.programmeplanner/images/%s-icon.png' % (
            site.absolute_url(),
            event_type
        )


    def item_date(self, item):
        return item.date.strftime('%A, %e %B')


class AddForm(base.AddForm):
    form_fields = form.Fields(IUpcomingProgrammes)
    form_fields['target_programmeplanner'].custom_widget = UberSelectionWidget

    label = _(u"Add Upcoming Programmes")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IUpcomingProgrammes)
    form_fields['target_programmeplanner'].custom_widget = UberSelectionWidget

    label = _(u"Edit Upcoming Programmes")
    description = _(u"")
