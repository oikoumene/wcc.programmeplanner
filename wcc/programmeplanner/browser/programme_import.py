from five import grok
from Products.CMFCore.interfaces import ISiteRoot
from plone.directives import form
from plone.namedfile.field import NamedFile
import csv
import z3c.form.button
from wcc.programmeplanner import MessageFactory as _
from wcc.programmeplanner.interfaces import IProductSpecific
from wcc.programmeplanner.content.programmeplanner import IProgrammePlanner
from StringIO import StringIO
from plone.dexterity.utils import createContentInContainer
from zope.component.hooks import getSite
from Products.statusmessages.interfaces import IStatusMessage
from dateutil.parser import parse as parse_date
import re

grok.templatedir('templates')

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

class IUploadFormSchema(form.Schema):

    import_file = NamedFile(title=_('Upload CSV'))


class UploadForm(form.SchemaForm):

    name = _("Import Programmes from CSV")
    schema = IUploadFormSchema
    ignoreContext = True
    grok.layer(IProductSpecific)
    grok.context(IProgrammePlanner)
    grok.name('import_programmes')
    grok.require('cmf.AddPortalContent')
 

    @z3c.form.button.buttonAndHandler(_("Import"), name='import')
    def import_content(self, action):
        formdata, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        f = formdata['import_file'].data.decode('utf-8')
        for l in unicode_csv_reader(StringIO(f)):
            if l[0].lower().strip() == 'title':
                continue
            if len(l) > 8:
                code = l[8]
            else:
                code = ''
            self.create(title=l[0].strip(), 
                        description=l[1].strip(), 
                        text=l[2].strip(), 
                        startTime=l[3].strip(), 
                        endTime=l[4].strip(), 
                        date=parse_date(l[5]).date(),
                        event_type=l[6],
                        focus_group=l[7],
                        code=code)

    def create(self, **params):
        dest = self.context
        match = re.match(r'.*\((.*?)\)$',
                params['title'].strip().replace('\n',' '))
        if match:
            code = match.groups()[0].upper().strip()
        else:
            if params['code'].strip().upper():
                code = params['code'].strip().upper()
            else:
                code = None

        item = createContentInContainer(dest, 'wcc.programmeplanner.programme',
            title=params['title'])

        item.code = code
        item.setTitle(params['title'])
        item.setDescription(params['description'])
        item.text = params['text'].replace('\n', '<br/>')
        item.startTime = params['startTime']
        item.endTime = params['endTime']
        item.date = params['date']
        item.event_type = self.parse_event_type(params['event_type'])
        item.focus_group = self.parse_focus_group(params['focus_group'])
        item.reindexObject()

    def parse_event_type(self, event_type_title):
        mapping = {
            'ecumenical conversation': 'ecumenical-conversation',
            'madang workshop': 'madang-workshop',
            'madang performance': 'madang-performance',
            'bible study': 'bible-study',
            'prayer': 'prayer',
            'plenary': 'plenary',
            'other': 'other'
        }

        if not event_type_title.lower().strip():
            return None

        val = mapping[event_type_title.lower().strip()]
        return val

    def parse_focus_group(self, focus_groups):
        mapping = {
            'inter-religious':'inter-religious',
            'gender': 'gender',
            'indigenous people': 'indigenous-people',
            'indigenous peoples': 'indigenous-people',
            'edan': 'edan',
            'youth':'youth'
        }
        items = [i.strip() for i in focus_groups.split(',')]

        result = []
        for i in items:
            if not i.lower().strip():
                continue
            val = mapping[i.lower().strip()]
            result.append(val)
        return result

