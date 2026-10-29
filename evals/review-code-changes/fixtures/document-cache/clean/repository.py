from dataclasses import dataclass


@dataclass(frozen=True)
class Document:
    tenant: str
    document_id: str
    amount_cents: int


class Repository:
    def __init__(self, documents):
        self._rows = {(item.tenant, item.document_id): item for item in documents}
        self.reads = 0

    def get(self, tenant, document_id):
        self.reads += 1
        return self._rows[(tenant, document_id)]

    def put(self, document):
        self._rows[(document.tenant, document.document_id)] = document
