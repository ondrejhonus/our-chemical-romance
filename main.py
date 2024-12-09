import csv
import json

def load_elements_from_csv(filename):
    elements = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                elements.append({
                    'symbol': row['Symbol'],
                    'name': row['Element'],
                    'atomic_number': int(row['AtomicNumber']),
                    'group': row['Group'],
                    'period': int(row['Period']),
                    'atomic_weight': float(row['AtomicMass']),
                })
            except KeyError as e:
                print(f"Missing key in CSV file: {e}")
    return elements

def load_groups_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        groups = json.load(jsonfile)
    return groups

def display_menu():
    print("Chemická databáze")
    print("1. Vyhledat prvek")
    print("2. Zobrazit vlastnosti prvku")
    print("3. Výpočet průměrné relativní atomové hmotnosti")
    print("4. Generovat HTML tabulku")
    print("5. Export do JSON")
    print("6. Export do Markdown")
    print("7. Konec")

def get_user_choice():
    choice = input("Vyberte možnost: ")
    return choice

def find_element(elements, criteria, value):
    results = [element for element in elements if str(element[criteria]).lower() == value.lower()]
    return results

def display_element_properties(element):
    for key, value in element.items():
        print(f"{key}: {value}")

def calculate_average_atomic_weight(elements, group=None, period=None):
    filtered_elements = elements
    if group:
        filtered_elements = [e for e in elements if e['group'] == group]
    if period:
        filtered_elements = [e for e in elements if e['period'] == period]
    if not filtered_elements:
        return 0
    total_weight = sum(e['atomic_weight'] for e in filtered_elements)
    return total_weight / len(filtered_elements)

def generate_html_table(elements, filename="periodic_table.html"):
    with open(filename, 'w', encoding='utf-8') as htmlfile:
        htmlfile.write("<table border='1'>")
        htmlfile.write("<tr><th>Symbol</th><th>Name</th><th>Atomic Number</th><th>Group</th><th>Period</th><th>Atomic Weight</th></tr>")
        for element in elements:
            htmlfile.write(f"<tr><td>{element['symbol']}</td><td>{element['name']}</td><td>{element['atomic_number']}</td><td>{element['group']}</td><td>{element['period']}</td><td>{element['atomic_weight']}</td></tr>")
        htmlfile.write("</table>")

def export_elements_to_json(elements, filename="selected_elements.json"):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(elements, jsonfile, indent=4)

def export_elements_to_markdown(elements, filename="elements_overview.md"):
    with open(filename, 'w', encoding='utf-8') as mdfile:
        for element in elements:
            mdfile.write(f"## {element['name']} ({element['symbol']})\n")
            mdfile.write(f"- **Atomic Number:** {element['atomic_number']}\n")
            mdfile.write(f"- **Group:** {element['group']}\n")
            mdfile.write(f"- **Period:** {element['period']}\n")
            mdfile.write(f"- **Atomic Weight:** {element['atomic_weight']}\n\n")

def main():
    elements = load_elements_from_csv('elements.csv')
    groups = load_groups_from_json('groups.json')

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '1':
            criteria = input("Vyberte kritérium (symbol, name, atomic_number, group, period): ")
            value = input("Zadejte hodnotu: ")
            print(f"Searching for {criteria} = {value}")  # Debugging output
            results = find_element(elements, criteria, value)
            if results:
                for element in results:
                    display_element_properties(element)
            else:
                print("Žádný prvek nenalezen.")
        elif choice == '2':
            symbol = input("Zadejte symbol prvku: ")
            element = next((e for e in elements if e['symbol'].lower() == symbol.lower()), None)
            if element:
                display_element_properties(element)
            else:
                print("Prvek nenalezen.")
        elif choice == '3':
            group = input("Zadejte skupinu (nepovinné): ")
            period = input("Zadejte periodu (nepovinné): ")
            avg_weight = calculate_average_atomic_weight(elements, group, period)
            print(f"Průměrná relativní atomová hmotnost: {avg_weight}")
        elif choice == '4':
            generate_html_table(elements)
            print("HTML tabulka byla vygenerována.")
        elif choice == '5':
            symbol = input("Zadejte symbol prvku: ")
            element = next((e for e in elements if e['symbol'].lower() == symbol.lower()), None)
            if element:
                export_elements_to_json([element])
                print("Data byla exportována do JSON.")
            else:
                print("Prvek nenalezen.")
        elif choice == '6':
            group = input("Zadejte skupinu: ")
            group_elements = [e for e in elements if e['group'] == group]
            export_elements_to_markdown(group_elements)
            print("Data byla exportována do Markdown.")
        elif choice == '7':
            break
        else:
            print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    main()
