# Document lookup contract

This local service returns billing documents for an authenticated tenant.
Document IDs are unique within a tenant, not globally. The same ID can occur
in several tenants. An allowed caller must receive only its own tenant's
record. Roles `reader` and `admin` may read documents; every other role is
denied before storage or cache access. The service receives an authenticated
principal from its caller; it does not authenticate raw HTTP requests.

Document objects are immutable. A cached document can be reused until its
30-second TTL expires. At exactly the expiry timestamp the repository must
be read again. Changes to storage need not appear before expiry. Missing
documents raise LookupError and are not cached. The cache lives for the
service lifetime and can be shared by requests from different tenants.

The legacy `summarize_cents` helper returns the exact integer sum of amounts
in cents. Amounts passed to this helper are nonnegative integers.

Run the existing local tests with `python3 -m unittest -v test_service.py`.
The tests use no network, external services, or third-party packages.
