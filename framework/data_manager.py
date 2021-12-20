from pathlib import PurePath
import json

class DataForSave:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def save(self, file_name):
        path = PurePath(__file__).parent.parent / 'data_files' / file_name
        file_content = []
        try:
            with open(path, "r", encoding='UTF-8') as f:
                file_content = json.load(f)
        except Exception:
            pass

        file_content.append(self.data)
        #print(file_content)
        with open(path, "w", encoding='UTF-8') as f:
            f.write(json.dumps(file_content, indent=2, ensure_ascii=False))

        print(f"Запись сохранена в файл {path}")
