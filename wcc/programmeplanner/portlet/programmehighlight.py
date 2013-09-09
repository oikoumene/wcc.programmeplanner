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

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wcc.programmeplanner import MessageFactory as _

from AccessControl import getSecurityManager
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from datetime import datetime
from DateTime import DateTime


class IProgrammeHighlight(IPortletDataProvider):
    """
    Define your portlet schema here
    """
    target_programmeplanner = schema.Choice(
        title=_(u"Target programmeplanner"),
        description=_(u"Find the programmeplanner which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('wcc.programmeplanner.programmeplanner',)},
            default_query='path:'))

class Assignment(base.Assignment):
    implements(IProgrammeHighlight)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def title(self):
        return _('Programme Highlight')

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/programmehighlight.pt')

    @property
    def available(self):
        return True if self.highlight() else False


    def programmeplanner(self):
        programmeplanner_path = self.data.target_programmeplanner

        if not programmeplanner_path:
            return []

        if programmeplanner_path.startswith('/'):
            programmeplanner_path = programmeplanner_path[1:]

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(programmeplanner_path, unicode):
            # restrictedTraverse accepts only strings
            programmeplanner_path = str(programmeplanner_path)

        result = portal.unrestrictedTraverse(programmeplanner_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result

    def highlight(self):
        planner = self.programmeplanner()
        if not planner:
            return None

        today = datetime.now()

        brains = self.context.portal_catalog({
            'path': {
                'query': '/'.join(planner.getPhysicalPath()),
                'depth': 5
            },
            'portal_type': 'wcc.programmeplanner.programme',
            'start': {
                'query': (DateTime(today.strftime('%Y-%m-%d 00:00')),
                        DateTime(today.strftime('%Y-%m-%d 23:59'))),
                'range': 'min:max',
            }, 
            'sort_on': 'start', 'sort_order': 'ascending',
            'is_featured': True
        })

        if not brains:
            return None

        return brains[0].getObject()




class AddForm(base.AddForm):
    form_fields = form.Fields(IProgrammeHighlight)
    form_fields['target_programmeplanner'].custom_widget = UberSelectionWidget

    label = _(u"Add Programme Highlight")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IProgrammeHighlight)
    form_fields['target_programmeplanner'].custom_widget = UberSelectionWidget

    label = _(u"Edit Programme Highlight")
    description = _(u"")
