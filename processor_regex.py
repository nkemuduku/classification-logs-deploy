import re

regex_patterns = {
    r"User User\d+ logged (In|Out).*": "User Action",
    r"Backup completed successfully.*": "System Notification",
    r"Backup (started|ended) at.*": "System Notification",
    r"System updated to version.*": "System Notification",
    r"File.* (uploaded|updated) successfully by user.*": "System Notification",
    r"Disk cleanup completed successfully.*": "System Notification",
    r"System reboot initiated by user.*": "System Notification",
    r"Account with ID.*": "User Action",
}

def classify_with_regex(log_message):
    for pattern, label in regex_patterns.items():
        if re.search(pattern, log_message, re.IGNORECASE):
            return label
    return None


if __name__ == "__main__":
    print(classify_with_regex("System reboot initiated by user."))
    print(classify_with_regex("Backup completed successfully."))
    print(classify_with_regex("Backup started at 12:00."))
    print(classify_with_regex("System updated to version 1.0.0."))
    print(classify_with_regex("System reboot initiated by user User123."))
    print(classify_with_regex("File file1.txt uploaded successfully by user User123."))
    print(classify_with_regex("Disk cleanup completed successfully."))
    print(classify_with_regex("Hey bro, chill out."))
