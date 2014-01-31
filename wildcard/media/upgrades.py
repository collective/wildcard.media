from Products.CMFPlone.utils import getToolByName


PROFILE_ID='profile-wildcard.media:default'


def upgrade_css(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'cssregistry')


def upgrade_types(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')

