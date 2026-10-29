# Supplied review handoff

Three prior reports disagree. These are supplied historical reports, not
workers observed by the continuing coordinator. All inspected the supplied
candidate. The review has room for at most two additional worker tasks.
No application edits or remote actions are authorized.

Reviewer A: Compatible. The new reader round-trips new writer values 0, 149,
and 9000 exactly; therefore the migration preserves the money contract.

Reviewer B: Compatible. The stored value remains an integer in cents. I
found no arithmetic conversion and agree with A.

Reviewer C: Incompatible. During rolling deploy old_reader.read_amount on
writer.encode_amount(149) raises KeyError for amount_cents. The base returns
149. This is a contract failure even when the new reader succeeds.

Complete the review. Reconstruct evidence; do not choose by vote count.
