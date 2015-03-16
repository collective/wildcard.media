from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple


PROFILE_ID = 'profile-wildcard.media:default'
PROFILE_ID_PLONE4 = 'profile-wildcard.media:plone4'
PROFILE_ID_PLONE5 = 'profile-wildcard.media:plone5'


def upgrade_resources(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    if getFSVersionTuple()[0] == 4:
        setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry')
        setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    else:
        setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def upgrade_types(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')


def upgrade_registry(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def upgrade_to_2(context):
    upgrade_registry(context)
    upgrade_resources(context)