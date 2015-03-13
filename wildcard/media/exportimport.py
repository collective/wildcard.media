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


def uninstall(context):
    if not context.readDataFile('wildcard.media.uninstall.txt'):
        return

    portal = context.getSite()
    portal_actions = getToolByName(portal, 'portal_actions')
    object_buttons = portal_actions.object_buttons

    # remove actions
    actions_to_remove = ('media_convert',)
    for action in actions_to_remove:
        if action in object_buttons.objectIds():
            object_buttons.manage_delObjects([action])

    # remove control panel
    pcp = getToolByName(context, 'portal_controlpanel', None)
    if pcp:  # plone 4
        pcp.unregisterConfiglet('wildcardmedia')
