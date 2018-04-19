# News Recommendation System

## News Pipeline
Implemented a data pipeline which monitors, scrapes and dedupes latest news (MongoDB, Redis, RabbitMQ, TF- IDF)

### 1 News Monitor
News API -> Redis(Deduplication url) -> Scraping MQ

### 2 News Fetcher
Scraping MQ -> News Fetcher -> Dedupe MQ
