LOGFILE = "sample_auth_small.log"
# Назва файлу, з якого будемо читати дані

def ip_parse(line):
    """
    Функція знаходить усі IP-адреси в одному рядку (методом токенів).
    """
    parts = line.split()            # Розбиваємо рядок на окремі слова
    ips = []                        # Створюємо порожній список для знайдених IP

    for token in parts:             # Перебираємо кожне слово рядка
        token_clean = token.strip(",.;:")     # Видаляємо коми та інші символи
        numbers = token_clean.split(".")      # Розбиваємо токен по крапках

        # Перевіряємо, що це IP-адреса:
        if len(numbers) == 4 and all(num.isdigit() for num in numbers):
            ips.append(token_clean)           # Додаємо IP у список

    return ips                                # Повертаємо список IP-адрес

def main():
    unique_ips = set()          # Множина — автоматично видаляє дублікати
    lines_read = 0              # Лічильник кількості прочитаних рядків

    with open(LOGFILE, "r") as f:    # Відкриваємо файл для читання
        for line in f:               # Читаємо файл рядок за рядком
            lines_read += 1          # Збільшуємо лічильник прочитаних рядків

            ip_list = ip_parse(line)    # Отримуємо список IP з рядка

            if ip_list:                 # Якщо список не порожній
                for ip in ip_list:      # Перебираємо всі IP у рядку
                    unique_ips.add(ip)  # Додаємо до множини унікальних IP

    print(f"Lines read: {lines_read}")             # Загальна кількість рядків
    print(f"Unique IPs: {len(unique_ips)}")        # Кількість унікальних IP
    print(f"First 10 IPs: {sorted(unique_ips)[:10]}")  
    # Виводимо перші 10 IP у відсортованому вигляді

if __name__ == "__main__":
    main()  
    # Запускаємо головну функцію, якщо файл запущено напряму
