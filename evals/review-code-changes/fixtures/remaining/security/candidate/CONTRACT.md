# Public render endpoint threat model

This anonymous endpoint accepts a positive integer copies. Rendering has
linear CPU work and memory use of 65536 bytes per copy. Every accepted
request must have copies at most 64; reject other values before allocation.
There is no upstream proxy cap or authentication barrier. Public resource
exhaustion is a material threat. The local helper is the endpoint entrypoint.
Do not stress-test huge values; bounded boundary probes are sufficient.
