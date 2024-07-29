import json
import os
import argparse

def search_string_in_file(string, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        if string in content:
            return True
    return False

def create_components_to_search_json(project_directory):
    vue_files = []
    for root, dirs, files in os.walk(project_directory):
        for file in files:
            if file.endswith('.vue'):
                vue_files.append(file)

    components_to_search = {'SEARCH_THIS': vue_files}

    components_file_path = os.path.join(project_directory, 'COMPONENTS_TO_SEARCH.json')
    with open(components_file_path, 'w', encoding='utf-8') as file:
        json.dump(components_to_search, file, ensure_ascii=False, indent=4)

def main(project_directory):

    create_components_to_search_json(project_directory)

    components_file_path = os.path.join(project_directory, 'COMPONENTS_TO_SEARCH.json')
    vue_files_path = os.path.join(project_directory, 'VUE_FILES.json')
    
    with open(components_file_path, 'r', encoding='utf-8') as file:
        components_to_search = json.load(file)

    with open(vue_files_path, 'r', encoding='utf-8') as file:
        vue_files = json.load(file)

    components_forgotten = []

    for component in components_to_search['SEARCH_THIS']:
        found = False
        for vue_file in vue_files['VUE_FILES']:
            vue_file_path = os.path.join(project_directory, vue_file)
            if search_string_in_file(component, vue_file_path):
                found = True
                break
        if not found:
            components_forgotten.append(component)

    forgotten_components_path = os.path.join(project_directory, 'COMPONENTS_FORGOTTEN.json')
    with open(forgotten_components_path, 'w', encoding='utf-8') as file:
        json.dump({'FORGOTTEN_COMPONENTS': components_forgotten}, file, ensure_ascii=False, indent=4)

    print(f"Processo concluído. Verifique {forgotten_components_path} para os componentes não encontrados.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analisa arquivos .vue em um projeto Vue.js para identificar arquivos não utilizados ou esquecidos.')
    parser.add_argument('project_directory', type=str, help='O diretório do projeto Vue a ser analisado.')
    args = parser.parse_args()
    
    main(args.project_directory)
