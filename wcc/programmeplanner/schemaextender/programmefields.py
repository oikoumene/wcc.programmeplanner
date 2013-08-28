from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes import atapi
from Products.ATContentTypes.interfaces import IATContentType
from zope.interface import Interface
from five import grok
from wcc.programmeplanner.interfaces import IProductSpecific
from wcc.programmeplanner import MessageFactory as _

# Visit http://pypi.python.org/pypi/archetypes.schemaextender for full 
# documentation on writing extenders

class ProgrammeFields(grok.Adapter):

    # This applies to all AT Content Types, change this to
    # the specific content type interface you want to extend
    grok.context(IATContentType)
    grok.name('wcc.programmeplanner.programmefields')
    grok.implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    grok.provides(IOrderableSchemaExtender)

    layer = IProductSpecific

    fields = [
        # add your extension fields here
        atapi.StringField(
            'event_type',
            vocabulary=['1','2','3'],
            widget=atapi.SelectionWidget(
                label=u'Event Type'
            )
        ),
        atapi.StringField(
            'focus_group',
            vocabulary=['4','5','6'],
            widget=atapi.SelectionWidget(
                label=u'Focus Group',
            )
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        # you may reorder the fields in the schemata here
        return schematas


