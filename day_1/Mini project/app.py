from reader import read_multiple_files
from analyzer import LogAnalyzer
from exporter import export_json, export_csv
from decorators import execution_time

LOG_FILES = [
    "sample_logs/app.log",
    "sample_logs/server.log"
]


@execution_time
def main():
    try:
        logs = read_multiple_files(LOG_FILES)
        analyzer = LogAnalyzer()
        analyzer.analyze(logs)
        report = analyzer.report()

        print("\nREPORT")
        print("=" * 40)
        for k, v in report.items():
            print(f"{k}: {v}")

        export_json(report, "reports/report.json")
        export_csv(report, "reports/report.csv")

        print("\nReports generated successfully.")

    except FileNotFoundError as e:
        print("Missing File:", e)
    except Exception as e:
        print("Unexpected Error:", e)


if __name__ == "__main__":
    main()
