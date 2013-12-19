try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName


def install(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(
        'profile-wildcard.media:default')


def uninstall(context, reinstall=False):
    if not reinstall:
        setup = getToolByName(context, 'portal_setup')
        setup.runAllImportStepsFromProfile(
            'profile-wildcard.media:uninstall')

        portal = getSite()
        portal_actions = getToolByName(portal, 'portal_actions')
        object_buttons = portal_actions.object_buttons

        # remove actions
        actions_to_remove = ('media_convert',)
        for action in actions_to_remove:
            if action in object_buttons.objectIds():
                object_buttons.manage_delObjects([action])

        # remove control panel
        pcp = getToolByName(context, 'portal_controlpanel')
        pcp.unregisterConfiglet('wildcardmedia')
