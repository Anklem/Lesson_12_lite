import json
import os
import shutil
import time
from datetime import date
from pathlib import Path
from jsonschema import validate, ValidationError

from file_info import FileInfo, FileInfoEncoder, file_info_schema
from utils import log_file_action, get_dir_size

# Создание и управление директориями:
# Напишите скрипт, который автоматически создаст следующую структуру директорий для вашего проекта:
# project_root/
# ├── data/
# │   ├── raw/
# │   ├── processed/
# ├── logs/
# ├── backups/
# └── output/
# Убедитесь, что все директории созданы, и если они уже существуют, не вызывайте ошибку.
dir_data = "project_root/data"
dir_raw = "project_root/data/raw"
dir_processed = "project_root/data/processed"
dir_logs = "project_root/logs"
dir_backups = "project_root/backups"
dir_output = "project_root/output"

dir_restore = "project_root/restore"

dirs = [dir_data, dir_raw, dir_processed, dir_logs, dir_backups, dir_output]

for d in dirs:
    os.makedirs(d, exist_ok=True)

for d in dirs:
    print(f"{d} существует: {os.path.exists(d)}")

# Создание и запись данных в файлы:
# В директории data/raw/ создайте несколько текстовых файлов с произвольным содержимым на разных языках,
# используя разные кодировки (например, UTF-8, ISO-8859-1).
# Заполните директорию logs/ лог-файлом с записями о выполнении предыдущих шагов,
# включая дату и время создания файлов и директорий.
file_1 = "project_root/data/raw/text_file_1.txt"
with open(file_1, "w", encoding='iso-8859-1') as tf_1:
    tf_1.writelines(["Hello, world!", "Bye, world!"])

file_2 = "project_root/data/raw/text_file_2.txt"
with open(file_2, "w", encoding='utf-8') as tf_2:
    tf_2.writelines(["Hello, UTF world!", "Bye, UTF world!"])

for d in dirs:
    log_file_action("создание директории", d)

log_file_action("запись строки", file_1)
log_file_action("запись строки", file_2)

# Чтение и обработка данных:
# Напишите скрипт, который будет автоматически читать все файлы из директории data/raw/, корректно определяя их кодировки.
# Выполните преобразование данных из каждого файла, заменяя в них все заглавные буквы на строчные и наоборот.
# Сохраните обработанные данные в новые файлы в директорию data/processed/ с сохранением исходных имен файлов,
# но добавив к ним суффикс _processed.
raw_files = os.listdir(dir_raw)
for f in raw_files:
    with open(os.path.join(dir_raw, f), "r") as raw_file:
        print(f"Кодировка {raw_file.name}: {raw_file.encoding}")
        content = raw_file.read()
        file_path = Path(raw_file.name)
        with open(os.path.join(dir_processed, file_path.stem + "_processed" + file_path.suffix), "w") as processed_file:
            processed_file.write(content.swapcase())

# Сериализация данных:
# Напишите скрипт для сериализации содержимого всех файлов из директории data/processed/ в один JSON-файл.
# Включите в этот JSON-файл следующую информацию:
# Имя файла, исходный текст, преобразованный текст, размер файла в байтах, дата последнего изменения файла.
# Сохраните JSON-файл в директорию output/ с именем processed_data.json.
processed_files = os.listdir(dir_processed)
root = []
for f in processed_files:
    with open(os.path.join(dir_processed, f), "r") as processed_file:
        content = processed_file.read()
        root.append({
            "File": processed_file.name,
            "Source text": content.swapcase(),
            "Processed text": content,
            "File size, bytes": os.path.getsize(processed_file.name),
            "Last edit time": time.ctime(os.path.getmtime(processed_file.name))
        })

with open(os.path.join(dir_output, "processed_data.json"), "w", encoding='utf-8') as json_file:
    json.dump(root, json_file, indent=4)

# Создание резервной копии:
# Напишите скрипт, который автоматически создаст архив резервной копии всех файлов из директории data/ и сохранит его
# в директорию backups/ с именем backup_<дата>.zip, где <дата> — текущая дата в формате YYYYMMDD.
zip_file = dir_backups + "/backup_" + date.today().strftime("%Y%m%d")
shutil.make_archive(zip_file, "zip", dir_data)

# Восстановление данных:
# Напишите скрипт для разархивирования и восстановления данных из созданного архива резервной копии.
# Убедитесь, что все файлы восстановлены в соответствующие директории, и их содержимое не повреждено.
os.makedirs(dir_restore, exist_ok=True)
shutil.unpack_archive(zip_file + ".zip", dir_restore, "zip")

data_size = get_dir_size(dir_data)
print(f"Суммарный размер файлов в папке {dir_data}: {data_size}")

restore_size = get_dir_size(dir_restore)
print(f"Суммарный размер файлов в папке {dir_restore}: {restore_size}")
if (data_size != restore_size):
    print("ОШИБКА! Данные разархивированы неправильно!")

# Работа с пользовательскими классами и JSON:
# Создайте класс FileInfo, который будет хранить информацию о файлах, включающую:
# Имя файла, полный путь к файлу, размер файла, даты создания и последнего изменения файла.
# Напишите скрипт, который собирает информацию обо всех файлах в директории data/processed/ и сериализует их в JSON-файл.
# Убедитесь, что при десериализации данные восстанавливаются корректно.
processed_files = os.listdir(dir_processed)
file_infos = []
for f in processed_files:
    with open(os.path.join(dir_processed, f), "r") as processed_file:
        file_infos.append(
            FileInfo(
                processed_file.name,
                processed_file.name,
                os.path.getsize(processed_file.name),
                os.path.getctime(processed_file.name),
                os.path.getmtime(processed_file.name)
            )
        )

with open(os.path.join(dir_output, "file_info.json"), "w", encoding='utf-8') as json_file:
    json.dump(file_infos, json_file, indent=4, cls=FileInfoEncoder)

print(f"Прочитано, сериализовано и сохранено {len(file_infos)} записей о файлах")

with open(os.path.join(dir_output, "file_info.json"), 'r') as file:
    file_infos_restored = json.load(file)
print(f"Прочитано и десериализовано {len(file_infos_restored)} записей о файлах:")
print("\t", file_infos_restored)

# Валидация JSON с использованием JSON Schema:
# Создайте JSON Schema для проверки структуры данных, созданной в предыдущем задании.
# Напишите скрипт, который проверяет валидность JSON-файла, созданного в предыдущем задании, с использованием созданной JSON Schema.
# Обработайте возможные ошибки валидации, предоставив отчет о найденных несоответствиях.
try:
    validate(instance=file_infos_restored, schema=file_info_schema)
    print("Данные валидны")
except ValidationError as e:
    print(f"Ошибка валидации: {e}")

# Создание итогового отчёта:
# Сгенерируйте отчёт в текстовом файле или в формате JSON с анализом выполнения всех заданий:
# Описание возникших трудностей и способы их решения.
# Время, затраченное на выполнение каждого задания.
# Выводы о проделанной работе и предложенные улучшения.

# --> Смотри report.txt

# Логирование и контроль версий: (по желанию, но если хотите "релевантный опыт", то сделайте)
# Подумайте о добавлении логирования во все скрипты для отслеживания ошибок и прогресса выполнения заданий.
# Опишите, как можно было бы интегрировать систему контроля версий (например, Git) в выполнение этого задания
# для отслеживания изменений и управления проектом.

# --> Выполнение каждого шага полностью логируется в консоли. При желании можно перенаправить этот поток в файл журнала.
# --> И проект уже интегрирован в GitHub, Вы должны проверять его именно там :)
