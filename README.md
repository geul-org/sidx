# sidx

Research toward SIDX (Semantic-aligned Index) assignment for [GEUL](https://geul.org/): giving frequently used Wikidata items and GEUL IDs numbers such that entities with close meanings get close numbers.

> **Status: pre-v1 design material.** No SIDX assignment has been produced yet. Much of this repository (the 48-bit Entity Node schema, the encoder scripts, the codebooks) predates the current GEUL grammar and does not match it. The normative definition of SIDX is the GEUL grammar page [GEUL-SIDX](https://geul.org/grammar/reference/geul-sidx/).

## What SIDX is

A SIDX is a semantic address: numbers that are close mean entities that are close in meaning. GEUL IDs and Wikidata QIDs are identity numbers whose values carry no meaning. An entity that has both a GEUL ID and a SIDX links the two References with `SAME-NODE`. Equal SIDX values denote the same entity.

The assignment approach, its inputs and the open questions are described in [docs/design.md](docs/design.md) (Korean).

The geul.org term definition document `0x0001000000000003` (Issuer `0x0000`) identifies this repository as a tool: earlier Wikidata conversions cite its loader `artifacts/wikidata/postgres.go` at commit `4225b3b`. That file therefore stays at its path.

## Contents

```
artifacts/
  wikidata/    Wikidata usage and hierarchy statistics with the scripts that produced them
  scripts/     the earlier 64-bit Entity SIDX encoder and its five-stage pipeline (reference only)
files/
  legacy/      earlier Entity Node design documents, codebooks and reports (superseded)
docs/
  design.md    SIDX assignment design draft and file notes (Korean)
```

The statistics in `artifacts/wikidata/` were computed from an earlier database layout. They have not been recomputed from a database loaded by [wikipg](https://github.com/geul-org/wikipg).

## Requirements

The scripts are kept for reference and do not run against current databases without changes. They expect:

- Python 3 with `psycopg2`, and Go for `artifacts/wikidata/*.go`
- PostgreSQL with the earlier table layout (`artifacts/wikidata/wikidata.sql`)

Database passwords are read from environment variables or from a `.env` file at the repository root (excluded from git). Copy [.env.example](.env.example) to `.env` and fill in `GEUL_READER_PASSWORD`, `GEUL_WRITER_PASSWORD` and `POSTGRES_PASSWORD`. Python reads them through `artifacts/scripts/sidx_env.py`, the Go tools through `envValue()`.

## Related repositories

| Repository | Relation |
|---|---|
| [wikipg](https://github.com/geul-org/wikipg) | Loads Wikidata dumps into PostgreSQL |
| [gogeulwiki](https://github.com/geul-org/gogeulwiki) | Converts Wikidata into GEUL documents |
| [gogeul](https://github.com/geul-org/gogeul) | GEUL Go library |

## License

Our own work in this repository (code, documents, data) is dedicated to the public domain under [CC0 1.0](LICENSE). The data source, Wikidata, is also CC0.
