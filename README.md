# Naše Chemická Romance

## Cíl projektu
Vytvořit konzolovou aplikaci v jazyce Python, která umožní uživatelům interagovat s databází chemických prvků.

## Vstupy
- **CSV soubor** s názvem `elements.csv`, který obsahuje seznam chemických prvků a sadu vlastností (značka, latinský název, anglický název, protonové číslo, skupina, perioda, relativní atomová hmotnost atd.).
- **JSON soubor** s názvem `groups.json`, který obsahuje informace o skupinách chemických prvků.

## Možné výstupy
- **HTML soubor** s periodickou tabulkou chemických prvků.
- **JSON soubor** s informacemi o vybraných chemických prvcích.
- **Markdown soubor** s přehledem některých vlastností prvků.

## Funkcionalita programu
- Načítání dat z CSV souboru do vhodné datové struktury v Pythonu.
- Opakovaný výběr z různých předvoleb - symbolické menu v rámci konzolové aplikace.
- Možnost vyhledávání prvku podle různých kritérií (např. značka, název, protonové číslo, skupina, perioda).
- Zobrazení všech vlastností vybraného prvku.
- Výpočet průměrné relativní atomové hmotnosti prvků ve vybrané skupině nebo periodě.
- Generování HTML tabulky se seznamem všech prvků a jejich základními vlastnostmi.
- Export vybraných dat do XML souboru.
- Vytvoření Markdown souboru s přehledem prvků v konkrétní skupině nebo periodě.

## Požadavky na kód
- Použití funkcí pro modularitu kódu.
- Správné využití strukturovaných datových typů: list, dictionary, tuple, set.
- Práce s řetězci a formátování výstupů.
- Ošetření možných chyb při vstupu od uživatele.
- Komentáře a dokumentace kódu.
