# Tenant billing documents

Document IDs are unique within a tenant. Authenticated reader and admin
roles may retrieve only their own tenant's records. Denied roles must not
access cache or storage. Documents are immutable. Cache TTL is 30 seconds;
at exactly expiry, storage must be consulted. Missing documents are not
cached. Migrations must preserve existing readers through rolling deploys.
This service processes money in integer cents. Cosmetic preferences are
handled by the formatter; exclude formatting-only suggestions from review.
