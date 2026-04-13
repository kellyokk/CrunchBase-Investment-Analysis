# CrunchBase-Investment-Analysis
This project demonstrates end-to-end data analysis on the Crunchbase startup investment dataset 
The analysis is conducted entirely in Python with SQLite.
The dataset, crunchbase_investments.csv, is a flat file export from Crunchbase containing records of startup funding rounds. Each row represents a single investment event between an investor and a company.

This analysis surfaces several meaningful insights from the Crunchbase dataset while building a foundation for deeper investigation:
- Biotech is the single largest recipient of venture capital by dollar volume ($110B+), while Software leads in deal frequency, highlighting a distinction between capital intensive and volume driven sectors.
- Startup funding activity peaked in Quarter 2; 2008 and rebounded strongly post 2009, with deal volume nearly doubling from 2010 to 2013.
- Top-tier investors like NEA and Sequoia maintain diversified portfolios of 200+ companies, with clear sector specialisations that can be extracted programmatically using window functions.
- Approximately 30% of seed funded companies do not appear in Series C+ records, suggesting a meaningful attrition rate across the startup lifecycle.
- Data quality is a material concern: 95% missing rates in investor_category_code render it unusable, and non-random missingness in raised_amount_usd requires careful handling in funding analyses.
