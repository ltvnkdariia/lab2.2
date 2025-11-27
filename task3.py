import time   # Імпортуємо модуль для вимірювання часу роботи програми

LOGFILE = "sample_auth_small.log"  
# Назва файлу з логами, який будемо аналізувати

def ip_parse(line):
    """
    Функція знаходить усі IP-адреси в одному рядку.
    Використовує токенізацію (split) замість regex.
    """
    parts = line.split()           # Розбиваємо рядок на слова
    ips = []                       # Порожній список для зібраних IP

    for token in parts:            # Перебираємо кожне слово
        token_clean = token.strip(",.;:")  # Видаляємо зайві символи
        numbers = token_clean.split(".")   # Розбиваємо слово по крапках

        if len(numbers) == 4 and all(num.isdigit() for num in numbers):
            ips.append(token_clean)        # Якщо токен схожий на IP — додаємо

    return ips                             # Повертаємо всі IP, знайдені в рядку

def top_n(counts, n=5):
    # Сортуємо словник {ip: count} за кількістю (value), від більшого до меншого
    return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:n]

def main():
    start = time.time()   # Запам’ятовуємо час початку виконання

    failed_counts = {}    # Словник: {ip: кількість_невдалих_спроб}
    lines_read = 0        # Лічильник прочитаних рядків

    with open(LOGFILE, "r") as f:          # Відкриваємо лог-файл
        for line in f:                     # Читаємо покроково
            lines_read += 1                # Збільшуємо лічильник рядків

            if "Failed" not in line:       # Якщо в рядку немає невдалої спроби — ігноруємо
                continue

            ips = ip_parse(line)           # Витягуємо IP з рядка

            if ips:                        # Якщо є принаймні один IP
                ip = ips[0]                # Беремо перший IP у рядку
                failed_counts[ip] = failed_counts.get(ip, 0) + 1  
                # Якщо IP вже є — збільшуємо лічильник
                # Якщо нема — ставимо 1

    # Беремо топ-5 IP-адрес за кількістю невдалих спроб
    top5 = top_n(failed_counts, 5)

    print("\nTop 5 attacker IPs:")           # Заголовок

    rank = 1                                 # Номер у рейтингу
    for ip, count in top5:                   # Перебираємо top-5
        print(f"{rank}. {ip} — {count}")     # Друкуємо у форматі: 1. IP — Count
        rank += 1

    # Записуємо всі результати у файл failed_counts.txt
    with open("failed_counts.txt", "w") as out:
        out.write("ip,failed_count\n")        # Заголовок CSV-файлу
        for ip, count in failed_counts.items():
            out.write(f"{ip},{count}\n")      # Запис кожного IP і його кількості

    print("\nWrote failed_counts.txt")       # Підтвердження запису

    end = time.time()                        # Час завершення
    print("Elapsed:", round(end - start, 3), "seconds")   # Тривалість роботи

if __name__ == "__main__":
    main()   # Запуск головної функції
