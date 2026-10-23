# SEC Disclosure Explorer

## Project overview / 项目概述

披露事件、交易日对齐、股价窗口 / Filings, trading-day alignment, price windows。

**Interactive portfolio:** [SEC disclosure explorer](https://milanchen0307-cmyk.github.io/sec-disclosure-explorer/) — public, no login required.
**Source code:** public repository with notebooks, analysis scripts and dashboard source.

SEC 披露事件探索器：连接公司标识、披露日期和价格序列，展示可追溯的事件窗口。

**Question:** What happened to a company's adjusted stock price around a public filing, and which observations are worth a deeper event study?

The original coursework combines PostgreSQL company/price tables, MongoDB filing text, and a Flask interface. This portfolio adds a database-free explorer so reviewers can inspect the workflow immediately.

## 阅读方式 / Start here

This is a coursework project curated into a reproducible portfolio. The original analytical approach is retained; the standalone presentation and validation scripts are a later portfolio refinement.

Open **[the interactive demo](https://milanchen0307-cmyk.github.io/sec-disclosure-explorer/)** or download the repository and open `docs/index.html` directly. The hosted demo is public. Explore the code, notebooks and aggregate results in this repository. No API key is needed to open the local HTML version.

## Repository map

- `docs/`: standalone interactive evidence page and its aggregate data.
- `src/`: reproducible portfolio analysis/export and rendering scripts.
- `reports/`: machine-readable aggregate evidence and figures.
- `notebooks/`: original coursework source, cleared of outputs and execution state.
- `data/README.md`: input schema and data access notes.


## Published evidence

The current demonstration includes **75 filings across 11 companies**, selected from a bounded scan of the original export. Every event links back to its SEC source. The sample is a convenience sample, not a market-wide or representative study.

### Event-window definition

1. Sort and deduplicate trading dates per company.
2. Day 0 is the first available trading date on or after the filing date (reject gaps over seven calendar days).
3. Normalize adjusted close to the session immediately before day 0.
4. Show up to five preceding and ten subsequent trading sessions.

Return = `(adjusted_close_t / adjusted_close_previous_session - 1) × 100`.

**These are raw cumulative price returns, not CAR or abnormal returns.** No benchmark is subtracted. Filing time is absent, so after-hours disclosures may affect the next session. Other news can explain price moves. Inspect the source filing before interpreting the chart.

## Architecture

```text
SEC company identifiers ─┬─ company table (PostgreSQL)
Historical prices ──────┴─ daily_price table (PostgreSQL)
SEC filings ────────────── document store (MongoDB)
                          ↓ join by company and date
                    Flask research interface
                          ↓ portfolio export
                 standalone HTML + aggregate JSON
```

Original database notebook: `notebooks/original_database_workflow.ipynb`. It includes table recreation cells; use an isolated development database. The portfolio export does not connect to a database or execute those cells. Credentials have been removed from the archive.

## Reproduce locally

```bash
python -m venv .venv
# Activate .venv using your platform's standard command.
python -m pip install -r requirements.txt
python src/build_demo.py --source /path/to/headerless_exports
python src/render_site.py
```

Use an authorized local copy of the original dataset. Raw data is not required to inspect the checked-in aggregate results or to open the interactive demo. Original datasets are not silently replaced with synthetic data.

## Data and attribution

This is a team coursework project. Existing authorship in source material is retained. Source code cleanup and presentation do not imply sole authorship of the original work. No third-party data license is granted by this repository; source datasets and third-party materials retain their original terms. The original source URL/license still needs to be documented where noted in `data/README.md`.
