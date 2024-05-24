import json,os

def company_getter():
    companies = []
    archivos = os.listdir('.\\Results\\')
    for archivo in archivos:
        with open('.\\Results\\' + archivo,'r') as file:
            dicc = json.load(file)
        for keys,values in dicc.items():
            if values['company'] == 'No tiene': continue
            companies.append(values['company'])
    with open('.\\Companies\\companies.json','w') as file:
        json.dump(list(set(companies)),file,indent=2)
    print('Done')

if __name__ == '__main__':
    company_getter()