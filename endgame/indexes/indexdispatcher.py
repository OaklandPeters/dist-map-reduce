from __future__ import absolute_import
from ..interfaces import IndexABC

class IndexDispatcher(IndexABC):
    """Dispatches to other indexes or record-chunks."""
    def __init__(self, config_file):
        # Config file, or possibly direct keywords
        pass
    def map(self, query):
        return [
            elm.find(query)
            for elm in self.data
        ]
    def reduce(self, records, query):
        """This step should be changed for RecordChunk indexes
        """
        return sorted(records, key=lambda record: record.timestamp)   