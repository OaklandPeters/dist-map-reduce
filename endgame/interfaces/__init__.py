

__all__ = [
    'Query', 'Record'
]

class Query(object):
    def __init__(self, ips, timerange):
        self.ips = ips
        self.timerange = timerange

class Record(object):
    def __init__(self, ip, timestamp):
        self.ip = ip
        self.timestamp = timestamp