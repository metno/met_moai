from datetime import datetime


def parse_time(timestring):
    alternatives = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d']
    for a in alternatives:
        try:
            return datetime.strptime(timestring, a)
        except:
            pass
    return datetime.now()
