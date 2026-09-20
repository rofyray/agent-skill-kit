# Worked repairs

## A short polish stays short

Original: “Translate {{text}} to Spanish. Give just the translation please, don't add notes. Keep people's names the same.”

Polished: “Translate {{text}} into Spanish. Preserve people's names and return only the translation.”

The variable, language, name-preservation rule, and output restriction survive. There is no need for three headings, tools, a persona, or a word limit. Performance remains unverified until tested.

## Resolve a product decision before calling a rewrite ready

Original: “Always answer immediately without questions. If the request is unclear, ask what the user means before answering.”

Finding: Both instructions govern unclear requests but require different first actions. Ask whether clarification should take priority in that situation. Independently improve surrounding wording, but do not silently choose the priority or claim the result is ready.

If the user chooses clarification: “When ambiguity would materially change the answer, ask a focused clarification question before answering. Otherwise answer directly.” The narrower clarification condition is itself a product choice and must be supported by the user's decision.

## Refactor with requirements preserved

Original: “You help editors summarize supplied interviews. Return JSON with summary and unresolved_questions. Only use the transcript {{transcript}}. Don't fill gaps with guesses. Return no markdown. If the interview doesn't answer something, put that in unresolved_questions. Don't browse.”

Revised:

```markdown
# Background
Help editors summarize the supplied interview transcript: {{transcript}}

# Behaviour
Use only the transcript. Do not browse or infer missing facts. Identify unanswered questions from the interview.

# Output
Return only JSON with the keys summary and unresolved_questions. Put unanswered questions in unresolved_questions. Do not include Markdown.
```

The rewrite retains the declared keys without inventing their data types. If a consuming application requires a schema, request that schema before claiming interface validation. Review the phrase “unanswered questions” against examples if the product needs a narrower definition.

## Catch a cross-fragment conflict

Shared developer message: “Use the language of the user's message.”
Injected developer message for French accounts: “Always respond in English.”

Each fragment is readable alone. Audit the French-account combination and identify the unresolved locale policy. Preserve both message boundaries in the draft, and resolve the product decision before changing assembly rules.

## Compare a misleading simplification

Original: “Draft an email using {{customer}}. Ask for confirmation before calling send_email.”
Revision: “Email {{customer}} using send_email.”

Finding: The placeholder and tool name survived, but draft-only behavior and confirmation did not. A mechanical comparison may return no flags; the semantic review must still catch both changes. Do not send an email while evaluating this example.

## Leave a good prompt alone

Original: “Extract invoice_number and total from the supplied invoice. Return only JSON with those two keys. Use null for a missing value. Do not infer missing values.”

If this meets the user's intent, report no necessary changes. A different arrangement of headings alone is not evidence of better results.
