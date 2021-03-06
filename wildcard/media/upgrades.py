from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple
from wildcard.media.settings import GlobalSettings


PROFILE_ID = 'profile-wildcard.media:default'
PROFILE_ID_PLONE4 = 'profile-wildcard.media:plone4'
PROFILE_ID_PLONE5 = 'profile-wildcard.media:plone5'


def upgrade_resources(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    if getFSVersionTuple()[0] == 4:
        setup.runImportStepFromProfile(PROFILE_ID_PLONE4, 'cssregistry')
        setup.runImportStepFromProfile(PROFILE_ID_PLONE4, 'jsregistry')
    else:
        setup.runImportStepFromProfile(PROFILE_ID_PLONE5, 'plone.app.registry')


def upgrade_types(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'typeinfo')


def upgrade_registry(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def upgrade_to_2(context):
    upgrade_registry(context)
    upgrade_resources(context)


def upgrade_to_2003(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    settings = GlobalSettings(portal)
    # Apply old in/outfile options to each new format specific option
    old_outfileopt = settings.convert_outfile_options
    old_infileopt = settings.convert_infile_options

    if old_outfileopt:
        settings.avconv_out_mp4 = old_outfileopt
        settings.avconv_out_ogg = old_outfileopt
        settings.avconv_out_webm = old_outfileopt
    if old_infileopt:
        settings.avconv_in_mp4 = old_infileopt
        settings.avconv_in_ogg = old_infileopt
        settings.avconv_in_webm = old_infileopt
