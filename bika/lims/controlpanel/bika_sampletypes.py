from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import schemata
from Products.Archetypes import atapi
from Products.Archetypes.ArchetypeTool import registerType
from Products.CMFCore import permissions
from Products.Five.browser import BrowserView
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.config import PROJECTNAME
from bika.lims import bikaMessageFactory as _
from bika.lims.content.bikaschema import BikaFolderSchema
from bika.lims.interfaces import ISampleTypes
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.folder.folder import ATFolder, ATFolderSchema
from zope.interface.declarations import implements
from Products.CMFCore.utils import getToolByName
import json
from operator import itemgetter

class SampleTypesView(BikaListingView):
    implements(IFolderContentsView)
    contentFilter = {'portal_type': 'SampleType', 'sort_on': 'sortable_title'}
    content_add_actions = {_('Sample Type'): "createObject?type_name=SampleType"}
    title = _("Sample Types")
    description = ""
    show_editable_border = False
    show_filters = True
    show_sort_column = False
    show_select_row = False
    show_select_column = True
    pagesize = 20

    columns = {
               'Title': {'title': _('Sample Type'), 'icon':'sampletype.png'},
               'Description': {'title': _('Description')},
              }
    review_states = [
                    {'title': _('All'), 'id':'all',
                     'columns': ['Title', 'Description'],
                     'buttons':[{'cssclass': 'context',
                                 'Title': _('Delete'),
                                 'url': 'folder_delete:method'}]},
                    ]

    def folderitems(self):
        items = BikaListingView.folderitems(self)
        out = []
        for x in range(len(items)):
            if not items[x].has_key('obj'): continue
            obj = items[x]['obj'].getObject()
            items[x]['Description'] = obj.Description()
            items[x]['replace']['Title'] = "<a href='%s'>%s</a>" % \
                 (items[x]['url'], items[x]['Title'])
            out.append(items[x])


        out = sorted(out, key=itemgetter('Title'))
        for i in range(len(out)):
            out[i]['table_row_class'] = ((i + 1) % 2 == 0) and "draggable even" or "draggable odd"
        return out

schema = ATFolderSchema.copy()

class SampleTypes(ATFolder):
    implements(ISampleTypes)
    schema = schema
    displayContentsTab = False
schemata.finalizeATCTSchema(schema, folderish = True, moveDiscussion = False)
atapi.registerType(SampleTypes, PROJECTNAME)

class AJAX_SampleTypes():
    """ autocomplete data source for sample types field
        return JSON data [string,string]
    """
    def __call__(self):
        pc = getToolByName(self, 'portal_catalog')
        term = self.request.get('term', '')
        items = pc(portal_type = "SampleType")
        nr_items = len(items)
        items = [s.Title for s in items if s.Title.lower().find(term.lower()) > -1]
        return json.dumps(items)

