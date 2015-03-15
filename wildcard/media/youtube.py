from zope.globalrequest import getRequest
from oauthlib.oauth2 import WebApplicationClient
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone import api

import json
import requests


class GoogleAPIException(Exception):
    pass


def gapi(func, error_msg='Error calling youtube api'):
    def myfunc(self, *args, **kwargs):
        resp = func(self, *args, **kwargs)
        rdata = None
        if resp.content:
            # if not empty, check if error
            rdata = resp.json()
            if 'error' in rdata and rdata['error']['code'] == 401:
                self.refresh_access_token()
                resp = func(self, *args, **kwargs)
                rdata = None
        if resp.content:
            # if not empty, check if error, again, raise now since not auth
            rdata = resp.json()
            if 'error' in rdata:
                msg = error_msg
                error = rdata['error']
                if 'message' in error:
                    msg = error['message']
                raise GoogleAPIException(msg + '\n: ' + resp.content)
        return rdata
    return myfunc


class GoogleAPI(object):
    base_url = 'https://www.googleapis.com/youtube/v3/videos'
    upload_url = 'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=status,snippet'  # noqa

    def __init__(self, req=None):
        self._req = req
        self._site = None
        self._registry = None
        self._auth_data = None

    @property
    def req(self):
        if self._req is None:
            self._req = getRequest()
        return self._req

    @property
    def registry(self):
        if not self._registry:
            self._registry = getUtility(IRegistry)
        return self._registry

    @property
    def site(self):
        if not self._site:
            self._site = api.portal.get()
        return self._site

    @property
    def auth_data(self):
        if not self._auth_data:
            self._auth_data = json.loads(self.registry['google_auth_data'])
        return self._auth_data

    @property
    def _headers(self):
        return {
            'Authorization': '%s %s' % (self.auth_data['token_type'],
                                        self.auth_data['access_token']),
            'Content-Type': 'application/json'
        }

    @gapi
    def delete_video(self, data):
        return requests.delete(
            self.base_url + '?id=' + data['id'],
            headers=self._headers)

    @gapi
    def edit_video(self, video, title, description, status=None):
        data = {
            'id': video['id'],
            'kind': 'youtube#video',
            'snippet': video['snippet'].copy()
        }
        parts = 'part=snippet'
        data['snippet']['title'] = title
        data['snippet']['description'] = description
        if status:
            parts = 'part=snippet,status'
            data['status'] = video['status'].copy()
            data['status']['privacyStatus'] = status
        return requests.put(
            '%s?%s' % (self.base_url, parts),
            headers=self._headers,
            data=json.dumps(data)
        )

    def upload_video(self, named_file, title, description, second_try=False):
        fi = named_file.open()
        headers = self._headers
        headers.update({
            'x-upload-content-length': named_file.size,
            'x-upload-content-type': named_file.contentType
        })
        initial_resp = requests.post(
            self.upload_url,
            headers=headers,
            data=json.dumps({
                'snippet': {
                    'title': title,
                    'description': description
                },
                'status': {
                    'privacyStatus': 'unlisted',
                    'embeddable': True
                }
            })
        )
        if initial_resp.content:  # should be empty
            # if not empty, check if error
            rdata = initial_resp.json()
            if 'error' in rdata and rdata['error']['code'] == 401:
                if second_try:
                    # already attempted authorization, suck, error out here
                    raise GoogleAPIException("Error uploading")
                self.refresh_access_token()
                return self.upload_video(named_file, title, description, second_try=True)
        upload_url = initial_resp.headers['location']
        resp = requests.put(upload_url, headers=self._headers, data=fi)
        return resp.json()

    def authorize(self):
        scope = [
            'https://www.googleapis.com/auth/youtube.upload',
            'https://www.googleapis.com/auth/youtube',
            'https://www.googleapis.com/auth/youtubepartner'
        ]
        client = WebApplicationClient(self.registry['google_oauth_id'])
        self.req.response.redirect(client.prepare_request_uri(
            'https://accounts.google.com/o/oauth2/auth', scope=scope,
            redirect_uri='%s/authorize-google' % self.site.absolute_url(),
            approval_prompt='force', access_type='offline',
            include_granted_scopes='true'))

    def confirm_authorization(self):
        url = 'https://accounts.google.com/o/oauth2/token'
        data = {
            'code': self.req.form['code'],
            'client_id': self.registry['google_oauth_id'],
            'client_secret': self.registry['google_oauth_secret'],
            'redirect_uri': '%s/authorize-google' % self.site.absolute_url(),
            'grant_type': 'authorization_code'
        }
        resp = requests.post(url, data=data)
        self.registry['google_auth_data'] = unicode(resp.content)
        self.req.response.redirect(self.site.absolute_url())

    def refresh_access_token(self):
        params = {
            'refresh_token': self.auth_data['refresh_token'],
            'client_id': self.registry['google_oauth_id'],
            'client_secret': self.registry['google_oauth_secret'],
            'grant_type': 'refresh_token'
        }
        resp = requests.post('https://accounts.google.com/o/oauth2/token',
                             data=params)
        self.auth_data.update(resp.json())
        self.registry['google_auth_data'] = unicode(json.dumps(self.auth_data))

    @property
    def authorized(self):
        return self.auth_data is not None


def uploadToYouTube(video):
    api = GoogleAPI()
    if not api.authorized:
        raise Exception("Website is not authorized to upload to YouTube")
    video.youtube_data = api.upload_video(
        video.video_file, video.Title(), video.Description())
    try:
        updateYouTubePermissions(video)
    except:
        removeFromYouTube(video)
        raise
    video.youtube_url = u'https://www.youtube.com/watch?v=%s' % video.youtube_data['id']
    video.video_converted = True


def removeFromYouTube(video):
    api = GoogleAPI()
    if not api.authorized:
        raise Exception("Website is not authorized to upload to YouTube")
    if not hasattr(video, 'youtube_data'):
        raise Exception("No youtube data found. This was never uploaded")
    api.delete_video(video.youtube_data)
    video.youtube_data = None
    video.video_converted = False
    video.youtube_url = u''


def updateYouTubePermissions(video):
    api = GoogleAPI()
    if not api.authorized:
        raise Exception("Website is not authorized to upload to YouTube")
    is_public = False
    for perm in video.rolesOfPermission("View"):
        if perm['name'] == 'Anonymous':
            if perm['selected'] != '':
                is_public = True
            break
    if is_public:
        if video.youtube_data['status']['privacyStatus'] != 'public':
            api.edit_video(video.youtube_data, video.Title(),
                           video.Description(), 'public')
            video.youtube_data['status']['privacyStatus'] = 'public'
    else:
        if video.youtube_data['status']['privacyStatus'] != 'unlisted':
            api.edit_video(video.youtube_data, video.Title(),
                           video.Description(), 'unlisted')
            video.youtube_data['status']['privacyStatus'] = 'unlisted'


def editYouTubeVideo(video):
    api = GoogleAPI()
    if not api.authorized:
        raise Exception("Website is not authorized to upload to YouTube")
    api.edit_video(video.youtube_data, video.Title(), video.Description())
