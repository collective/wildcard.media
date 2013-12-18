from logging import getLogger
from zope.component import getUtility
from wildcard.video.convert import runConversion
from Products.CMFCore.utils import getToolByName

try:
    from zc.async.interfaces import COMPLETED
except:
    COMPLETED = None

logger = getLogger('wildcard.video')

QUOTA_NAME = 'wildcard.video'

try:
    from plone.app.async.interfaces import IAsyncService
except ImportError:
    pass


def getPortal(obj):
    return getToolByName(obj, 'portal_url').getPortalObject()


def asyncInstalled():
    try:
        import plone.app.async
        plone.app.async  # pyflakes
        return True
    except:
        return False


def isConversion(job, sitepath):
    """
    Check if job is a document viewer conversion job
    """
    return sitepath == job.args[1] and job.args[4] == runConversion


class JobRunner(object):
    """
    helper class to setup the quota and check the
    queue before adding it to the queue
    """

    def __init__(self, obj):
        self.object = obj
        self.objectpath = self.object.getPhysicalPath()
        self.portal = getPortal(obj)
        self.portalpath = self.portal.getPhysicalPath()
        self.async = getUtility(IAsyncService)
        self.queue = self.async.getQueues()['']

    def is_current_active(self, job):
        return isConversion(job, self.portalpath) and \
            job.args[0] == self.objectpath and \
            job.status != COMPLETED

    @property
    def already_in_queue(self):
        """
        Check if object in queue
        """
        return self.find_job()[0] > -1

    def find_position(self):
        # active in queue
        try:
            return self.find_job()[0]
        except KeyError:
            return -1

    def find_job(self):
        # active in queue
        if QUOTA_NAME not in self.queue.quotas:
            return -1, None
        for job in self.queue.quotas[QUOTA_NAME]._data:
            if self.is_current_active(job):
                return 0, job

        jobs = [job for job in self.queue]
        for idx, job in enumerate(jobs):
            if self.is_current_active(job):
                return idx + 1, job
        return -1, None

    def set_quota(self):
        """
        Set quota for document viewer jobs
        """
        if QUOTA_NAME in self.queue.quotas:
            if self.queue.quotas[QUOTA_NAME].size != 3:
                self.queue.quotas[QUOTA_NAME].size = 3
                logger.info("quota %r configured in queue %r", QUOTA_NAME,
                            self.queue.name)
        else:
            self.queue.quotas.create(QUOTA_NAME, size=3)
            logger.info("quota %r added to queue %r", QUOTA_NAME,
                        self.queue.name)

    def queue_it(self):
        self.async.queueJobInQueue(self.queue, (QUOTA_NAME,), runConversion,
                                   self.object)


def queueJob(obj):
    """
    queue a job async if available.
    otherwise, just run normal
    """
    if asyncInstalled():
        try:
            runner = JobRunner(obj)
            runner.set_quota()
            if runner.already_in_queue:
                logger.info('object %s already in queue for conversion' % (
                    repr(obj)))
            else:
                runner.queue_it()
            return
        except:
            logger.exception(
                "Error using plone.app.async with "
                "collective.documentviewer. Converting pdf without "
                "plone.app.async...")
            runConversion(obj)
    else:
        runConversion(obj)
