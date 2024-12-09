import json
groups_filename = 'imports/groups.json'

def generate_html_table(elements, filename="generated/periodic_table.html"):
    # Načtení skupin z JSON
    with open(groups_filename, 'r', encoding='utf-8') as file:
        groups = json.load(file)

    # Přiřazení skupin prvkům
    element_classes = {}
    group_colors = {}
    css_rules = []
    for group in groups:
        group_name = group['cs']
        color = f"hsl({len(group['elements']) * 30}, 70%, 80%)"  # Dynamická barva
        group_colors[group_name] = color
        css_rules.append(f".{group_name.replace(' ', '_')} {{ background-color: {color}; }}")
        for element in group['elements']:
            element_classes[element] = group_name.replace(' ', '_')

    # Oddělení lanthanoidů a aktinoidů
    lanthanoids = [e for e in elements if 57 <= e['atomic_number'] <= 71]
    actinoids = [e for e in elements if 89 <= e['atomic_number'] <= 103]
    main_elements = [e for e in elements if e not in lanthanoids and e not in actinoids]

    # Vytvoření mřížky pro periodickou tabulku
    table = [["" for _ in range(18)] for _ in range(7)]

    for element in main_elements:
        try:
            group = int(element['group'])
            period = int(element['period'])
            element_class = element_classes.get(element['symbol'], "unknown")
            if element['atomic_number'] == 57 or element['atomic_number'] == 89:
                # Prázdné místo pro lanthanoidy/aktinoidy
                table[period - 1][group - 1] = "<div class='empty'></div>"
            else:
                table[period - 1][group - 1] = (
                    f"<div class='element {element_class}' onclick=\"showPopup('{element['symbol']}', '{element['name']}', {element['atomic_number']}, '{element['group']}', '{element['period']}', {element['atomic_weight']}, '{element['state']}')\">"
                    f"<div class='atomic-number'>{element['atomic_number']}</div>"
                    f"<div class='symbol'>{element['symbol']}</div>"
                    f"<div class='name'>{element['name']}</div>"
                    f"<div class='atomic-weight'>{element['atomic_weight']}</div>"
                    f"</div>"
                )
        except ValueError:
            continue

    # Generování HTML
    with open(filename, 'w', encoding='utf-8') as htmlfile:
        htmlfile.write("<!DOCTYPE html><html><head><style>")
        htmlfile.write("""
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
        }
        .periodic-table {
            display: grid;
            grid-template-columns: repeat(18, 1fr); /* All columns have the same width */
            gap: 2px;
            max-width: 95vw;
            margin: auto;
        }
        .lanthanoids, .actinoids {
            display: grid;
            grid-template-columns: repeat(15, 1fr);
            gap: 2px;
            margin: 10px auto;
            max-width: 95vw;
        }
        .lanthanoids {
            margin-bottom: 20px; /* Add margin to separate lanthanoids and actinoids */
        }
        .element {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            cursor: pointer;
        }
        .empty {
            border: 1px solid transparent;
            background-color: #f0f0f0;
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
        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            z-index: 1000;
        }
        .popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            display: none;
            z-index: 1001;
        }
        .popup .close {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            font-size: 1.2em;
        }
        """ + "\n".join(css_rules) + """
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
                    htmlfile.write("<div class='element' style='background-color: #f0f0f0;'></div>")
        
        # Přidání lanthanoidů na první řádek pod tabulkou
        htmlfile.write("</div><div class='lanthanoids'>")
        for element in lanthanoids:
            element_class = element_classes.get(element['symbol'], "unknown")
            htmlfile.write(
                f"<div class='element {element_class}' onclick=\"showPopup('{element['symbol']}', '{element['name']}', {element['atomic_number']}, '{element['group']}', '{element['period']}', {element['atomic_weight']}, '{element['state']}')\">"
                f"<div class='atomic-number'>{element['atomic_number']}</div>"
                f"<div class='symbol'>{element['symbol']}</div>"
                f"<div class='name'>{element['name']}</div>"
                f"<div class='atomic-weight'>{element['atomic_weight']}</div>"
                f"</div>"
            )
        htmlfile.write("</div>")

        # Přidání aktinoidů na druhý řádek pod tabulkou
        htmlfile.write("<div class='actinoids'>")
        for element in actinoids:
            element_class = element_classes.get(element['symbol'], "unknown")
            htmlfile.write(
                f"<div class='element {element_class}' onclick=\"showPopup('{element['symbol']}', '{element['name']}', {element['atomic_number']}, '{element['group']}', '{element['period']}', {element['atomic_weight']}, '{element['state']}')\">"
                f"<div class='atomic-number'>{element['atomic_number']}</div>"
                f"<div class='symbol'>{element['symbol']}</div>"
                f"<div class='name'>{element['name']}</div>"
                f"<div class='atomic-weight'>{element['atomic_weight']}</div>"
                f"</div>"
            )
        htmlfile.write("</div>")
        
        htmlfile.write("""
        <script>
        function showPopup(symbol, name, atomicNumber, group, period, atomicWeight, state) {
            const popup = document.getElementById('popup');
            const overlay = document.getElementById('overlay');
            const content = document.getElementById('popup-content');
            content.innerHTML = `
                <h2>${name} (${symbol})</h2>
                <p><strong>Atomic Number:</strong> ${atomicNumber}</p>
                <p><strong>Group:</strong> ${group}</p>
                <p><strong>Period:</strong> ${period}</p>
                <p><strong>Atomic Weight:</strong> ${atomicWeight}</p>
                <p><strong>State:</strong> ${state}</p>
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

    print(f"Periodická tabulka s lanthanoidy a aktinoidy byla vygenerována a uložena jako {filename}.")