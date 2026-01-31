# CSV_processer

## Установка и запуск

### Настройка среды и зависимостей

Перейдите в репозиторий проекта и введите

```bash
python -m venv venv
.\venv\Scripts\activate  
pip install -r requirements.txt 
```

### Запуск

```bash
python main.py -f имя_файла(по умолчанию test_data из корня) -*(ваши аттрибуты) 
python main.py -h # для информации по аттрибутам
```

#### Примеры запуска

```bash
python main.py -f test_data.csv -o brand=desc 
python main.py -f test_data.csv -a price=avg 
python main.py -w rating=asc
```

Сочетание аттрибутов аггрегации и сортировки выдаст кастомную ошибку

## Важные комментарии

### 1) Гибкое добавление функций аггрегирования

Создаем функцию и добавляем в словарь func_name_dict с ключом ее строкового названия.
Это изолирует код, недопуская использование сторонних функций
