from Products.CMFCore.utils import getToolByName
# Plone 4 compatibility does not automatically run
# uninstall step so we have to do this old style way


def install(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(
        'profile-wildcard.media:default')


def uninstall(context, reinstall=False):
    if not reinstall:
        setup = getToolByName(context, 'portal_setup')
        setup.runAllImportStepsFromProfile(
            'profile-wildcard.media:uninstall')
