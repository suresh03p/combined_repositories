# Enterprise Concurrent Data Collection System

This project is designed to collect data from multiple REST APIs at the same time, process the results, and generate useful reports for analysis. It uses Python concurrency features such as asyncio, aiohttp, ThreadPoolExecutor, and ProcessPoolExecutor to make the workflow efficient and scalable.

## Project Purpose
The system is built to:
- fetch data from several APIs concurrently,
- retry any failed requests,
- handle request timeouts safely,
- log failed requests for debugging and monitoring,
- parse and clean the received data,
- remove duplicates,
- validate records,
- aggregate the final results,
- generate reports in CSV and JSON format.

## Main Features
- Concurrent API collection using asyncio and aiohttp
- Retry logic for failed requests
- Graceful timeout handling
- Structured logging for failures and progress
- Data validation and deduplication
- Report generation for response time, success/failure, data volume, and processing time
- Export to CSV and JSON files

## Folder Structure
```text
enterprise_data_collector/
├── app.py
├── config.py
├── api_client.py
├── async_tasks.py
├── processor.py
├── exporter.py
├── logger.py
├── utils.py
├── reports/
├── data/
├── config/
│   └── config.json
├── README.md
└── requirements.txt
```

## How It Works
1. The application reads configuration from the JSON file.
2. It sends requests to multiple endpoints concurrently.
3. Failed requests are retried and logged.
4. JSON responses are parsed and cleaned.
5. Valid records are deduplicated and aggregated.
6. Reports are generated and saved in the reports and data folders.

## Running the Project
Install the dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python app.py
```

## Example Output
The application generates:
- reports/reports.json
- data/processed_records.json
- data/processed_records.csv
