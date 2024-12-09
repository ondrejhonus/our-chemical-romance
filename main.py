from functions.gen_html import generate_html_table
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

def main():
    elements = load_elements_from_csv('imports/elements.csv')
    groups = load_groups_from_json('imports/groups.json')

    while True:
        display_menu()
        choice = get_user_choice()
        if choice == '1':
            criteria = input("Vyberte kritérium (symbol, name, atomic_number, group, period, state): ").strip()
            value = input("Zadejte hodnotu: ")
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
            export_elements_to_markdown(elements)
            print("Data byla exportována do Markdown.")
        elif choice == '6':
            export_elements_to_xml(elements)
        elif choice == '7':
            break
        else:
            print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    main()