# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles
#http://developer.plone.org/security/custom_permissions.html
security = ModuleSecurityInfo('plone.app.contenttypes')
TYPE_ROLES = ('Manager', 'Site Administrator', 'Owner', 'Contributor')
security.declarePublic('wildcard.video.AddWildcardVideo')
setDefaultRoles('wildcard.video.AddWildcardVideo', TYPE_ROLES)

AddWildcardVideo = "wildcard.video.AddWildcardVideo"
