LOGFILE = "sample_auth_small.log"
from collections import defaultdict

def ip_parse(line):
    """
    Extracts the IP address that follows the token 'from' in the line.
    Returns None if no 'from' token or no IP found.
    """
    if " from " in line:
        parts = line.split()
        try:
            anchor = parts.index("from")
            ip = parts[anchor + 1]
            return ip.strip()
        except (ValueError, IndexError):
            return None
    return None

counts = defaultdict(int)  # dictionary with default int (0)

with open("sample_auth_small.log") as f:
    for line in f:
        if "Failed password" in line or "Invalid user" in line:
            ip = ip_parse(line)
            if ip:
                counts[ip] += 1

print(counts)
