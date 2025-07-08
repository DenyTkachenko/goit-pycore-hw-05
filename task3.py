import argparse
from datetime import datetime

"""
Note: Since this assignment was optional, I deviated from some of the original instructions 
to create a highly optimized, universal, and efficient solution. 
This program is capable of processing log files of unlimited size. 
It can also filter logs and write the filtered results to files.
"""

def parse_log_line(line):
    """Parse log line"""
    parts = line.strip().split(maxsplit=3)
    if len(parts) < 4:
        return None
    date_str, time_str, level, message = parts
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        timestamp_ms = int(dt.timestamp() * 1000)
    except Exception:
        return None
    return {
        "timestamp_ms": timestamp_ms,
        "level": level.upper(),
        "message": message,
        "raw": line.strip()
    }

def load_logs(file_path):
    """Read logs lines by generator"""
    with open(file_path, "r") as f:
        for line in f:
            yield line

def display_log_counts(counts):
    """Display log statistics"""
    print("\n--- Total logs statistics ---")
    total = sum(counts.values())
    for level, count in counts.items():
        print(f"{level}: {count}")
    print(f"Total: {total}")

def get_selected_log_levels(args):
    levels = []
    if args.error: levels.append("ERROR")
    if args.warning: levels.append("WARNING")
    if args.debug: levels.append("DEBUG")
    if args.info: levels.append("INFO")
    return levels

def get_selected_log_period(args):
    """Get period filter value"""
    if hasattr(args, "period") and args.period:
        try:
            period_from_str, period_to_str = args.period.split(";")
            period_from = int(period_from_str)
            period_to = int(period_to_str)
            return period_from, period_to
        except Exception:
            print("Incorrect period format. Use --period from_ms;to_ms")
    return None, None

def main():
    parser = argparse.ArgumentParser(description="Log analyzer")
    parser.add_argument("file_path", help="Path to the log file")
    parser.add_argument("--error", action="store_true", help="Filter ERROR logs")
    parser.add_argument("--warning", action="store_true", help="Filter WARNING logs")
    parser.add_argument("--debug", action="store_true", help="Filter DEBUG logs")
    parser.add_argument("--info", action="store_true", help="Filter INFO logs")
    parser.add_argument("--period", help="Period in format from_ms;to_ms")
    parser.add_argument("--print", action="store_true", help="Print to console")
    parser.add_argument("--write", help="Write to file file_name")

    args = parser.parse_args()

    levels_filter = get_selected_log_levels(args)
    [ period_from, period_to ] = get_selected_log_period(args)


    # Open file to collect data by filters
    file_writer = open(args.write, "w", encoding="utf-8") if args.write else None

    # Total Counter init
    log_counts = {}

    if args.print:
        print("\n--- Selected logs ---")

    for line in load_logs(args.file_path):
        log = parse_log_line(line)
        if not log:
            continue

        # Filter by period
        if period_from is not None and not (period_from <= log["timestamp_ms"] <= period_to):
            continue

        # Total Counter
        log_counts[log["level"]] = log_counts.get(log["level"], 0) + 1

        # Filter by log lvl
        if bool(levels_filter) and log["level"] not in levels_filter:
            continue

        # Print to console
        if args.print:
            print(log["raw"])
        if file_writer:
            file_writer.write(log["raw"] + "\n")

    if file_writer:
        file_writer.close()

    display_log_counts(log_counts)

if __name__ == "__main__":
    main()
