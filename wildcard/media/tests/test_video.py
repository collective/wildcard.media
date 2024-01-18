# -*- coding: utf-8 -*-
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID, setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.dexterity.interfaces import IDexterityFTI
from plone.rfc822.interfaces import IPrimaryFieldInfo, IPrimaryField
from plone.testing.z2 import Browser
from wildcard.media.behavior import IVideo
from wildcard.media.browser.widget import MediaStream
from wildcard.media.interfaces import IVideoEnabled
from wildcard.media.settings import GlobalSettings
from wildcard.media.testing import MEDIA_FUNCTIONAL_TESTING
from wildcard.media.testing import MEDIA_INTEGRATION_TESTING
from wildcard.media.tests import getVideoBlob, test_file_dir
from zope.component import createObject
from zope.component import queryUtility
from zope.interface import alsoProvides

import os
import unittest


class VideoIntegrationTest(unittest.TestCase):
    layer = MEDIA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.request["ACTUAL_URL"] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        settings = GlobalSettings(self.portal)
        settings.additional_video_formats = []

    def getFti(self):
        return queryUtility(IDexterityFTI, name="WildcardVideo")

    def create(self, id):
        self.portal.invokeFactory(
            "WildcardVideo",
            id,
            video_file=getVideoBlob("mp4"),
            video_file_ogv=getVideoBlob("ogv"),
            video_file_webm=getVideoBlob("webm"),
        )
        return self.portal[id]

    def test_fti(self):
        fti = self.getFti()
        self.assertNotEquals(None, fti)

    def test_factory(self):
        fti = self.getFti()
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IVideoEnabled.providedBy(new_object))

    def test_adding(self):
        self.create("video1")
        self.assertTrue(IVideoEnabled.providedBy(self.portal["video1"]))

    def test_view(self):
        self.create("video2")
        video = self.portal["video2"]
        video.title = "My video"
        video.description = "This is my video."
        self.request.set("URL", video.absolute_url())
        self.request.set("ACTUAL_URL", video.absolute_url())
        alsoProvides(self.request, IPloneFormLayer)
        view = video.restrictedTraverse("@@view")

        result = view()
        self.assertTrue(result)
        self.assertEqual(view.request.response.status, 200)
        self.assertTrue("My video" in result)
        self.assertTrue("This is my video." in result)
        self.assertIn(
            "++widget++form.widgets.IVideo.video_file/@@download/test.mp4", result
        )
        # self.assertIn(
        #     '++widget++form.widgets.IVideo.video_file_ogv/@@download/test.ogv',
        #     result)
        # self.assertIn(
        #    '++widget++form.widgets.IVideo.video_file_webm/@@download/test.webm',
        #    result)

    @unittest.skip("Partial downloads are not supported by plone.namedfile")
    def test_media_range_request(self):
        self.create("video3")
        video = self.portal["video3"]
        alsoProvides(self.request, IPloneFormLayer)
        view = video.restrictedTraverse("@@view")
        view()

        widget = view.widgets.get("IVideo.video_file")
        stream = MediaStream(widget, self.request)

        stream()
        self.assertEqual(self.request.response.status, 200)
        self.assertNotIn("Content-Range", self.request.response.headers)

        for start in (0, 1000, 2000):
            self.request.environ["HTTP_RANGE"] = "bytes=%i-" % start
            stream()
            # Partial content responses for ranges
            self.assertEqual(self.request.response.status, 206)
            self.assertEqual(self.request.response.getHeader("Accept-Ranges"), "bytes")
            content_range = self.request.response.getHeader("Content-Range")
            self.assertIsNotNone(content_range)
            self.assertTrue(content_range.startswith("bytes %i-" % start))

    def test_primary_field(self):
        video = self.create("video")
        info = IPrimaryFieldInfo(video)
        self.assertEquals(info.fieldname, "video_file")
        self.assertTrue(IPrimaryField.providedBy(info.field))

    def test_file_field(self):
        """Although video_file is the Primary field, DX might attempt to set
        the file on the file attribute"""
        video = self.create("videof")
        blob = getVideoBlob("mp4")
        video.file = blob
        self.assertEqual(video.video_file.size, blob.size)
        self.assertEqual(video.video_file.filename, blob.filename)


class VideoFunctionalTest(unittest.TestCase):
    layer = MEDIA_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        settings = GlobalSettings(self.portal)
        settings.additional_video_formats = []
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            "Basic %s:%s"
            % (
                SITE_OWNER_NAME,
                SITE_OWNER_PASSWORD,
            ),
        )

    def test_add_video(self):
        self.browser.open(self.portal_url)
        self.browser.getLink("Video").click()
        self.browser.getControl(
            name="form.widgets.IDublinCore.title"
        ).value = "My video"
        self.browser.getControl(
            name="form.widgets.IDublinCore.description"
        ).value = "This is my video."
        file_path = os.path.join(test_file_dir, "test.mp4")
        file_ctl = self.browser.getControl(name="form.widgets.IVideo.video_file")
        file_ctl.add_file(open(file_path, "rb"), "video/mp4", "test.mp4")
        self.browser.getControl("Save").click()
        self.assertTrue("My video" in self.browser.contents)
        self.assertTrue("This is my video" in self.browser.contents)
        self.assertTrue("<video" in self.browser.contents)
        self.assertIn(
            "++widget++form.widgets.IVideo.video_file/@@stream", self.browser.contents
        )

    @unittest.skip("Async conversion does not work in py3 yet")
    def test_add_video_creates_three_sources(self):
        self.browser.open(self.portal_url)
        self.browser.getLink("Video").click()
        self.browser.getControl(
            name="form.widgets.IDublinCore.title"
        ).value = "My video"
        self.browser.getControl(
            name="form.widgets.IDublinCore.description"
        ).value = "This is my video."
        file_path = os.path.join(test_file_dir, "test.mp4")
        file_ctl = self.browser.getControl(name="form.widgets.IVideo.video_file")
        file_ctl.add_file(open(file_path, "rb"), "video/mp4", "test.mp4")
        self.browser.getControl("Save").click()
        self.assertTrue("My video" in self.browser.contents)
        self.assertTrue("This is my video" in self.browser.contents)
        self.assertTrue("<video" in self.browser.contents)
        self.assertEqual(self.browser.contents.count("<source"), 3)
        self.assertIn(
            "++widget++form.widgets.IVideo.video_file/@@stream", self.browser.contents
        )
        # self.assertIn(
        #    '++widget++form.widgets.IVideo.video_file_ogv/@@stream',
        #    self.browser.contents)
        # self.assertIn(
        #    '++widget++form.widgets.IVideo.video_file_webm/@@stream',
        #    self.browser.contents)


class VideoUrlIntegrationTest(unittest.TestCase):
    layer = MEDIA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.request["ACTUAL_URL"] = self.portal.absolute_url()
        self.video_id = "2Lb2BiUC898"
        self.create("video1", "https://youtu.be/" + self.video_id)
        self.video1 = self.portal["video1"]
        self.create("video2", "https://www.youtube.com/watch?v=2Lb2BiUC898")
        self.video2 = self.portal["video2"]
        self.create("video3", "https://www.youtube.com/embed/" + self.video_id)
        self.video3 = self.portal["video3"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def getFti(self):
        return queryUtility(IDexterityFTI, name="WildcardVideo")

    def create(self, id, video_url, retrieve_thumb=False):
        self.portal.invokeFactory(
            "WildcardVideo", id, video_url=video_url, retrieve_thumb=retrieve_thumb
        )
        return self.portal[id]

    def test_extract_yt_video_id(self):
        behavior1 = IVideo(self.video1)
        behavior2 = IVideo(self.video2)
        behavior3 = IVideo(self.video3)
        self.assertEqual(behavior1.get_youtube_id_from_url(), self.video_id)
        self.assertEqual(behavior2.get_youtube_id_from_url(), self.video_id)
        self.assertEqual(behavior3.get_youtube_id_from_url(), self.video_id)

    def test_yt_url_generation_short(self):
        view = self.video1.restrictedTraverse("@@wildcard_video_view")
        embed_url = "https://www.youtube.com/embed/" + self.video_id
        self.assertEqual(view.get_embed_url(), embed_url)

    def test_yt_url_generation_classic(self):
        view = self.video2.restrictedTraverse("@@wildcard_video_view")
        embed_url = "https://www.youtube.com/embed/" + self.video_id
        self.assertEqual(view.get_embed_url(), embed_url)

    def test_yt_url_generation_embed(self):
        view = self.video3.restrictedTraverse("@@wildcard_video_view")
        embed_url = "https://www.youtube.com/embed/" + self.video_id
        self.assertEqual(view.get_embed_url(), embed_url)

    def test_yt_video_thumb(self):
        image1 = getattr(self.video1, "image", None)
        self.assertEqual(image1, None)

        self.create(
            id="video4",
            video_url="https://www.youtube.com/embed/" + self.video_id,
            retrieve_thumb=True,
        )
        video4 = self.portal["video4"]
        image4 = getattr(video4, "image", None)
        self.assertNotEqual(image4, None)
        self.assertEqual(image4.getImageSize(), (480, 360))
        self.assertEqual(image4.filename, "%s.jpg" % self.video_id)

        self.create("video5", "https://youtu.be/foo")
        image5 = getattr(self.portal["video5"], "image", None)
        self.assertEqual(image5, None)


class VideoUrlPlayerIntegrationTest(unittest.TestCase):
    layer = MEDIA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.request["ACTUAL_URL"] = self.portal.absolute_url()
        self.video_id = "2Lb2BiUC898"
        self.portal.invokeFactory(
            "WildcardVideo",
            "video1",
            video_url="https://youtu.be/" + self.video_id,
        )
        self.portal.invokeFactory(
            "WildcardVideo",
            "video2",
            video_url="https://www.youtube.com/watch?v=2Lb2BiUC898",
        )
        self.portal.invokeFactory(
            "WildcardVideo",
            "video3",
            video_url="https://www.youtube.com/embed/" + self.video_id,
        )
        self.portal.invokeFactory(
            "WildcardVideo",
            "video4",
            video_url="https://foo.com/video4",
        )
        self.portal.invokeFactory(
            "WildcardVideo",
            "video5",
            video_file=getVideoBlob("mp4"),
        )
        self.video1 = self.portal["video1"]
        self.video2 = self.portal["video2"]
        self.video3 = self.portal["video3"]
        self.video4 = self.portal["video4"]
        self.video5 = self.portal["video5"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_youtube_video_has_youtube_player(self):
        self.assertIn(
            'class="wcvideo-container youtube-player"',
            self.video1.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )

        self.assertIn(
            'class="wcvideo-container youtube-player"',
            self.video2.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertIn(
            'class="wcvideo-container youtube-player"',
            self.video3.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertNotIn(
            'class="wcvideo-container youtube-player"',
            self.video4.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertNotIn(
            'class="wcvideo-container youtube-player"',
            self.video5.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )

    def test_internal_video_has_internal_player(self):
        self.assertNotIn(
            'class="wcvideo-container internal-video-player"',
            self.video1.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )

        self.assertNotIn(
            'class="wcvideo-container internal-video-player"',
            self.video2.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertNotIn(
            'class="wcvideo-container internal-video-player"',
            self.video3.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertNotIn(
            'class="wcvideo-container internal-video-player"',
            self.video4.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertIn(
            'class="wcvideo-container internal-video-player"',
            self.video5.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )

    def test_unknown_video_url_has_default_player(self):
        self.assertNotIn(
            'class="wcvideo-container default-player"',
            self.video1.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )

        self.assertNotIn(
            'class="wcvideo-container default-player"',
            self.video2.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertNotIn(
            'class="wcvideo-container default-player"',
            self.video3.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertIn(
            'class="wcvideo-container default-player"',
            self.video4.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )
        self.assertNotIn(
            'class="wcvideo-container default-player"',
            self.video5.restrictedTraverse("@@wildcard_video_view").get_player_code(),
        )


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
