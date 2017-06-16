from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple
from wildcard.media.settings import GlobalSettings
import logging

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

def upgrade_to_3000(context, logger=None):
    """We need to change the name for an attribute for video objects.
    youtube_url now is video_url"""

    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('wildcard.media')

    logger.info('Upgrading wildcard.media to version 3000')

    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog(portal_type='WildcardVideo')
    count = 0

    for brain in brains:
        video_obj = brain.getObject()
        video_obj.video_url = video_obj.youtube_url
        video_obj.reindexObject() # reindicizziamo
        count += 1


    logger.info('%s fields for WildcardVideo objects converted.' % count)
    logger.info('wildcard.media v.3000: upgrade done')
