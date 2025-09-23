LOGFILE = "sample_auth_small.log"
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


def main():
    unique_ips = set()
    lines_read = 0

    with open("sample_auth_small.log", "r") as f:
        for line in f:
            lines_read += 1
            ip = ip_parse(line)
            if ip:
                unique_ips.add(ip)

    print(f"Lines read: {lines_read}")
    print(f"Unique IPs: {len(unique_ips)}")
    print(f"First 10 IPs: {sorted(unique_ips)[:10]}")

if __name__ == "__main__":
    main()




    