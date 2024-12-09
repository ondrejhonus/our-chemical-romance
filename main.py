

# Import funkce generate_html_table z modulu functions.gen_html
from functions.gen_html import generate_html_table
# Import funkcí z modulu functions.all_func
from functions.all_func import (
    load_elements_from_csv,
    load_groups_from_json,
    display_menu, 
    get_user_choice, 
    find_element,
    display_element_properties,
    calculate_average_atomic_weight,
    export_elements_to_json,
    export_elements_to_markdown,
    export_elements_to_xml
)

elements = load_elements_from_csv('imports/elements.csv')  # Načte prvky z CSV souboru
groups = load_groups_from_json('imports/groups.json')  # Načte skupiny z JSON souboru

while True:
    display_menu()  # Spustí funkci pro zobrazení menu
    choice = get_user_choice()  # Získá výběr uživatele
    if choice == '1':
        criteria = input("Vyberte kritérium (symbol, name, atomic_number, group, period, state): ").strip()
        value = input("Zadejte hodnotu: ")
        results = find_element(elements, criteria, value)  # Najde prvky podle kritéria a hodnoty
        if results:
            for element in results:
                display_element_properties(element)  # Zobrazí vlastnosti nalezených prvků
        else:
            print("Žádný prvek nenalezen.")
    elif choice == '2':
        group = input("Zadejte skupinu (nepovinné): ")
        period = input("Zadejte periodu (nepovinné): ")
        avg_weight = calculate_average_atomic_weight(elements, group, period)  # Vypočítá průměrnou atomovou hmotnost
        print(f"Průměrná relativní atomová hmotnost: {avg_weight}")  # Zobrazí průměrnou atomovou hmotnost
    elif choice == '3':
        generate_html_table(elements)  # Vygeneruje HTML tabulku
        print("HTML tabulka byla vygenerována.")
    elif choice == '4':
        symbol = input("Zadejte symbol prvku: ")
        element = next((e for e in elements if e['symbol'].lower() == symbol.lower()), None) # Najde prvek podle symbolu
        if element:
            export_elements_to_json([element])  # Exportuje prvek do JSON
            print("Data byla exportována do JSON.")
        else:
            print("Prvek nenalezen.")
    elif choice == '5':
        export_elements_to_markdown(elements)  # Exportuje prvky do Markdown
        print("Data byla exportována do Markdown.")
    elif choice == '6':
        export_elements_to_xml(elements)  # Exportuje prvky do XML
    elif choice == '7':
        break  # Ukončí program
    else:
        print("Neplatná volba, zkuste to znovu.")
