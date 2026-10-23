# Sources and export schemas

SEC EDGAR filings: https://www.sec.gov/edgar/search/
Original source workflow retrieves historical prices through yfinance. Observe the provider terms when obtaining data; full price series and full filing text are not republished. The standalone page contains bounded event-window returns and public SEC links.

The original CSV exports have NO HEADER. `src/build_demo.py` expects:

- company.csv: company_id, cik, ticker, company_name, sic, sic_description
- daily_price.csv: company_id, trade_date, open, high, low, close, adj_close, volume
- sec_filings.csv: original 13-column export; indices used are accession=1, company_id=3, filing_date=5, form=6, source index URL=9, document URL=10.

Original filing text is deliberately excluded from published JSON. The default scan is capped at 600 source filings and exports at most 75 matched events. The exports are historical snapshots and are not updated live.
