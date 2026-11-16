# Data contracts

One entry per table. Update when a table is added or its grain, keys, or columns change.

## Template

### `{{schema.table}}`
- **Layer:** raw / bronze / silver / gold
- **Grain:** one row per {{…}}
- **Keys:** business key `{{…}}`; surrogate key `{{…}}`
- **Load pattern:** append / merge / full refresh; watermark `{{…}}`
- **Freshness:** expected by {{time}} after source availability
- **SCD type:** n/a / 1 / 2
- **Not-null columns:** {{…}}
- **Quality rules:** {{rule IDs or expectations}}
- **Inferred columns:** {{column — inference method}} (or "none")
- **Upstream / downstream:** {{…}}

## Tables
