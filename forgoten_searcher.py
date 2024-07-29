import json
import os

def search_string_in_file(string, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        if string in content:
            return True
    return False

def main():

    with open('COMPONENTS_TO_SEARCH.json', 'r', encoding='utf-8') as file:
        components_to_search = json.load(file)

    with open('VUE_FILES.json', 'r', encoding='utf-8') as file:
        vue_files = json.load(file)

    components_forgotten = []

    for component in components_to_search['SEARCH_THIS']:
        found = False
        for vue_file in vue_files['VUE_FILES']:
            if search_string_in_file(component, vue_file):
                found = True
                break
        if not found:
            components_forgotten.append(component)

    with open('COMPONENTS_FORGOTTEN.json', 'w', encoding='utf-8') as file:
        json.dump({'FORGOTTEN_COMPONENTS': components_forgotten}, file, ensure_ascii=False, indent=4)

    print("Processo concluído. Verifique COMPONENTS_FORGOTTEN.json para os componentes não encontrados.")


if __name__ == '__main__':
  main()
