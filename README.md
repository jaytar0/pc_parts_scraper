# pc_parts_scraper
Short project for scraping pc-parts-picker site. Features data scraping and database design.
Disclaimer: this project was started prior to the DE end to end project and I plan to flesh this out in the future so I have an analytical dashboard with daily updates.


### Formatting
Described in the formatting txt file, but lists out my idea for how the database schema should be as I scraped the website. This makes it easier in putting the parquet files to a posgresql, GCP, miniIO if I choose to in the future.

### Scripts
**Build Summary:** Refers to the rough scrape of data and sublinks gathered from the list of pc builds on the main listings page.
**Build Details:** Refers to the additional details like date and cost scraped from the direct link in a particular listing entry.
**Build List:** Scraping a sepearte link that lists the actual components used along with the component price.
**Merger:** Merges the gathered chunks of data into one uniform parquet.
**Scraper Main::** Main handler for scraper logging and inputs.

### Next Steps
- My main idea for gathering this data was to monitor current builds and trends so I could have insight into what people were using for current pc builds since I wanted to build one of my own.
- Could turn into a larger data project where I continuously scrape and store the data, via googles compute engine / EC2 equivalent orchestrate these processes using airflow and dumping into google storage or s3 bucket, on a daily basis for new entries.
- Then do some data quality checks via another script in the pipeline and send to googles cloud database and work with bigquery.
- Do further transformations with Data Build Tool (DBT) to flesh out certain models depending on what I want to do next (ML, Analytics, etc.)
- Send to either looker or powerbi for continual monitoring.
