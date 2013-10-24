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
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from zope.component.hooks import getSite


class IProgrammeFocusPortlet(IPortletDataProvider):
    """
    Define your portlet schema here
    """

    header = schema.TextLine(
        title=_(u'Heading'),
        default=u'Related activities in the assembly programme'
    )
    target_programmeplanner = schema.Choice(
        title=_(u"Target programmeplanner"),
        description=_(u"Find the programmeplanner which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('wcc.programmeplanner.programmeplanner',)},
            default_query='path:'))

    focus_group = schema.Choice(
        title=_(u"Focus group"),
        required=True,
        vocabulary="wcc.programmeplanner.focus_group"
    )


class Assignment(base.Assignment):
    implements(IProgrammeFocusPortlet)

    header = u'Related activities in the assembly programme'

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def title(self):
        return _('Programme Focus : %s' % self.focus_group)

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/programmefocusportlet.pt')

    @property
    def available(self):
        return True

    def vocabulary(self):
        factory = getUtility(IVocabularyFactory,
                            name='wcc.programmeplanner.focus_group')
        return factory(self.context)

    def focus_group(self):
        vocab = self.vocabulary()
        return vocab.getTerm(self.data.focus_group).title

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

    def planner_url(self):
        planner = self.programmeplanner()
        if not planner:
            return '#'
        return '%s/programmesearch?focus_group=gender&event_type=all&start_time=all' % (
            planner.absolute_url()
        )

    def items(self):

        planner = self.programmeplanner()
        if not planner:
            return []

        brains = self.context.portal_catalog({
            'path': {
                'query': '/'.join(planner.getPhysicalPath()),
                'depth': 5
            },
            'portal_type': 'wcc.programmeplanner.programme',
            'focus_group': self.data.focus_group
        })

        return [b.getObject() for b in brains[:3]]


    def item_day(self, item):
        return item.date.strftime('%A')

    def item_date(self, item):
        return item.date.strftime('%e %b. %Y')

    def item_time(self, item):
        return '%s - %s' % (item.startTime, item.endTime)

    def event_type_icon(self, event_type):
        site = getSite()
        return '%s/++resource++wcc.programmeplanner/images/%s-icon.png' % (
            site.absolute_url(),
            event_type
        )

        

class AddForm(base.AddForm):
    form_fields = form.Fields(IProgrammeFocusPortlet)
    form_fields['target_programmeplanner'].custom_widget = UberSelectionWidget

    label = _(u"Add Programme Focus Portlet")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IProgrammeFocusPortlet)
    form_fields['target_programmeplanner'].custom_widget = UberSelectionWidget

    label = _(u"Edit Programme Focus Portlet")
    description = _(u"")
