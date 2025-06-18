import csv
from collections import defaultdict

attendance_file = "attendance.csv"
summary_txt_file = "summary_report.txt"
summary_csv_file = "summary_report.csv"

summary = defaultdict(list)

try:
    with open(attendance_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            student_id, name, timestamp = row
            date = timestamp.split(' ')[0]
            summary[date].append((student_id, name))
except FileNotFoundError:
    print("❌ attendance.csv not found.")
    exit()

# 1. ✅ Print to terminal
print("\n📊 Date-wise Attendance Summary:\n")
for date in sorted(summary):
    print(f"📅 {date}")
    for student_id, name in summary[date]:
        print(f" - {name} (ID: {student_id})")
    print()

# 2. ✅ Write to TXT file
with open(summary_txt_file, 'w', encoding='utf-8') as f:
    f.write("📊 Date-wise Attendance Summary\n\n")
    for date in sorted(summary):
        f.write(f"📅 {date}\n")
        for student_id, name in summary[date]:
            f.write(f" - {name} (ID: {student_id})\n")
        f.write("\n")
print(f"📁 Summary saved to {summary_txt_file}")

# 3. ✅ Write to CSV file
with open(summary_csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Student ID", "Name"])
    for date in sorted(summary):
        for student_id, name in summary[date]:
            writer.writerow([date, student_id, name])
print(f"📁 Summary saved to {summary_csv_file}")
