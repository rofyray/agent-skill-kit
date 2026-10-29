class Cache:
    def __init__(self):
        self._entries = {}

    def get(self, key, now):
        entry = self._entries.get(key)
        if entry is None:
            return None
        expires_at, document = entry
        if now <= expires_at:
            return document
        del self._entries[key]
        return None

    def put(self, key, document, now):
        self._entries[key] = (now + 30, document)
