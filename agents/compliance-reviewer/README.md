# Compliance Reviewer

Privacy specialist for the legal demo. Usually invoked by `legal-counsel`.
Reads contracts and DPAs as they arrive — Word files — by converting them with
a **CLI** planted in its exec sandbox.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [anthropics/knowledge-work-plugins legal](https://github.com/anthropics/knowledge-work-plugins/tree/main/legal) `compliance-check` | official-vendor | Persona, skill, process (paraphrased, not copied) |
| [jgm/pandoc](https://github.com/jgm/pandoc) 3.10.2 | popular-oss (46k) | Document conversion; a tool dependency, not a persona source |

## Capabilities

| Capability | Required | Providers |
| --- | --- | --- |
| `document_converter` | yes | CLI `pandoc` (`./tools/pandoc`) |

Same tool package as `contract-analyst`: `~/legal/doc2md.sh` and
`~/legal/md2docx.sh`. Reads `.docx`, `.odt`, `.rtf`, HTML; not legacy `.doc`
or PDF.

## Install

```sh
python3 scripts/build.py compliance-reviewer
cs template create hub-compliance-reviewer dist/compliance-reviewer/template.yaml
cs llm agent create compliance-reviewer --shared dist/compliance-reviewer/agent.yaml
```

Not legal advice; every output is a draft for attorney review.
