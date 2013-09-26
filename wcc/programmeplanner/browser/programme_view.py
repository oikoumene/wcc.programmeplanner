from five import grok
from plone.directives import dexterity, form
from wcc.programmeplanner.content.programme import IProgramme
from zope.component.hooks import getSite

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IProgramme)
    grok.require('zope2.View')
    grok.template('programme_view')
    grok.name('view')

    def icon_url(self):
        site = getSite()
        return '%s/++resource++wcc.programmeplanner/images/%s-icon.png' % (
            site.absolute_url(),
            self.context.event_type
        )

    def get_feature_image(self, scale='mini', css_class=None):
        obj = self.context
        featureimages = obj.restrictedTraverse('@@featureimages')
        result = featureimages.tag(scale=scale, css_class=css_class)
        return result if result else ''

    def day(self):
        return self.context.date.strftime('%A')

    def date(self):
        return self.context.date.strftime('%d %b %Y')

    def time(self):
        return '%s - %s' % (self.context.startTime, self.context.endTime)
