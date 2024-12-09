import csv
import json

def load_elements_from_csv(filename):
    """
    Načte prvky z CSV souboru a uloží je do seznamu slovníků.
    - Každý prvek je reprezentován jako slovník s klíči: 'symbol', 'name', 'atomic_number', 'group', 'period', 'atomic_weight', 'state'.
    """
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
    """
    Načte data o skupinách prvků z JSON souboru a vrátí je jako seznam slovníků.
    """
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        groups = json.load(jsonfile)
    return groups

def display_menu():
    """
    Zobrazí hlavní menu aplikace s možnostmi pro uživatele.
    """
    print("Chemická databáze")
    print("1. Vyhledat prvek")
    print("2. Výpočet průměrné relativní atomové hmotnosti")
    print("3. Generovat HTML tabulku")
    print("4. Export do JSON")
    print("5. Export do Markdown")
    print("6. Export do XML")
    print("7. Konec")

def get_user_choice():
    """
    Získá vstup od uživatele pro výběr akce v menu.
    """
    choice = input("Vyberte možnost: ")
    return choice

def find_element(elements, criteria, value):
    """
    Vyhledá prvek v seznamu 'elements' podle zadaného kritéria (např. symbol, název).
    Vrátí seznam prvků, které odpovídají kritériu.
    """
    results = [element for element in elements if str(element[criteria]).lower() == value.lower()]
    return results

def display_element_properties(element):
    """
    Zobrazí všechny vlastnosti daného prvku (např. symbol, název, atomové číslo, skupina, perioda).
    """
    for key, value in element.items():
        print(f"{key}: {value}")

def calculate_average_atomic_weight(elements, group=None, period=None):
    """
    Vypočítá průměrnou atomovou hmotnost prvků podle zadané skupiny nebo periody.
    Pokud nejsou zadané žádné filtry, počítá průměrnou hmotnost pro všechny prvky.
    """
    filtered_elements = elements
    if group:
        filtered_elements = [e for e in elements if e['group'] == group]
    if period:
        filtered_elements = [e for e in elements if e['period'] == period]
    if not filtered_elements:
        return 0
    total_weight = sum(e['atomic_weight'] for e in filtered_elements)
    return total_weight / len(filtered_elements)

def export_elements_to_json(elements, filename="generated/selected_element.json"):
    """
    Exportuje seznam prvků do JSON souboru.
    Každý prvek je uložen jako slovník se všemi vlastnostmi.
    """
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(elements, jsonfile, indent=4)

def export_elements_to_markdown(elements, filename="generated/elements_overview.md"):
    """
    Exportuje seznam prvků do Markdown souboru.
    Každý prvek je zapsán jako nadpis a seznam jeho vlastností (např. atomové číslo, skupina, perioda).
    """
    with open(filename, 'w', encoding='utf-8') as mdfile:
        for element in elements:
            mdfile.write(f"## {element['name']} ({element['symbol']})\n")
            mdfile.write(f"- **Atomic Number:** {element['atomic_number']}\n")
            mdfile.write(f"- **Group:** {element['group']}\n")
            mdfile.write(f"- **Period:** {element['period']}\n")
            mdfile.write(f"- **Atomic Weight:** {element['atomic_weight']}\n")
            mdfile.write(f"- **State:** {element['state']}\n\n")

def export_elements_to_xml(elements, filename='generated/elements.xml'):
    """
    Exportuje seznam prvků do XML souboru.
    Vytvoří XML strukturu s každým prvkem jako element, jeho vlastnosti jako podřízené elementy.
    """
    import xml.etree.ElementTree as ET

    root = ET.Element("elements")
    for element in elements:
        element_elem = ET.SubElement(root, "element")
        for key, value in element.items():
            child = ET.SubElement(element_elem, key)
            child.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    print(f"Data byla exportována do XML souboru {filename}.")