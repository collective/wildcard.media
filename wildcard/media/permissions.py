# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles
#http://developer.plone.org/security/custom_permissions.html
security = ModuleSecurityInfo('plone.app.contenttypes')
TYPE_ROLES = ('Manager', 'Site Administrator', 'Owner', 'Contributor')

security.declarePublic('wildcard.media.AddWildcardVideo')
setDefaultRoles('wildcard.media.AddWildcardVideo', TYPE_ROLES)
AddWildcardVideo = "wildcard.media.AddWildcardVideo"

security.declarePublic('wildcard.media.AddWildcardAudio')
setDefaultRoles('wildcard.media.AddWildcardAudio', TYPE_ROLES)
AddWildcardAudio = "wildcard.media.AddWildcardAudio"
