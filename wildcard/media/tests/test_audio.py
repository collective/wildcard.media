# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import os
from zope.interface import alsoProvides
from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI

from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser

from wildcard.media.interfaces import IAudioEnabled

from wildcard.media.testing import (
    MEDIA_INTEGRATION_TESTING,
    MEDIA_FUNCTIONAL_TESTING
)

from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer
from wildcard.media.tests import getAudioBlob, test_file_dir
from plone.rfc822.interfaces import IPrimaryFieldInfo, IPrimaryField


class AudioIntegrationTest(unittest.TestCase):

    layer = MEDIA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def getFti(self):
        return queryUtility(IDexterityFTI, name='WildcardAudio')

    def create(self, id):
        self.portal.invokeFactory('WildcardAudio', id,
                                  audio_file=getAudioBlob())
        return self.portal[id]

    def test_schema(self):
        fti = self.getFti()
        schema = fti.lookupSchema()
        self.assertEqual(schema.getName(), 'plone_0_WildcardAudio')

    def test_fti(self):
        fti = self.getFti()
        self.assertNotEquals(None, fti)

    def test_factory(self):
        fti = self.getFti()
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IAudioEnabled.providedBy(new_object))

    def test_adding(self):
        self.create('audio1')
        self.assertTrue(IAudioEnabled.providedBy(self.portal['audio1']))

    def test_view(self):
        self.create('audio2')
        audio = self.portal['audio2']
        audio.title = "My Audio"
        audio.description = "This is my audio."
        self.request.set('URL', audio.absolute_url())
        self.request.set('ACTUAL_URL', audio.absolute_url())
        alsoProvides(self.request, IPloneFormLayer)
        view = audio.restrictedTraverse('@@view')

        self.assertTrue(view())
        self.assertEqual(view.request.response.status, 200)
        self.assertTrue('My Audio' in view())
        self.assertTrue('This is my audio.' in view())

    def test_primary_field(self):
        audio = self.create('audio')
        info = IPrimaryFieldInfo(audio)
        self.assertEquals(info.fieldname, 'audio_file')
        self.assertTrue(IPrimaryField.providedBy(info.field))


class AudioFunctionalTest(unittest.TestCase):

    layer = MEDIA_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_add_audio(self):
        self.browser.open(self.portal_url)
        self.browser.getLink('Audio').click()
        self.browser.getControl(
            name='form.widgets.IDublinCore.title').value = "My audio"
        self.browser.getControl(
            name='form.widgets.IDublinCore.description')\
            .value = "This is my audio."
        file_path = os.path.join(test_file_dir, "test.mp3")
        file_ctl = self.browser.getControl(
            name='form.widgets.IAudio.audio_file')
        file_ctl.add_file(open(file_path), 'audio/mp3', 'test.mp3')
        self.browser.getControl('Save').click()
        self.assertTrue('My audio' in self.browser.contents)
        self.assertTrue('This is my audio' in self.browser.contents)
        self.assertTrue('<audio' in self.browser.contents)
        self.assertIn(
            '++widget++form.widgets.IAudio.audio_file/@@stream',
            self.browser.contents)
