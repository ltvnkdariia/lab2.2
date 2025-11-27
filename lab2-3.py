import json
from collections import defaultdict
from datetime import datetime, timedelta

LOGFILE = "sample_auth_small.log"   # назва лог-файлу


# ============================================================
#                    TASK 1 — Парсинг логів 
#  Парсимо один рядок: витягуємо timestamp, ip, event_type
# ============================================================

def parse_auth_line(line):
    """
    Парсимо рядок із SSH-логу.
    Повертаємо: timestamp (datetime), ip (str), event_type (str)
    Приклад рядка:
    Mar 10 13:58:01 host1 sshd[1023]: Failed password for invalid user admin from 203.0.113.45 port 52344 ssh2
    """

    parts = line.split()  # розбиваємо рядок на токени

    # ---- 1) Парсимо timestamp (додаємо вручну рік 2025) ----
    ts_str = " ".join(parts[0:3])   # 'Mar 10 13:45:01'
    try:
        ts = datetime.strptime("2025 " + ts_str, "%Y %b %d %H:%M:%S")
    except:
        ts = None   # якщо парсинг не вдалий

    # ---- 2) Визначаємо тип події ----
    event_type = "other"
    if "Failed password" in line:
        event_type = "failed"
    elif "Accepted password" in line or "Accepted publickey" in line:
        event_type = "accepted"

    # ---- 3) Витягуємо IP після слова 'from' ----
    ip = None
    if " from " in line:
        try:
            idx = parts.index("from")   # шукаємо токен 'from'
            ip = parts[idx + 1]         # IP йде одразу після нього
        except:
            ip = None

    return ts, ip, event_type



# ============================================================
#            TASK 2 — Виявлення brute-force атак
#  Знаходимо "вибухи" ≥5 невдалих входів за 10 хвилин
# ============================================================

def detect_bruteforce(per_ip_timestamps):
    """
    Отримує структура:
       { ip: [список datetime об’єктів з невдалими входами] }

    Повертає список інцидентів:
       {ip, count, first, last}
    """

    incidents = []
    window = timedelta(minutes=10)   # вікно 10 хвилин

    for ip, times in per_ip_timestamps.items():
        times.sort()                 # обов’язково сортовані!

        n = len(times)
        i = 0

        # техніка sliding window
        while i < n:
            j = i

            # розширюємо вікно вправо поки різниця <= 10 хвилин
            while j + 1 < n and (times[j+1] - times[i]) <= window:
                j += 1

            count = j - i + 1   # скільки спроб у цьому вікні

            if count >= 5:
                incidents.append({
                    "ip": ip,
                    "count": count,
                    "first": times[i].isoformat(),
                    "last": times[j].isoformat()
                })
                i = j + 1   # перескакуємо кластер, щоб не дублювати
            else:
                i += 1

    return incidents



# ============================================================
#      TASK 3 — Генерація репорту + (опціонально) bar-chart
# ============================================================

def save_reports(incidents, per_ip_timestamps):
    """
    Зберігаємо:
      1) brute_force_incidents.txt — красиво роздруковані інциденти
      2) failed_counts.json       — статистика за кількістю спроб
    """

    # ---- 1) Запис brute-force інцидентів ----
    with open("bruteforce_incidents.txt", "w") as f:
        f.write("Brute-force incidents:\n\n")
        f.write(json.dumps(incidents, indent=4))
        f.write("\n")

    # ---- 2) Підрахунок кількості failed спроб за IP ----
    counts = {ip: len(times) for ip, times in per_ip_timestamps.items()}

    with open("failed_counts.json", "w") as f:
        json.dump(counts, f, indent=4)



# ============================================================
#                        MAIN (запуск)
# ============================================================

if __name__ == "__main__":
    per_ip_timestamps = defaultdict(list)

    # ---- Читаємо лог-файл ----
    with open(LOGFILE, "r") as f:
        for line in f:
            ts, ip, event = parse_auth_line(line)

            # беремо лише невдалі спроби входу
            if ts and ip and event == "failed":
                per_ip_timestamps[ip].append(ts)

    # ---- TASK 2: виявляємо brute-force ----
    incidents = detect_bruteforce(per_ip_timestamps)

    # ---- TASK 3: генеруємо репорти ----
    save_reports(incidents, per_ip_timestamps)

    # ---- Консольний вивід ----
    print("Знайдено інцидентів brute-force:", len(incidents))
    print("\nПерші 5:")
    for i in incidents[:5]:
        print(i)
