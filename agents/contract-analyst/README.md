# Contract Analyst

Specialist for vendor/customer agreement review. Usually invoked by
`legal-counsel`. Reads the contract as it actually arrives — a Word file — by
converting it with a **CLI** planted in its exec sandbox, and can deliver
redlines back as `.docx`.

## Sources

| Source | Kind | Used for |
| --- | --- | --- |
| [anthropics/knowledge-work-plugins legal](https://github.com/anthropics/knowledge-work-plugins/tree/main/legal) `review-contract` | official-vendor | Persona, skill, process (paraphrased, not copied) |
| [jgm/pandoc](https://github.com/jgm/pandoc) 3.10.2 | popular-oss (46k) | Document conversion; a tool dependency, not a persona source |

## Capabilities

| Capability | Required | Providers |
| --- | --- | --- |
| `document_converter` | yes | CLI `pandoc` (`./tools/pandoc`) |

The template plants `~/legal/doc2md.sh` (Word → Markdown, tracked changes
preserved) and `~/legal/md2docx.sh` (Markdown → Word). Pandoc reads `.docx`,
`.odt`, `.rtf`, and HTML; it does not read legacy `.doc` or PDF, and the
wrapper says so instead of guessing.

## Install

```sh
python3 scripts/build.py contract-analyst
cs template create hub-contract-analyst dist/contract-analyst/template.yaml
cs llm agent create contract-analyst --shared dist/contract-analyst/agent.yaml
```

Not legal advice; every output is a draft for attorney review.
