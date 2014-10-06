from __future__ import absolute_import
from ..interfaces import IndexABC

class URLDispatcher(object):
    """
    Interacts with a remote URL (which is expected to in turn be an IndexDispatcher).
    """
    #--------------------------------------------------------------------------
    #    Dispatching
    #--------------------------------------------------------------------------
    @classmethod
    def _validate_url(cls, url):
        """
        @todo: Expand this.
        """
        if not isinstance(url, basestring):
            raise TypeError("'url' must be a basestring.")
        else: # string
            if url.startswith("http://"):
                return url
            else:
                raise ValueError("Invalid url.")
    @classmethod
    def valid_url(cls, url):
        try:
            cls._validate_url(url)
        except (ValueError, TypeError):
            return False
        else:
            return True
    @classmethod
    def valid(cls, value):
        return cls.valid_url(value)