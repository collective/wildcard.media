# -*- coding: utf-8 -*-
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import login
from zope.configuration import xmlconfig
from plone.app.testing import quickInstallProduct


class MediaLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import wildcard.media
        xmlconfig.file(
            'configure.zcml',
            wildcard.media,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        quickInstallProduct(portal, 'wildcard.media')
        #applyProfile(portal, 'wildcard.media:default')
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        setRoles(portal, TEST_USER_ID, ['Manager'])

    def tearDownPloneSite(self, portal):
        applyProfile(portal, 'wildcard.media:uninstall')


MEDIA_FIXTURE = MediaLayer()
MEDIA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIA_FIXTURE,),
    name="Media:Integration"
)
MEDIA_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIA_FIXTURE,),
    name="MEDIA:Functional"
)
