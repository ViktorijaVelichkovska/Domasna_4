import os
import pandas as pd

# Патека до папката со CSV фајлови
folder_path = "all_data"  # Увери се дека оваа папка постои

# Проверка дали папката постои
if not os.path.exists(folder_path):
    print(f"Папката '{folder_path}' не постои. Проверете ја патеката.")
    exit()

# Листа за чување на сите податоци
all_data = []

# Процесирање на секој CSV фајл во папката
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)

        # Обиди се да го прочиташ фајлот
        try:
            # Пробај со различни сепаратори, автоматски препознај
            data = pd.read_csv(file_path, sep=",", encoding="utf-8")
        except Exception as e:
            print(f"Грешка при читање на фајлот {filename}: {e}")
            continue

        # Испечати ги колоните за да се осигуриме дека ги читаме точно
        print(f"Имиња на колони во {filename}: {data.columns.tolist()}")

        # Чистење на имињата на колоните од евентуални празни места
        data.columns = data.columns.str.strip()

        # Проверка дали колоната 'date' постои
        if 'date' in data.columns:
            try:
                # Претвори ја колоната 'date' во формат datetime
                data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')
            except Exception as e:
                print(f"Грешка при претворање на 'date' во {filename}: {e}")
                continue
        else:
            print(f"Колоната 'date' не постои во {filename}")
            continue

        # Додај го обработениот DataFrame во листата
        all_data.append(data)

# Комбинирај ги сите податоци во еден DataFrame
if all_data:
    try:
        final_data = pd.concat(all_data, ignore_index=True)
        print("Успешно комбинирани податоци.")

        # Зачувај го комбинираниот DataFrame во нов CSV фајл
        output_path = r"C:\Users\Viktorija\Desktop\Domasna_3\combined_data.csv"
        final_data.to_csv(output_path, index=False, sep=",", encoding="utf-8")
        print(f"Комбинираните податоци се зачувани во: {output_path}")
    except Exception as e:
        print(f"Грешка при комбинирање или зачувување на податоците: {e}")
else:
    print("Не се најдоа валидни податоци за комбинирање.")
