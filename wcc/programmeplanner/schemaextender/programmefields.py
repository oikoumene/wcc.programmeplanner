from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from Products.Archetypes import atapi
from Products.ATContentTypes.interfaces import IATContentType
from zope.interface import Interface
from five import grok
from wcc.programmeplanner.interfaces import IProductSpecific
from wcc.programmeplanner import MessageFactory as _
from wcc.programmeplanner.interfaces import IProgrammeFieldsEnabled

# Visit http://pypi.python.org/pypi/archetypes.schemaextender for full 
# documentation on writing extenders

class ExtensionStringField(ExtensionField, atapi.StringField):
    pass

class ProgrammeFields(grok.Adapter):

    # This applies to all AT Content Types, change this to
    # the specific content type interface you want to extend
    grok.context(IProgrammeFieldsEnabled)
    grok.name('wcc.programmeplanner.programmefields')
    grok.implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    grok.provides(IOrderableSchemaExtender)

    layer = IProductSpecific

    fields = [
        # add your extension fields here
        ExtensionStringField(
            'event_type',
            vocabulary_factory='wcc.programmeplanner.event_type',
            storage=atapi.AttributeStorage(),
            widget=atapi.SelectionWidget(
                label=u'Event Type'
            ),
            required=False,
            schemata='default'
        ),
        ExtensionStringField(
            'focus_group',
            vocabulary_factory='wcc.programmeplanner.focus_group',
            storage=atapi.AttributeStorage(),
            widget=atapi.SelectionWidget(
                label=u'Focus Group',
            ),
            required=False,
            schemata='default'
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        # you may reorder the fields in the schemata here
        return schematas


