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
                    'state': row['Phase']  # State of matter
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
    print("2. Výpočet průměrné relativní atomové hmotnosti")
    print("3. Generovat HTML tabulku")
    print("4. Export do JSON")
    print("5. Export do Markdown")
    print("6. Konec")

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
    # Vytvoření mřížky pro periodickou tabulku
    table = [["" for _ in range(18)] for _ in range(7)]

    # Naplnění mřížky prvky
    for element in elements:
        try:
            group = int(element['group'])
            period = int(element['period'])
            element_data = {
                "symbol": element['symbol'],
                "name": element['name'],
                "atomic_number": element['atomic_number'],
                "group": element['group'],
                "period": element['period'],
                "atomic_weight": element['atomic_weight'],
                "state": element['state'],
            }
            data_str = ",".join([f"{key}:'{value}'" for key, value in element_data.items()])
            table[period - 1][group - 1] = (
                f"<div class='element' onclick=\"showPopup({{{data_str}}})\">"
                f"<div class='atomic-number'>{element['atomic_number']}</div>"
                f"<div class='symbol'>{element['symbol']}</div>"
                f"<div class='name'>{element['name']}</div>"
                f"<div class='atomic-weight'>{element['atomic_weight']}</div>"
                f"</div>"
            )
        except ValueError:
            continue  # Přeskočí prvky s neplatnou skupinou nebo periodou

    # Generování HTML
    with open(filename, 'w', encoding='utf-8') as htmlfile:
        htmlfile.write("<!DOCTYPE html><html><head><style>")
        htmlfile.write("""
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        .periodic-table {
            display: grid;
            grid-template-columns: repeat(18, 1fr);
            gap: 2px;
            max-width: 95vw;
            max-height: 90vh;
        }
        .element {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            font-size: calc(0.6vw + 0.6vh);
            cursor: pointer;
        }
        .atomic-number {
            font-size: 0.7em;
            color: #666;
        }
        .symbol {
            font-size: 1.2em;
            font-weight: bold;
        }
        .name {
            font-size: 0.8em;
            color: #333;
        }
        .atomic-weight {
            font-size: 0.7em;
            color: #999;
        }
        .popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            padding: 20px;
            z-index: 1000;
            display: none;
        }
        .popup .close {
            position: absolute;
            top: 5px;
            right: 10px;
            cursor: pointer;
            color: #aaa;
        }
        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999;
            display: none;
        }
        </style></head><body>
        <div class='overlay' id='overlay' onclick='hidePopup()'></div>
        <div class='popup' id='popup'>
            <span class='close' onclick='hidePopup()'>×</span>
            <div id='popup-content'></div>
        </div>
        <div class='periodic-table'>
        """)

        for row in table:
            for cell in row:
                if cell:
                    htmlfile.write(cell)
                else:
                    # Prázdné místo v tabulce
                    htmlfile.write("<div class='element' style='background-color: #f0f0f0;'></div>")

        htmlfile.write("</div>")
        htmlfile.write("""
        <script>
        function showPopup(data) {
            const popup = document.getElementById('popup');
            const overlay = document.getElementById('overlay');
            const content = document.getElementById('popup-content');
            content.innerHTML = `
                <h2>${data.name} (${data.symbol})</h2>
                <p><strong>Atomic Number:</strong> ${data.atomic_number}</p>
                <p><strong>Group:</strong> ${data.group}</p>
                <p><strong>Period:</strong> ${data.period}</p>
                <p><strong>Atomic Weight:</strong> ${data.atomic_weight}</p>
                <p><strong>State:</strong> ${data.state}</p>
            `;
            popup.style.display = 'block';
            overlay.style.display = 'block';
        }
        function hidePopup() {
            const popup = document.getElementById('popup');
            const overlay = document.getElementById('overlay');
            popup.style.display = 'none';
            overlay.style.display = 'none';
        }
        </script>
        </body></html>
        """)

    print(f"Interaktivní periodická tabulka byla vygenerována a uložena jako {filename}.")
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
            mdfile.write(f"- **Atomic Weight:** {element['atomic_weight']}\n")
            mdfile.write(f"- **State:** {element['state']}\n\n")

def main():
    elements = load_elements_from_csv('elements.csv')
    groups = load_groups_from_json('groups.json')

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '1':
            criteria = input("Vyberte kritérium (symbol, name, atomic_number, group, period, state): ").strip()
            value = input("Zadejte hodnotu: ")
            print(f"Searching for {criteria} = {value}")  # Debugging output
            results = find_element(elements, criteria, value)
            if results:
                for element in results:
                    display_element_properties(element)
            else:
                print("Žádný prvek nenalezen.")
        elif choice == '2':
            group = input("Zadejte skupinu (nepovinné): ")
            period = input("Zadejte periodu (nepovinné): ")
            avg_weight = calculate_average_atomic_weight(elements, group, period)
            print(f"Průměrná relativní atomová hmotnost: {avg_weight}")
        elif choice == '3':
            generate_html_table(elements)
            print("HTML tabulka byla vygenerována.")
        elif choice == '4':
            symbol = input("Zadejte symbol prvku: ")
            element = next((e for e in elements if e['symbol'].lower() == symbol.lower()), None)
            if element:
                export_elements_to_json([element])
                print("Data byla exportována do JSON.")
            else:
                print("Prvek nenalezen.")
        elif choice == '5':
            group = input("Zadejte skupinu: ")
            group_elements = [e for e in elements if e['group'] == group]
            export_elements_to_markdown(group_elements)
            print("Data byla exportována do Markdown.")
        elif choice == '6':
            break
        else:
            print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    main()
