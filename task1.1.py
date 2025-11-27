LOGFILE = "sample_auth_small.log"  
# Назва файлу з логами, який будемо читати

def ip_parse(line):
    """
    Функція виділяє всі IP-адреси з одного рядка (через токени).
    """
    parts = line.split()             # Розбиваємо рядок на слова (токени)
    ips = []                         # Список, куди додамо знайдені IP

    for token in parts:              # Перебираємо кожне слово рядка
        token_clean = token.strip(",.;:")    # Прибираємо розділові знаки
        numbers = token_clean.split(".")     # Розбиваємо слово по крапках
        if len(numbers) == 4 and all(num.isdigit() for num in numbers):
            ips.append(token_clean)          # Якщо це IP — додаємо його

    return ips                             # Повертаємо список IP

def main():
    unique_ips = set()      # Множина для зберігання унікальних IP
    lines_read = 0          # Лічильник кількості прочитаних рядків

    with open("sample_auth_small.log", "r") as f:
        # Відкриваємо файл для читання

        for line in f:                     # Читаємо файл рядок за рядком
            lines_read += 1               # Збільшуємо лічильник рядків

            ip = ip_parse(line)           # Викликаємо функцію парсингу IP
            
            if ip:                        # Якщо список IP не порожній
                for one_ip in ip:         # Перебираємо всі IP у рядку
                    unique_ips.add(one_ip)  # Додаємо у множину (уникнення дублікатів)

    print(f"Lines read: {lines_read}")            # Виводимо кількість прочитаних рядків
    print(f"Unique IPs: {len(unique_ips)}")       # Виводимо кількість унікальних IP
    print(f"First 10 IPs: {list(sorted(unique_ips))[:10]}")  
    # Виводимо перші 10 IP у відсортованому вигляді

if __name__ == "__main__":
    main()  
    # Запускаємо main() тільки якщо файл запущено напряму





    