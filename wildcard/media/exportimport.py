from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple


def install(context):
    site = context.getSite()

    if not context.readDataFile('wildcard.media.txt'):
        return

    setup = getToolByName(site, 'portal_setup')
    if getFSVersionTuple()[0] == 4:
        setup.runAllImportStepsFromProfile('profile-wildcard.media:plone4')
    else:
        setup.runAllImportStepsFromProfile('profile-wildcard.media:plone5')