class Service:
    def __init__(self, repository, cache):
        self.repository = repository
        self.cache = cache

    def read(self, principal, document_id, now):
        if principal["role"] not in frozenset({"reader", "admin"}):
            raise PermissionError("Document access denied")
        tenant = principal["tenant"]
        key = (tenant, document_id)
        document = self.cache.get(key, now)
        if document is None:
            document = self.repository.get(tenant, document_id)
            self.cache.put(key, document, now)
        return document
