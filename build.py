# -*- coding: utf-8 -*-
"""
Grizzly Barber Shop — static multi-location site generator (feature-rich).
Edit the data below, then run:  python3 build.py
Preview:  python3 -m http.server 8790
"""
import json, os, re, glob, html, unicodedata
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
VER = "14"  # cache-bust; bump after CSS/JS changes

BOOKSY_MAIN = "https://booksy.com/pl-pl/115246_grizzly-barber-shop_barber-shop_18078_szczecin"
INSTAGRAM   = "https://www.instagram.com/grizzly_gorkiego_/"
WHATSAPP    = "https://wa.me/48536338445"

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
LOCATIONS = [
    {
        "slug": "piastow", "short": "Piastów", "name": "Grizzly Barber Shop — Piastów",
        "flagship": True,
        "address": "aleja Piastów 10/1, 70-331 Szczecin", "maps": "aleja Piastów 10, Szczecin",
        "lat": 53.4293, "lng": 14.5510, "open": [10, 20],
        "rating": "4.9", "reviews": "1303",
        "book_type": "booksy", "book_url": BOOKSY_MAIN, "phone": "",
        "hours": "Pon–Niedz · 10:00 – 20:00",
        "staff": [("Olka","Junior Barber"),("Matvij","Barber"),("Julia Blond","Barber"),("Aliona","Barber")],
        "services": [
            ("Strzyżenie (mycie + masaż + stylizacja)", "100 zł", "1 g"),
            ("COMBO — strzyżenie + broda brzytwą", "150 zł", "1 g 30 min"),
            ("Strzyżenie", "80 zł", "1 g 30 min"),
            ("Broda", "70–90 zł", "40–50 min"),
            ("Głowa na łyso + broda", "100–120 zł", "1 g 10 min"),
            ("COVER — koloryzacja / kamuflaż", "60–70 zł", "30 min"),
            ("Strzyżenie długich włosów (15 cm+)", "120 zł", "1 g 10 min"),
            ("Rozjaśnianie", "od 200 zł", "2 g"),
        ],
    },
    {
        "slug": "niebuszewo", "short": "Niebuszewo", "name": "Grizzly Barber Shop — Niebuszewo",
        "flagship": False,
        "address": "Księcia Warcisława I 27b, 71-667 Szczecin", "maps": "Księcia Warcisława I 27b, Szczecin",
        "lat": 53.4525, "lng": 14.5470, "open": [10, 20],
        "rating": "5.0", "reviews": "655",
        "book_type": "booksy", "book_url": "https://booksy.com/pl-pl/220732_grizzly-barber-shop-niebuszewo_barber-shop_18078_szczecin", "phone": "",
        "hours": "Pon–Niedz · 10:00 – 20:00",
        "staff": [("Magda","Barber"),("Julia","Barber"),("Danil","Barber"),("Damian Bonson","Barber"),("Michał","Barber")],
        "services": [
            ("Grizzly Cut — strzyżenie męskie", "80–90 zł", "50 min – 1 g 20 min"),
            ("Broda Bestii — stylizacja brody", "70–80 zł", "40 min – 1 g"),
            ("Full Grizzly — strzyżenie + broda", "130–140 zł", "1 g 10 min – 1 g 50 min"),
            ("Łysa Moc — na łyso + broda", "120 zł", "1 g – 1 g 30 min"),
            ("Maska Niedźwiedzia — kamuflaż brody", "70 zł", "30 min"),
            ("Grizzly Total Look — pełne combo", "200 zł", "1 g 40 min – 2 g 15 min"),
            ("HOT WAX — depilacja woskiem", "30 zł", "15–20 min"),
            ("Kompleksowa pielęgnacja twarzy", "50 zł", "30 min"),
            ("Strzyżenie długich włosów", "120 zł", "1 g"),
        ],
    },
    {
        "slug": "mickiewicza", "short": "Mickiewicza", "name": "Grizzly Barbershop — Mickiewicza",
        "flagship": False,
        "address": "Adama Mickiewicza 36A, 70-385 Szczecin", "maps": "Adama Mickiewicza 36A, Szczecin",
        "lat": 53.4232, "lng": 14.5460, "open": [10, 20],
        "rating": "4.9", "reviews": "407",
        "book_type": "booksy", "book_url": "https://booksy.com/pl-pl/263864_grizzly-barbershop-mickiewicza_barber-shop_18078_szczecin", "phone": "",
        "hours": "Pon–Niedz · 10:00 – 20:00",
        "staff": [("Anton","Senior Barber"),("Julia","Barber"),("Dimas","Barber"),("Ira","Junior Barber"),("Dima","Junior Barber")],
        "services": [
            ("Grizzly Cut — strzyżenie", "90–100 zł", "45–60 min"),
            ("Broda Bestii — stylizacja brody", "80–90 zł", "45–50 min"),
            ("Łysa Moc — na łyso + broda", "120–130 zł", "1 g 10 min"),
            ("Full Grizzly — strzyżenie + broda", "140–150 zł", "1 g – 1 g 30 min"),
            ("Maska Niedźwiedzia — kamuflaż brody", "70 zł", "30 min"),
            ("Strzyżenie Junior", "60 zł", "1 g"),
            ("COMBO Junior — strzyżenie + broda", "110 zł", "1 g 30 min"),
        ],
    },
    {
        "slug": "gorkiego", "short": "Gorkiego", "name": "Grizzly Barber Shop — Gorkiego",
        "flagship": False,
        "address": "Maksyma Gorkiego 5, 70-390 Szczecin", "maps": "Maksyma Gorkiego 5, Szczecin",
        "lat": 53.4468, "lng": 14.5250, "open": [11, 19],
        "rating": "", "reviews": "",
        "book_type": "phone", "book_url": "tel:+48536338445", "phone": "+48 536 338 445",
        "hours": "Pon–Niedz · 11:00 – 19:00",
        "staff": [],
        "services": [
            ("Grizzly Cut — strzyżenie męskie", "od 90 zł", "≈ 1 g"),
            ("Broda Bestii — stylizacja brody", "od 80 zł", "≈ 45 min"),
            ("Full Grizzly — strzyżenie + broda", "od 140 zł", "≈ 1 g 30 min"),
            ("Łysa Moc — na łyso + broda", "od 120 zł", "≈ 1 g"),
            ("HOT WAX — depilacja woskiem", "od 30 zł", "15–20 min"),
            ("Koloryzacja / cover", "od 70 zł", "30 min"),
        ],
    },
]
_total_reviews = sum(int(l["reviews"]) for l in LOCATIONS if l["reviews"])

REVIEWS = [
    ("Najlepszy barber w Szczecinie. Zawsze wychodzę zadowolony, chłopaki znają się na robocie.", "Kamil", "Piastów"),
    ("Broda wymodelowana idealnie, gorący ręcznik, kawa i luźna atmosfera. Polecam.", "Marek", "Niebuszewo"),
    ("Precyzja i konkret. Combo strzyżenie + broda za każdym razem na medal.", "Tomek", "Mickiewicza"),
    ("Umówiłem się przez telefon, obsłużyli szybko i profesjonalnie. Wrócę na pewno.", "Paweł", "Gorkiego"),
    ("Klimat prawdziwego barbera. Widać, że robią to z pasją.", "Bartek", "Piastów"),
]

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def esc(s): return html.escape(str(s), quote=True)
def price_num(p):
    m = re.search(r"\d+", p.replace(" ", "")); return int(m.group()) if m else 0
def mins(tm):
    seg = re.split(r"[–-]", tm.replace("≈", "").strip())[0]
    total = 0
    h = re.search(r"(\d+)\s*g", seg); mm = re.search(r"(\d+)\s*min", seg)
    if h: total += int(h.group(1)) * 60
    if mm: total += int(mm.group(1))
    if total == 0:
        n = re.search(r"\d+", seg)
        if n: total = int(n.group())
    return total
def fmt_dur(m):
    h, mm = divmod(m, 60)
    if h and mm: return f"{h} g {mm} min"
    if h: return f"{h} g"
    return f"{mm} min"
def maps_embed(q): return f"https://www.google.com/maps?q={quote(q)}&output=embed"
def maps_link(q):  return f"https://www.google.com/maps/search/?api=1&query={quote(q)}"

def t(key): return f'<span data-i18n="{key}">{esc(I18N["pl"][key])}</span>'
def ta(key): return esc(I18N["pl"][key])  # plain PL text (for attributes / default)

def emblem(rel="", cls=""):
    c = (" " + cls) if cls else ""
    return f'<img class="emb{c}" src="{rel}assets/emblem.png" alt="Grizzly Barber Shop">'

def nslug(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def team_photo(slug, name):
    rel = f"assets/team/{slug}__{nslug(name)}.jpg"
    return rel if os.path.exists(os.path.join(HERE, rel)) else None

def bslug(slug, name):
    return f"{slug}-{nslug(name)}"

def tm_card(slug, name, role):
    ph = team_photo(slug, name)
    ava = (f'<div class="tm-ava has-photo"><img loading="lazy" src="{ph}" alt="{esc(name)}"></div>'
           if ph else f'<div class="tm-ava">{emblem()}</div>')
    return (f'<a class="tm-card reveal" href="barber-{bslug(slug, name)}.html">{ava}'
            f'<h4>{esc(name)}</h4><span>{esc(role)}</span><span class="tm-go">{t("view_loc")} →</span></a>')

PAW = ('<svg class="paw" viewBox="0 0 100 100" aria-hidden="true">'
       '<ellipse cx="50" cy="64" rx="24" ry="20"/>'
       '<ellipse cx="24" cy="44" rx="8" ry="11"/>'
       '<ellipse cx="41" cy="32" rx="8.5" ry="12.5"/>'
       '<ellipse cx="59" cy="32" rx="8.5" ry="12.5"/>'
       '<ellipse cx="76" cy="44" rx="8" ry="11"/></svg>')

# ---------------------------------------------------------------------------
# i18n
# ---------------------------------------------------------------------------
I18N = {
 "pl": {
  "nav_lokale":"Lokale","nav_barberzy":"Barberzy","nav_uslugi":"Cennik","nav_kalk":"Kalkulator","nav_onas":"O nas",
  "barberzy_title":"Barberzy","barberzy_sub":"Nasza ekipa w każdym lokalu — poznaj się przed wizytą.",
  "feat_online":"Rezerwacja online","feat_card":"Płatność kartą","feat_wifi":"Wi-Fi","feat_access":"Dostęp dla wózków","feat_pets":"Zwierzaki mile widziane","feat_kids":"Przyjazny dzieciom",
  "nav_konstr":"Konstruktor","konstr_title":"Konstruktor fryzury","konstr_sub":"Przymierz fryzurę i kolor na żywo w kamerze — potem zarezerwuj w Grizzly.",
  "konstr_look":"Twój look","konstr_serv":"Proponowane usługi","konstr_from":"Orientacyjnie od",
  "nav_bony":"Bony","gift_title":"Bony podarunkowe","gift_text":"Zrób prezent w grizzly stylu — bon podarunkowy na dowolną usługę lub kwotę. Kup online przez Booksy albo zapytaj w dowolnym lokalu.","gift_cta":"Kup bon na Booksy",
  "nav_opinie":"Opinie","nav_galeria":"Galeria","nav_faq":"FAQ","nav_kontakt":"Kontakt","btn_book":"Rezerwuj",
  "promo_text":"Rezerwuj online w 4 lokalach Grizzly — Piastów · Niebuszewo · Mickiewicza · Gorkiego.","promo_cta":"Rezerwuj",
  "hero_kicker":"Szczecin · 4 lokale","hero_title":"GRIZZLY BARBER SHOP",
  "hero_sub":"Męski fach, niedźwiedzia moc. Cztery lokale w Szczecinie — jedno rzemiosło.",
  "hero_cta1":"Rezerwuj wizytę","hero_cta2":"Znajdź najbliższy lokal",
  "hero_stat_r":"średnia ocena","hero_stat_v":"opinii","hero_stat_l":"lokale",
  "lokale_title":"Nasze lokale","lokale_sub":"Wybierz najbliższy Grizzly w Szczecinie.",
  "finder_btn":"Znajdź najbliższy lokal","finder_wait":"Ustalam lokalizację…","finder_deny":"Nie udało się ustalić lokalizacji — wybierz lokal ręcznie.",
  "finder_res":"Najbliżej jesteś:","km":"km",
  "uslugi_title":"Cennik","uslugi_sub":"Ceny różnią się między lokalami — wybierz zakładkę.",
  "kalk_title":"Kalkulator wizyty","kalk_sub":"Zaznacz usługi i policz orientacyjny koszt oraz czas.",
  "kalk_pick":"Wybierz lokal","kalk_total":"Razem","kalk_time":"Czas","kalk_book":"Rezerwuj w tym lokalu","kalk_empty":"Zaznacz usługi powyżej.",
  "onas_title":"O nas",
  "onas_p1":"Grizzly Barber Shop to męski barber z charakterem — założony w Szczecinie przez Antona Fomicha. Zaczęło się od jednego fotela, dziś to cztery lokale i jedno rzemiosło.",
  "onas_p2":"Ostre nożyczki, gorący ręcznik, brzytwa i zero pośpiechu. Wchodzisz jak człowiek, wychodzisz jak niedźwiedź.",
  "onas_v1t":"Rzemiosło","onas_v1d":"Każde strzyżenie dopięte na ostatni włos.",
  "onas_v2t":"Atmosfera","onas_v2d":"Wi-Fi, kawa, karta, zwierzaki i dzieciaki mile widziane.",
  "onas_v3t":"Cztery lokale","onas_v3d":"Ten sam standard w całym Szczecinie.",
  "opinie_title":"Opinie","opinie_sub":"Ponad 2300 opinii ze wszystkich lokali.",
  "galeria_title":"Galeria","galeria_empty":"Zdjęcia realizacji zobaczysz na naszym Booksy i Instagramie.",
  "ba_title":"Efekt przed / po","ba_hint":"Przeciągnij suwak","ba_note":"Wizualizacja poglądowa.",
  "faq_title":"Częste pytania",
  "faq0q":"Czy trzeba się umawiać?","faq0a":"Najlepiej zarezerwuj online przez Booksy. Z wolnej ręki przyjmujemy w miarę dostępności.",
  "faq1q":"Jak mogę zapłacić?","faq1a":"Gotówką i kartą — w każdym lokalu.",
  "faq2q":"Ile trwa wizyta?","faq2a":"Strzyżenie ok. 45–60 min, combo strzyżenie + broda do 1,5 godziny.",
  "faq3q":"Mogę przyjść z dzieckiem lub zwierzakiem?","faq3a":"Tak — dzieci i zwierzaki są mile widziane.",
  "faq4q":"Czy mogę kupić bon podarunkowy?","faq4a":"Tak — bon na dowolną usługę lub kwotę kupisz przez Booksy albo w każdym z naszych lokali.",
  "kontakt_title":"Kontakt","kontakt_sub":"Wszystkie lokale Grizzly w jednym miejscu.",
  "staff_label":"Zespół","hours_label":"Godziny","addr_label":"Adres","phone_label":"Telefon",
  "book_phone":"Zadzwoń i umów","book_booksy":"Rezerwuj online","view_loc":"Zobacz lokal",
  "reviews_word":"opinii","back_all":"Wszystkie lokale","open_now":"Otwarte teraz","closed_now":"Zamknięte",
  "svc_service":"Usługa","svc_price":"Cena","svc_time":"Czas","loc_menu_title":"Cennik","loc_team_title":"Barberzy",
  "modal_title":"Gdzie chcesz się umówić?","modal_sub":"Wybierz lokal — przekierujemy Cię do rezerwacji.",
  "map_label":"Mapa","new_loc":"Nowy lokal",
  "footer_tag":"Męski fach, niedźwiedzia moc.","footer_rights":"Wszystkie prawa zastrzeżone.",
 },
 "uk": {
  "nav_lokale":"Локації","nav_barberzy":"Барбери","nav_uslugi":"Прайс","nav_kalk":"Калькулятор","nav_onas":"Про нас",
  "barberzy_title":"Барбери","barberzy_sub":"Наша команда в кожній локації — знайомся перед візитом.",
  "feat_online":"Онлайн-запис","feat_card":"Оплата карткою","feat_wifi":"Wi-Fi","feat_access":"Доступ для візків","feat_pets":"Тварини вітаються","feat_kids":"Дружній до дітей",
  "nav_konstr":"Конструктор","konstr_title":"Конструктор зачіски","konstr_sub":"Приміряй зачіску і колір у камері — потім запишись у Grizzly.",
  "konstr_look":"Твій образ","konstr_serv":"Пропоновані послуги","konstr_from":"Орієнтовно від",
  "nav_bony":"Сертифікати","gift_title":"Подарункові сертифікати","gift_text":"Зроби подарунок у grizzly-стилі — сертифікат на будь-яку послугу чи суму. Купуй онлайн через Booksy або запитай у будь-якій локації.","gift_cta":"Купити на Booksy",
  "nav_opinie":"Відгуки","nav_galeria":"Галерея","nav_faq":"FAQ","nav_kontakt":"Контакти","btn_book":"Записатись",
  "promo_text":"Записуйся онлайн у 4 локаціях Grizzly — Piastów · Niebuszewo · Mickiewicza · Gorkiego.","promo_cta":"Записатись",
  "hero_kicker":"Щецин · 4 локації","hero_title":"GRIZZLY BARBER SHOP",
  "hero_sub":"Чоловіче ремесло, ведмежа сила. Чотири локації в Щеціні — одна майстерність.",
  "hero_cta1":"Записатись","hero_cta2":"Знайти найближчу локацію",
  "hero_stat_r":"середня оцінка","hero_stat_v":"відгуків","hero_stat_l":"локації",
  "lokale_title":"Наші локації","lokale_sub":"Обери найближчий Grizzly у Щеціні.",
  "finder_btn":"Знайти найближчу локацію","finder_wait":"Визначаю місце…","finder_deny":"Не вдалося визначити місце — обери локацію вручну.",
  "finder_res":"Найближче до тебе:","km":"км",
  "uslugi_title":"Прайс","uslugi_sub":"Ціни різняться між локаціями — обери вкладку.",
  "kalk_title":"Калькулятор візиту","kalk_sub":"Познач послуги й порахуй орієнтовну вартість і час.",
  "kalk_pick":"Обери локацію","kalk_total":"Разом","kalk_time":"Час","kalk_book":"Записатись у цю локацію","kalk_empty":"Познач послуги вище.",
  "onas_title":"Про нас",
  "onas_p1":"Grizzly Barber Shop — це чоловічий барбершоп з характером, заснований у Щеціні Антоном Фомічем. Почалося з одного крісла, сьогодні це чотири локації та одне ремесло.",
  "onas_p2":"Гострі ножиці, гарячий рушник, небезпечна бритва і жодного поспіху. Заходиш людиною — виходиш ведмедем.",
  "onas_v1t":"Ремесло","onas_v1d":"Кожна стрижка вивірена до останньої волосини.",
  "onas_v2t":"Атмосфера","onas_v2d":"Wi-Fi, кава, картка, тварини і діти вітаються.",
  "onas_v3t":"Чотири локації","onas_v3d":"Той самий стандарт по всьому Щеціну.",
  "opinie_title":"Відгуки","opinie_sub":"Понад 2300 відгуків з усіх локацій.",
  "galeria_title":"Галерея","galeria_empty":"Фото робіт дивись на нашому Booksy та в Instagram.",
  "ba_title":"Ефект до / після","ba_hint":"Потягни повзунок","ba_note":"Ілюстрація для наочності.",
  "faq_title":"Часті запитання",
  "faq0q":"Чи треба записуватись?","faq0a":"Найкраще записатись онлайн через Booksy. Без запису приймаємо за наявності місця.",
  "faq1q":"Як можна оплатити?","faq1a":"Готівкою і карткою — у кожній локації.",
  "faq2q":"Скільки триває візит?","faq2a":"Стрижка бл. 45–60 хв, комбо стрижка + борода до 1,5 години.",
  "faq3q":"Можна прийти з дитиною чи твариною?","faq3a":"Так — діти і тварини вітаються.",
  "faq4q":"Чи можна купити подарунковий сертифікат?","faq4a":"Так — сертифікат на будь-яку послугу чи суму купиш через Booksy або в будь-якій нашій локації.",
  "kontakt_title":"Контакти","kontakt_sub":"Усі локації Grizzly в одному місці.",
  "staff_label":"Команда","hours_label":"Години","addr_label":"Адреса","phone_label":"Телефон",
  "book_phone":"Зателефонувати","book_booksy":"Записатись онлайн","view_loc":"Дивитись локацію",
  "reviews_word":"відгуків","back_all":"Усі локації","open_now":"Зараз відкрито","closed_now":"Зачинено",
  "svc_service":"Послуга","svc_price":"Ціна","svc_time":"Час","loc_menu_title":"Прайс","loc_team_title":"Барбери",
  "modal_title":"Де хочеш записатись?","modal_sub":"Обери локацію — перекинемо тебе на бронювання.",
  "map_label":"Карта","new_loc":"Нова локація",
  "footer_tag":"Чоловіче ремесло, ведмежа сила.","footer_rights":"Усі права захищені.",
 },
 "ru": {
  "nav_lokale":"Локации","nav_barberzy":"Барберы","nav_uslugi":"Прайс","nav_kalk":"Калькулятор","nav_onas":"О нас",
  "barberzy_title":"Барберы","barberzy_sub":"Наша команда в каждой локации — знакомься перед визитом.",
  "feat_online":"Онлайн-запись","feat_card":"Оплата картой","feat_wifi":"Wi-Fi","feat_access":"Доступ для колясок","feat_pets":"Животные welcome","feat_kids":"Можно с детьми",
  "nav_konstr":"Конструктор","konstr_title":"Конструктор причёски","konstr_sub":"Примерь причёску и цвет в камере — потом запишись в Grizzly.",
  "konstr_look":"Твой образ","konstr_serv":"Рекомендуемые услуги","konstr_from":"Ориентировочно от",
  "nav_bony":"Сертификаты","gift_title":"Подарочные сертификаты","gift_text":"Сделай подарок в grizzly-стиле — сертификат на любую услугу или сумму. Купи онлайн через Booksy или спроси в любой локации.","gift_cta":"Купить на Booksy",
  "nav_opinie":"Отзывы","nav_galeria":"Галерея","nav_faq":"FAQ","nav_kontakt":"Контакты","btn_book":"Записаться",
  "promo_text":"Записывайся онлайн в 4 локациях Grizzly — Piastów · Niebuszewo · Mickiewicza · Gorkiego.","promo_cta":"Записаться",
  "hero_kicker":"Щецин · 4 локации","hero_title":"GRIZZLY BARBER SHOP",
  "hero_sub":"Мужское ремесло, медвежья сила. Четыре локации в Щецине — одно мастерство.",
  "hero_cta1":"Записаться","hero_cta2":"Найти ближайшую локацию",
  "hero_stat_r":"средняя оценка","hero_stat_v":"отзывов","hero_stat_l":"локации",
  "lokale_title":"Наши локации","lokale_sub":"Выбери ближайший Grizzly в Щецине.",
  "finder_btn":"Найти ближайшую локацию","finder_wait":"Определяю местоположение…","finder_deny":"Не удалось определить местоположение — выбери локацию вручную.",
  "finder_res":"Ближе всего к тебе:","km":"км",
  "uslugi_title":"Прайс","uslugi_sub":"Цены отличаются по локациям — выбери вкладку.",
  "kalk_title":"Калькулятор визита","kalk_sub":"Отметь услуги и посчитай примерную стоимость и время.",
  "kalk_pick":"Выбери локацию","kalk_total":"Итого","kalk_time":"Время","kalk_book":"Записаться в эту локацию","kalk_empty":"Отметь услуги выше.",
  "onas_title":"О нас",
  "onas_p1":"Grizzly Barber Shop — мужской барбершоп с характером, основанный в Щецине Антоном Фомичем. Началось с одного кресла, сегодня это четыре локации и одно ремесло.",
  "onas_p2":"Острые ножницы, горячее полотенце, опасная бритва и ноль спешки. Заходишь человеком — выходишь медведем.",
  "onas_v1t":"Ремесло","onas_v1d":"Каждая стрижка выверена до последнего волоса.",
  "onas_v2t":"Атмосфера","onas_v2d":"Wi-Fi, кофе, карта, животные и дети — welcome.",
  "onas_v3t":"Четыре локации","onas_v3d":"Один стандарт по всему Щецину.",
  "opinie_title":"Отзывы","opinie_sub":"Более 2300 отзывов со всех локаций.",
  "galeria_title":"Галерея","galeria_empty":"Фото работ смотри на нашем Booksy и в Instagram.",
  "ba_title":"Эффект до / после","ba_hint":"Потяни ползунок","ba_note":"Иллюстрация для наглядности.",
  "faq_title":"Частые вопросы",
  "faq0q":"Нужно ли записываться?","faq0a":"Лучше записаться онлайн через Booksy. Без записи принимаем при наличии места.",
  "faq1q":"Как можно оплатить?","faq1a":"Наличными и картой — в каждой локации.",
  "faq2q":"Сколько длится визит?","faq2a":"Стрижка около 45–60 мин, комбо стрижка + борода до 1,5 часа.",
  "faq3q":"Можно прийти с ребёнком или животным?","faq3a":"Да — дети и животные welcome.",
  "faq4q":"Можно купить подарочный сертификат?","faq4a":"Да — сертификат на любую услугу или сумму купишь через Booksy или в любой нашей локации.",
  "kontakt_title":"Контакты","kontakt_sub":"Все локации Grizzly в одном месте.",
  "staff_label":"Команда","hours_label":"Часы","addr_label":"Адрес","phone_label":"Телефон",
  "book_phone":"Позвонить и записаться","book_booksy":"Записаться онлайн","view_loc":"Смотреть локацию",
  "reviews_word":"отзывов","back_all":"Все локации","open_now":"Сейчас открыто","closed_now":"Закрыто",
  "svc_service":"Услуга","svc_price":"Цена","svc_time":"Время","loc_menu_title":"Прайс","loc_team_title":"Барберы",
  "modal_title":"Где хочешь записаться?","modal_sub":"Выбери локацию — отправим тебя на бронь.",
  "map_label":"Карта","new_loc":"Новая локация",
  "footer_tag":"Мужское ремесло, медвежья сила.","footer_rights":"Все права защищены.",
 },
 "en": {
  "nav_lokale":"Locations","nav_barberzy":"Barbers","nav_uslugi":"Prices","nav_kalk":"Calculator","nav_onas":"About",
  "barberzy_title":"Barbers","barberzy_sub":"Our crew at every shop — meet them before your visit.",
  "feat_online":"Online booking","feat_card":"Card payment","feat_wifi":"Wi-Fi","feat_access":"Wheelchair access","feat_pets":"Pets welcome","feat_kids":"Kid-friendly",
  "nav_konstr":"Style builder","konstr_title":"Style builder","konstr_sub":"Try a hairstyle and color live on camera — then book at Grizzly.",
  "konstr_look":"Your look","konstr_serv":"Suggested services","konstr_from":"Approx. from",
  "nav_bony":"Gift cards","gift_title":"Gift cards","gift_text":"Give a gift the grizzly way — a gift card for any service or amount. Buy online on Booksy or ask at any shop.","gift_cta":"Buy on Booksy",
  "nav_opinie":"Reviews","nav_galeria":"Gallery","nav_faq":"FAQ","nav_kontakt":"Contact","btn_book":"Book now",
  "promo_text":"Book online at all 4 Grizzly shops — Piastów · Niebuszewo · Mickiewicza · Gorkiego.","promo_cta":"Book now",
  "hero_kicker":"Szczecin · 4 shops","hero_title":"GRIZZLY BARBER SHOP",
  "hero_sub":"A man's craft with a bear's strength. Four shops in Szczecin — one trade.",
  "hero_cta1":"Book a visit","hero_cta2":"Find the nearest shop",
  "hero_stat_r":"avg rating","hero_stat_v":"reviews","hero_stat_l":"shops",
  "lokale_title":"Our shops","lokale_sub":"Pick the nearest Grizzly in Szczecin.",
  "finder_btn":"Find the nearest shop","finder_wait":"Locating you…","finder_deny":"Couldn't get your location — pick a shop manually.",
  "finder_res":"Closest to you:","km":"km",
  "uslugi_title":"Prices","uslugi_sub":"Prices vary by shop — pick a tab.",
  "kalk_title":"Visit calculator","kalk_sub":"Tick services to estimate the cost and time.",
  "kalk_pick":"Pick a shop","kalk_total":"Total","kalk_time":"Time","kalk_book":"Book at this shop","kalk_empty":"Tick services above.",
  "onas_title":"About us",
  "onas_p1":"Grizzly Barber Shop is a men's barber with character, founded in Szczecin by Anton Fomich. It started with a single chair — today it's four shops and one trade.",
  "onas_p2":"Sharp scissors, a hot towel, a straight razor and zero rush. Walk in a man, walk out a bear.",
  "onas_v1t":"Craft","onas_v1d":"Every cut dialed in to the last hair.",
  "onas_v2t":"Atmosphere","onas_v2d":"Wi-Fi, coffee, card, pets and kids welcome.",
  "onas_v3t":"Four shops","onas_v3d":"The same standard across Szczecin.",
  "opinie_title":"Reviews","opinie_sub":"Over 2,300 reviews across all shops.",
  "galeria_title":"Gallery","galeria_empty":"See our work on Booksy and Instagram.",
  "ba_title":"Before / after","ba_hint":"Drag the slider","ba_note":"Illustrative visual.",
  "faq_title":"FAQ",
  "faq0q":"Do I need an appointment?","faq0a":"Best to book online via Booksy. Walk-ins are taken subject to availability.",
  "faq1q":"How can I pay?","faq1a":"Cash and card — at every shop.",
  "faq2q":"How long does a visit take?","faq2a":"A cut is about 45–60 min, a cut + beard combo up to 1.5 hours.",
  "faq3q":"Can I come with a kid or a pet?","faq3a":"Yes — kids and pets are welcome.",
  "faq4q":"Can I buy a gift card?","faq4a":"Yes — a gift card for any service or amount is available on Booksy or at any of our shops.",
  "kontakt_title":"Contact","kontakt_sub":"Every Grizzly shop in one place.",
  "staff_label":"Team","hours_label":"Hours","addr_label":"Address","phone_label":"Phone",
  "book_phone":"Call to book","book_booksy":"Book online","view_loc":"View shop",
  "reviews_word":"reviews","back_all":"All shops","open_now":"Open now","closed_now":"Closed",
  "svc_service":"Service","svc_price":"Price","svc_time":"Time","loc_menu_title":"Price list","loc_team_title":"Barbers",
  "modal_title":"Where do you want to book?","modal_sub":"Pick a shop — we'll send you to booking.",
  "map_label":"Map","new_loc":"New shop",
  "footer_tag":"A man's craft, a bear's strength.","footer_rights":"All rights reserved.",
 },
}

# ---------------------------------------------------------------------------
# JS data blob
# ---------------------------------------------------------------------------
def js_data():
    locs = []
    for l in LOCATIONS:
        locs.append({
            "slug": l["slug"], "short": l["short"], "name": l["name"],
            "address": l["address"], "book_type": l["book_type"], "book_url": l["book_url"],
            "phone": l["phone"], "lat": l["lat"], "lng": l["lng"], "open": l["open"],
            "rating": l["rating"], "reviews": l["reviews"], "flagship": l["flagship"],
            "services": [{"name": n, "price": p, "time": tm, "num": price_num(p), "min": mins(tm)}
                         for (n, p, tm) in l["services"]],
        })
    return {"booksy": BOOKSY_MAIN, "ig": INSTAGRAM, "locs": locs}

# ---------------------------------------------------------------------------
# partials
# ---------------------------------------------------------------------------
def head(title, rel=""):
    return f"""<!DOCTYPE html>
<html lang="pl" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="Grizzly Barber Shop — męski barbershop w Szczecinie. 4 lokale: Piastów, Niebuszewo, Mickiewicza, Gorkiego. Rezerwacja online.">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="Męski barbershop w Szczecinie — 4 lokale, jedno rzemiosło.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}styles.css?v={VER}">
<link rel="icon" href="{rel}assets/favicon.png?v={VER}">
</head>
<body>
<script>var r=document.documentElement;r.classList.remove('no-js');r.classList.add('js');try{{var th=localStorage.getItem('grz_theme');if(th)r.setAttribute('data-theme',th);}}catch(e){{}}</script>
<div id="progress"></div>
"""

def _nav_links(rel, keys):
    return "".join(f'<a href="{rel}index.html#{sec}">{t(key)}</a>' for sec, key in keys)

def header(rel=""):
    top = [("lokale","nav_lokale"),("barberzy","nav_barberzy"),("uslugi","nav_uslugi"),
           ("konstruktor","nav_konstr"),("galeria","nav_galeria"),("kontakt","nav_kontakt")]
    full = [("lokale","nav_lokale"),("barberzy","nav_barberzy"),("uslugi","nav_uslugi"),("kalkulator","nav_kalk"),
            ("konstruktor","nav_konstr"),("opinie","nav_opinie"),("galeria","nav_galeria"),
            ("bony","nav_bony"),("faq","nav_faq"),("kontakt","nav_kontakt")]
    return f"""<header class="site-head">
<div class="wrap head-in">
  <a class="brand" href="{rel}index.html">{emblem(rel)}<span class="brand-word">GRIZZLY</span></a>
  <nav class="nav">{_nav_links(rel, top)}</nav>
  <div class="head-right">
    <button class="theme-btn" id="themeBtn" aria-label="motyw">◐</button>
    <div class="lang" id="lang">
      <button data-l="pl">PL</button><button data-l="uk">UA</button><button data-l="ru">RU</button><button data-l="en">EN</button>
    </div>
    <button class="btn btn-amber head-cta js-book">{t('btn_book')}</button>
    <button class="burger" id="burger" aria-label="menu"><span></span><span></span><span></span></button>
  </div>
</div>
<div class="drawer" id="drawer"><nav>{_nav_links(rel, full)}
  <button class="btn btn-amber js-book">{t('btn_book')}</button>
</nav></div>
</header>"""

def footer(rel=""):
    loc_links = " · ".join(f'<a href="{rel}lokal-{l["slug"]}.html">{esc(l["short"])}</a>' for l in LOCATIONS)
    return f"""<footer class="site-foot">
<div class="wrap foot-in">
  <div>
    <a class="brand" href="{rel}index.html">{emblem(rel)}<span class="brand-word">GRIZZLY</span></a>
    <p class="foot-tag">{t('footer_tag')}</p>
  </div>
  <div class="foot-locs">{loc_links}</div>
  <div class="foot-social">
    <a href="{esc(BOOKSY_MAIN)}" target="_blank" rel="noopener">Booksy</a>
    <a href="{esc(INSTAGRAM)}" target="_blank" rel="noopener">Instagram</a>
    <a href="{esc(WHATSAPP)}" target="_blank" rel="noopener">WhatsApp</a>
  </div>
</div>
<div class="wrap foot-bar">© 2026 Grizzly Barber Shop · Szczecin · <span data-i18n="footer_rights">{ta('footer_rights')}</span></div>
</footer>
{booking_modal()}
<div class="mobar"><button class="btn btn-amber js-book" style="width:100%">{t('btn_book')}</button></div>
<div id="lightbox" class="lightbox"><button class="lb-close" aria-label="close">×</button><button class="lb-prev" aria-label="prev">‹</button><img id="lbImg" alt=""><button class="lb-next" aria-label="next">›</button></div>
<button id="toTop" aria-label="top">↑</button>
<script src="{rel}translations.js?v={VER}"></script>
<script src="{rel}app.js?v={VER}"></script>
<script type="module" src="{rel}ar.js?v={VER}"></script>
</body></html>"""

def booking_modal():
    rows = ""
    for l in LOCATIONS:
        meta = f'{l["rating"]} ★ · {l["reviews"]} ' if l["rating"] else ""
        act = ("book_phone" if l["book_type"] == "phone" else "book_booksy")
        tgt = "" if l["book_type"] == "phone" else 'target="_blank" rel="noopener"'
        rows += f"""<a class="mo-loc" href="{esc(l['book_url'])}" {tgt}>
  <div><b>{esc(l['short'])}</b><span>{esc(l['address'])}</span></div>
  <span class="mo-go">{t(act)} →</span></a>"""
    return f"""<div class="modal" id="bookModal"><div class="modal-card">
  <button class="modal-x" aria-label="close">×</button>
  <h3 data-i18n="modal_title">{ta('modal_title')}</h3>
  <p data-i18n="modal_sub">{ta('modal_sub')}</p>
  <div class="mo-list">{rows}</div>
</div></div>"""

def book_btn(l, big=False, cls_extra=""):
    cls = "btn btn-amber" + (" btn-lg" if big else "") + (f" {cls_extra}" if cls_extra else "")
    if l["book_type"] == "phone":
        return f'<a class="{cls}" href="{esc(l["book_url"])}">{t("book_phone")}</a>'
    return f'<a class="{cls}" href="{esc(l["book_url"])}" target="_blank" rel="noopener">{t("book_booksy")}</a>'

def open_badge(slug):
    return f'<span class="open-badge" data-open="{slug}"></span>'

_FEAT_ICONS = {
 "online": '<rect x="3" y="4.5" width="18" height="16" rx="2"/><path d="M3 9h18M8 2.5v4M16 2.5v4M9 14l2 2 4-4"/>',
 "card": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 9.5h19M6 15h4"/>',
 "wifi": '<path d="M2 8.5a15 15 0 0 1 20 0M5 12a10 10 0 0 1 14 0M8 15.3a5 5 0 0 1 8 0"/><circle cx="12" cy="19" r="1" fill="currentColor" stroke="none"/>',
 "access": '<circle cx="10.5" cy="4" r="1.9"/><path d="M10.5 6.2v5.3h4.2l2.3 5"/><path d="M15 15.8a5 5 0 1 1-5.2-4.3"/>',
 "pets": '<ellipse cx="12" cy="15" rx="4" ry="3.2"/><ellipse cx="6.5" cy="10" rx="1.6" ry="2.1"/><ellipse cx="10" cy="7.5" rx="1.7" ry="2.3"/><ellipse cx="14" cy="7.5" rx="1.7" ry="2.3"/><ellipse cx="17.5" cy="10" rx="1.6" ry="2.1"/>',
 "kids": '<circle cx="12" cy="12" r="9"/><path d="M9 10h.01M15 10h.01M8.5 14.5a4.5 4.5 0 0 0 7 0"/>',
}
def features_strip():
    order = [("online","feat_online"),("card","feat_card"),("wifi","feat_wifi"),
             ("access","feat_access"),("pets","feat_pets"),("kids","feat_kids")]
    items = "".join(
        f'<div class="feat"><svg viewBox="0 0 24 24">{_FEAT_ICONS[ic]}</svg>'
        f'<span data-i18n="{key}">{ta(key)}</span></div>' for ic, key in order)
    return f'<section class="features"><div class="wrap feat-in">{items}</div></section>'

# ---------------------------------------------------------------------------
# INDEX
# ---------------------------------------------------------------------------
def loc_photo(slug):
    p = os.path.join(HERE, "assets", "loc", f"{slug}.jpg")
    return f"assets/loc/{slug}.jpg" if os.path.exists(p) else None

def location_card(l):
    if l["rating"]:
        meta = f'<span class="lc-rate"><span class="stars">★</span> <b>{esc(l["rating"])}</b> · {esc(l["reviews"])} {t("reviews_word")}</span>'
    else:
        meta = f'<span class="lc-rate lc-new">{t("new_loc")}</span>'
    flag = '<span class="lc-flag">★</span>' if l["flagship"] else ""
    ph = loc_photo(l["slug"])
    img = (f'<div class="lc-img" style="background-image:url({ph})"></div>' if ph
           else f'<div class="lc-img emblem">{emblem()}</div>')
    return f"""<a class="loc-card reveal" data-slug="{l['slug']}" href="lokal-{l['slug']}.html">
  {flag}{open_badge(l['slug'])}
  {img}
  <div class="lc-body">
    <h3>{esc(l['short'])}</h3>
    <p class="lc-addr">{esc(l['address'])}</p>
    {meta}
    <span class="lc-dist" data-dist="{l['slug']}"></span>
    <span class="lc-go">{t('view_loc')} →</span>
  </div>
</a>"""

def svc_chip(s):
    n, p, tm = s
    return f'<div class="svc"><div class="svc-name">{esc(n)}</div><div class="svc-meta"><span class="svc-price">{esc(p)}</span><span class="svc-time">{esc(tm)}</span></div></div>'

def build_index():
    cards = "".join(location_card(l) for l in LOCATIONS)
    # masters grouped by location
    masters_blocks = ""
    for l in LOCATIONS:
        if not l["staff"]:
            continue
        tm = "".join(tm_card(l["slug"], nm, role) for (nm, role) in l["staff"])
        masters_blocks += f"""<div class="masters-loc">
  <div class="ml-head reveal">{esc(l['short'])} <a href="lokal-{l['slug']}.html">{t('view_loc')} →</a></div>
  <div class="team-grid">{tm}</div>
</div>"""
    # price tabs
    tabs = "".join(
        f'<button class="tab {"on" if i==0 else ""}" data-tab="{l["slug"]}">{esc(l["short"])}</button>'
        for i, l in enumerate(LOCATIONS))
    panels = "".join(
        f'<div class="tab-panel {"on" if i==0 else ""}" data-panel="{l["slug"]}"><div class="svc-grid">'
        + "".join(svc_chip(s) for s in l["services"]) + "</div></div>"
        for i, l in enumerate(LOCATIONS))
    # reviews
    slides = "".join(
        f'<div class="rev-slide"><p>“{esc(txt)}”</p><div class="rev-by"><b>{esc(who)}</b><span>{esc(loc)}</span></div></div>'
        for (txt, who, loc) in REVIEWS)
    dots = "".join(f'<button class="rev-dot {"on" if i==0 else ""}" data-i="{i}"></button>' for i in range(len(REVIEWS)))
    # faq
    faqs = "".join(
        f'<div class="faq-item"><button class="faq-q">{t(f"faq{i}q")}<span>+</span></button><div class="faq-a"><p>{t(f"faq{i}a")}</p></div></div>'
        for i in range(5))
    # gallery
    imgs = sorted(glob.glob(os.path.join(HERE, "assets", "gallery", "*.jpg")) +
                  glob.glob(os.path.join(HERE, "assets", "gallery", "*.jpeg")) +
                  glob.glob(os.path.join(HERE, "assets", "gallery", "*.png")))
    if imgs:
        gal = '<div class="masonry">' + "".join(
            f'<img class="lb" loading="lazy" src="assets/gallery/{esc(os.path.basename(p))}" alt="Grizzly">'
            for p in imgs) + "</div>"
    else:
        gal = f"""<div class="gallery-empty reveal">
      <p data-i18n="galeria_empty">{ta('galeria_empty')}</p>
      <div class="ge-btns"><a class="btn btn-ghost" href="{esc(BOOKSY_MAIN)}" target="_blank" rel="noopener">Booksy</a>
      <a class="btn btn-ghost" href="{esc(INSTAGRAM)}" target="_blank" rel="noopener">Instagram</a></div>
    </div>"""
    # contact rows
    contact_rows = "".join(
        f"""<div class="ct-row reveal">
  <div><h4>{esc(l['short'])} {open_badge(l['slug'])}</h4><p>{esc(l['address'])}</p>
  <p class="ct-sub">{('☎ '+esc(l['phone'])) if l['phone'] else esc(l['hours'])}</p></div>
  <div class="ct-act">{book_btn(l)}<a class="btn btn-ghost" href="{esc(maps_link(l['maps']))}" target="_blank" rel="noopener">{t('map_label')}</a></div>
</div>""" for l in LOCATIONS)

    body = f"""{header()}
<div class="promo" id="promo"><div class="wrap promo-in">
  <span data-i18n="promo_text">{ta('promo_text')}</span>
  <button class="promo-cta js-book">{t('promo_cta')}</button>
  <button class="promo-x" id="promoX" aria-label="close">×</button>
</div></div>
<main>
<section class="hero">
  <div class="hero-bg" style="background-image:url(assets/hero.jpg)"></div>
  <div class="hero-shade"></div>
  <div class="wrap hero-in">
    <h1 class="sr-only">Grizzly Barber Shop — Szczecin</h1>
    <p class="kicker" data-i18n="hero_kicker">{ta('hero_kicker')}</p>
    <img class="hero-logo" src="assets/emblem.png" alt="Grizzly Barber Shop">
    <p class="hero-est">EST. 2021 · SZCZECIN</p>
    <p class="hero-sub" data-i18n="hero_sub">{ta('hero_sub')}</p>
    <div class="hero-cta">
      <button class="btn btn-amber btn-lg js-book" data-i18n="hero_cta1">{ta('hero_cta1')}</button>
      <button class="btn btn-ghost btn-lg" id="finderBtn" data-i18n="hero_cta2">{ta('hero_cta2')}</button>
    </div>
    <p class="finder-msg" id="finderMsg"></p>
    <div class="hero-stats">
      <div><b>4.9</b><span data-i18n="hero_stat_r">{ta('hero_stat_r')}</span></div>
      <div><b data-count="{_total_reviews}">0</b><span data-i18n="hero_stat_v">{ta('hero_stat_v')}</span></div>
      <div><b data-count="4">0</b><span data-i18n="hero_stat_l">{ta('hero_stat_l')}</span></div>
    </div>
  </div>
</section>

{features_strip()}

<section id="lokale" class="sec">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="lokale_title">{ta('lokale_title')}</h2><p data-i18n="lokale_sub">{ta('lokale_sub')}</p></div>
    <div class="loc-grid">{cards}</div>
  </div>
</section>

<section id="barberzy" class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="barberzy_title">{ta('barberzy_title')}</h2><p data-i18n="barberzy_sub">{ta('barberzy_sub')}</p></div>
    {masters_blocks}
  </div>
</section>

<section id="uslugi" class="sec">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="uslugi_title">{ta('uslugi_title')}</h2><p data-i18n="uslugi_sub">{ta('uslugi_sub')}</p></div>
    <div class="tabs">{tabs}</div>
    <div class="tab-panels">{panels}</div>
  </div>
</section>

<section id="kalkulator" class="sec">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="kalk_title">{ta('kalk_title')}</h2><p data-i18n="kalk_sub">{ta('kalk_sub')}</p></div>
    <div class="calc reveal">
      <div class="calc-top">
        <label data-i18n="kalk_pick">{ta('kalk_pick')}</label>
        <select id="calcLoc"></select>
      </div>
      <div id="calcItems" class="calc-items"></div>
      <div class="calc-bar">
        <div class="calc-sum"><span data-i18n="kalk_total">{ta('kalk_total')}</span><b id="calcTotal">0 zł</b></div>
        <div class="calc-sum"><span data-i18n="kalk_time">{ta('kalk_time')}</span><b id="calcTime">0 min</b></div>
        <a id="calcBook" class="btn btn-amber" href="#" target="_blank" rel="noopener" data-i18n="kalk_book">{ta('kalk_book')}</a>
      </div>
    </div>
  </div>
</section>

<section id="konstruktor" class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="konstr_title">{ta('konstr_title')}</h2><p data-i18n="konstr_sub">{ta('konstr_sub')}</p></div>
    <div class="konstr reveal">
      <div class="konstr-form" id="konstrForm"></div>
      <div class="konstr-result">
        <div class="kr-face" id="krStage"><video id="krVideo" playsinline autoplay muted></video><img id="krImg" alt="Grizzly look"><div class="kr-overlay" id="krOverlay"><svg id="krHair" viewBox="60 30 120 100" preserveAspectRatio="xMidYMid meet"></svg></div><div class="kr-hint" id="krHint"><svg class="cam-ic" viewBox="0 0 24 24"><path d="M3 8.5a2 2 0 0 1 2-2h2l1.4-2h7.2L19 6.5h0a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="3.6"/></svg><button class="btn btn-amber" id="krCamOn" type="button">Przymierz na kamerze</button><span>albo zobacz gotowe zdjęcie niżej</span></div><div class="kr-ctrl" id="krCtrl"><input type="range" id="krScale" min="45" max="150" value="82" aria-label="rozmiar"><button id="krSnap" type="button" title="Zdjęcie">⬇</button><button id="krCamOff" type="button" title="Wyłącz">✕</button></div></div>
        <div class="kr-body">
          <span class="kr-kicker" data-i18n="konstr_look">{ta('konstr_look')}</span>
          <h3 id="krTitle"></h3>
          <p id="krAdvice"></p>
          <div class="kr-serv-lbl" data-i18n="konstr_serv">{ta('konstr_serv')}</div>
          <div id="krServices" class="kr-services"></div>
          <div class="kr-cta">
            <div class="kr-price"><span data-i18n="konstr_from">{ta('konstr_from')}</span><b id="krPrice">—</b></div>
            <button class="btn btn-amber js-book">{t('btn_book')}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="o-nas" class="sec">
  <div class="wrap onas">
    <div class="onas-text reveal">
      <h2 data-i18n="onas_title">{ta('onas_title')}</h2>
      <p data-i18n="onas_p1">{ta('onas_p1')}</p>
      <p data-i18n="onas_p2">{ta('onas_p2')}</p>
      <div class="values">
        <div class="val"><h4 data-i18n="onas_v1t">{ta('onas_v1t')}</h4><p data-i18n="onas_v1d">{ta('onas_v1d')}</p></div>
        <div class="val"><h4 data-i18n="onas_v2t">{ta('onas_v2t')}</h4><p data-i18n="onas_v2d">{ta('onas_v2d')}</p></div>
        <div class="val"><h4 data-i18n="onas_v3t">{ta('onas_v3t')}</h4><p data-i18n="onas_v3d">{ta('onas_v3d')}</p></div>
      </div>
    </div>
    <div class="onas-emblem reveal"><img src="assets/about.jpg" alt="Grizzly Barber Shop — Szczecin" class="onas-photo"></div>
  </div>
</section>

<section id="opinie" class="sec">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="opinie_title">{ta('opinie_title')}</h2><p data-i18n="opinie_sub">{ta('opinie_sub')}</p></div>
    <div class="rev reveal">
      <button class="rev-arrow rev-prev" aria-label="prev">‹</button>
      <div class="rev-track" id="revTrack">{slides}</div>
      <button class="rev-arrow rev-next" aria-label="next">›</button>
    </div>
    <div class="rev-dots" id="revDots">{dots}</div>
  </div>
</section>

<section id="galeria" class="sec sec-alt">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="galeria_title">{ta('galeria_title')}</h2></div>
    {gal}
    <div class="ba-wrap reveal">
      <h3 class="ba-title" data-i18n="ba_title">{ta('ba_title')}</h3>
      <div class="ba" id="ba">
        <div class="ba-after"></div>
        <div class="ba-before" id="baBefore"><div class="ba-lbl">PRZED</div></div>
        <div class="ba-after-lbl">PO</div>
        <div class="ba-handle" id="baHandle"><span>‹ ›</span></div>
        <input type="range" min="0" max="100" value="50" id="baRange" aria-label="before/after">
      </div>
      <p class="ba-note" data-i18n="ba_note">{ta('ba_note')}</p>
    </div>
  </div>
</section>

<section id="faq" class="sec">
  <div class="wrap narrow">
    <div class="sec-head reveal"><h2 data-i18n="faq_title">{ta('faq_title')}</h2></div>
    <div class="faq">{faqs}</div>
  </div>
</section>

<section id="bony" class="sec sec-alt">
  <div class="wrap">
    <div class="gift reveal">
      <div class="gift-emb">{emblem()}</div>
      <h2 data-i18n="gift_title">{ta('gift_title')}</h2>
      <p data-i18n="gift_text">{ta('gift_text')}</p>
      <div class="gift-cta">
        <a class="btn btn-amber" href="{esc(BOOKSY_MAIN)}" target="_blank" rel="noopener" data-i18n="gift_cta">{ta('gift_cta')}</a>
        <a class="btn btn-ghost" href="{esc(WHATSAPP)}" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
  </div>
</section>

<section id="kontakt" class="sec">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="kontakt_title">{ta('kontakt_title')}</h2><p data-i18n="kontakt_sub">{ta('kontakt_sub')}</p></div>
    <div class="contact-wrap">
      <div class="ct-list">{contact_rows}</div>
      <div class="ct-map reveal"><iframe loading="lazy" src="{esc(maps_embed(LOCATIONS[0]['maps']))}" title="Mapa"></iframe></div>
    </div>
  </div>
</section>
</main>
{footer()}"""
    return head("Grizzly Barber Shop — Szczecin · 4 lokale") + body

# ---------------------------------------------------------------------------
# LOCATION PAGE
# ---------------------------------------------------------------------------
def build_location(l):
    svc_rows = "".join(
        f'<tr><td class="st-name">{esc(n)}</td><td class="st-price">{esc(p)}</td><td class="st-time">{esc(tm)}</td></tr>'
        for (n, p, tm) in l["services"])
    team = ""
    if l["staff"]:
        cards = "".join(tm_card(l["slug"], nm, role) for (nm, role) in l["staff"])
        team = f"""<section class="sec sec-alt"><div class="wrap">
  <div class="sec-head reveal"><h2 data-i18n="loc_team_title">{ta('loc_team_title')}</h2></div>
  <div class="team-grid">{cards}</div></div></section>"""
    rate = f'<span class="lh-rate"><span class="stars">★</span> <b>{esc(l["rating"])}</b> · {esc(l["reviews"])} {t("reviews_word")}</span>' if l["rating"] else ""
    phone_row = f'<div class="ib"><span data-i18n="phone_label">{ta("phone_label")}</span><a href="{esc(l["book_url"])}">{esc(l["phone"])}</a></div>' if l["phone"] else ""
    # sibling locations strip
    others = "".join(
        f'<a href="lokal-{o["slug"]}.html">{esc(o["short"])}</a>'
        for o in LOCATIONS if o["slug"] != l["slug"])

    ph = loc_photo(l["slug"]) or "assets/hero.jpg"
    body = f"""{header()}
<main>
<section class="loc-hero">
  <div class="hero-bg" style="background-image:url({ph})"></div>
  <div class="hero-shade"></div>
  <div class="wrap loc-hero-in">
    <a class="back-link" href="index.html#lokale">← <span data-i18n="back_all">{ta('back_all')}</span></a>
    <p class="kicker">Grizzly Barber Shop {open_badge(l['slug'])}</p>
    <h1 class="hero-title">{esc(l['short'])}</h1>
    <p class="hero-sub">{esc(l['address'])}</p>
    {rate}
    <div class="hero-cta">{book_btn(l, big=True)}
      <a class="btn btn-ghost btn-lg" href="{esc(maps_link(l['maps']))}" target="_blank" rel="noopener">Google Maps</a>
    </div>
  </div>
</section>

<section class="info-bar"><div class="wrap info-in">
  <div class="ib"><span data-i18n="addr_label">{ta('addr_label')}</span><b>{esc(l['address'])}</b></div>
  <div class="ib"><span data-i18n="hours_label">{ta('hours_label')}</span><b>{esc(l['hours'])}</b></div>
  {phone_row}
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><h2 data-i18n="loc_menu_title">{ta('loc_menu_title')}</h2></div>
  <table class="svc-table reveal">
    <thead><tr><th data-i18n="svc_service">{ta('svc_service')}</th><th data-i18n="svc_price">{ta('svc_price')}</th><th data-i18n="svc_time">{ta('svc_time')}</th></tr></thead>
    <tbody>{svc_rows}</tbody>
  </table>
  <div class="menu-cta reveal">{book_btn(l, big=True)}</div>
</div></section>

{team}

<section class="sec"><div class="wrap">
  <div class="loc-map reveal"><iframe loading="lazy" src="{esc(maps_embed(l['maps']))}" title="Mapa — {esc(l['short'])}"></iframe></div>
  <div class="sib-strip reveal"><span data-i18n="back_all">{ta('back_all')}:</span> {others}</div>
</div></section>
</main>
{footer()}"""
    return head(f"{l['name']} — Szczecin") + body

# ---------------------------------------------------------------------------
# BARBER PAGE
# ---------------------------------------------------------------------------
def build_barber(l, name, role):
    ph = team_photo(l["slug"], name)
    bg = ph or "assets/hero.jpg"
    svc_rows = "".join(
        f'<tr><td class="st-name">{esc(n)}</td><td class="st-price">{esc(p)}</td><td class="st-time">{esc(tm)}</td></tr>'
        for (n, p, tm) in l["services"])
    others = "".join(
        f'<a href="barber-{bslug(l["slug"], nm)}.html">{esc(nm)}</a>'
        for (nm, rl) in l["staff"] if nm != name)
    others_html = (f'<div class="sib-strip reveal"><span>{esc(l["short"])}:</span> {others}</div>' if others else "")
    body = f"""{header()}
<main>
<section class="loc-hero barber-hero">
  <div class="hero-bg" style="background-image:url({bg})"></div>
  <div class="hero-shade"></div>
  <div class="wrap loc-hero-in">
    <a class="back-link" href="lokal-{l['slug']}.html">← {esc(l['name'])}</a>
    <p class="kicker">{esc(role)} · Grizzly {esc(l['short'])}</p>
    <h1 class="hero-title">{esc(name)}</h1>
    <p class="hero-sub">Barber w Grizzly Barber Shop — {esc(l['address'])}</p>
    <div class="hero-cta">{book_btn(l, big=True)}
      <a class="btn btn-ghost btn-lg" href="lokal-{l['slug']}.html">{t('view_loc')}</a>
    </div>
  </div>
</section>

<section class="info-bar"><div class="wrap info-in">
  <div class="ib"><span data-i18n="staff_label">{ta('staff_label')}</span><b>{esc(name)} — {esc(role)}</b></div>
  <div class="ib"><span data-i18n="addr_label">{ta('addr_label')}</span><b>{esc(l['address'])}</b></div>
  <div class="ib"><span data-i18n="hours_label">{ta('hours_label')}</span><b>{esc(l['hours'])}</b></div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head reveal"><h2 data-i18n="loc_menu_title">{ta('loc_menu_title')}</h2></div>
  <table class="svc-table reveal">
    <thead><tr><th data-i18n="svc_service">{ta('svc_service')}</th><th data-i18n="svc_price">{ta('svc_price')}</th><th data-i18n="svc_time">{ta('svc_time')}</th></tr></thead>
    <tbody>{svc_rows}</tbody>
  </table>
  <div class="menu-cta reveal">{book_btn(l, big=True)}</div>
</div></section>

<section class="sec sec-alt"><div class="wrap">
  <div class="loc-map reveal"><iframe loading="lazy" src="{esc(maps_embed(l['maps']))}" title="Mapa — {esc(l['short'])}"></iframe></div>
  {others_html}
</div></section>
</main>
{footer()}"""
    return head(f"{name} — Grizzly Barber Shop {l['short']} · Szczecin") + body

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0c0c0d; --panel:#151517; --panel2:#1c1c1f; --ink:#f1efe9; --mut:#9a978f;
  --amber:#e4e0d6; --amber2:#ffffff; --line:rgba(240,238,231,.13); --maxw:1160px;
  --card:#151517; --shadow:rgba(0,0,0,.7);
}
html[data-theme="light"]{
  --bg:#f3f1ec; --panel:#fbfaf6; --panel2:#eae7df; --ink:#141413; --mut:#65625b;
  --amber:#2a2a2a; --amber2:#111111; --line:rgba(20,20,20,.14); --card:#fbfaf6; --shadow:rgba(0,0,0,.14);
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:'Barlow',system-ui,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased;transition:background .3s,color .3s;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px}
.wrap.narrow{max-width:760px}
h1,h2,h3,h4{font-family:'Barlow Condensed',sans-serif;font-weight:700;letter-spacing:.01em;line-height:1.05}
.hero-title{font-family:'Anton',sans-serif;font-weight:400;letter-spacing:.02em}

#progress{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--amber),var(--amber2));z-index:100;transition:width .1s}

.btn{display:inline-flex;align-items:center;gap:.4em;padding:.72em 1.35em;border-radius:2px;font-family:'Barlow Condensed',sans-serif;font-weight:600;font-size:1rem;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;border:1px solid transparent;transition:.18s;font-family:'Barlow Condensed'}
.btn-lg{padding:.9em 1.7em;font-size:1.08rem}
.btn-amber{background:var(--ink);color:var(--bg);border:1px solid var(--ink)}
.btn-amber:hover{background:transparent;color:var(--ink);transform:translateY(-1px)}
.btn-ghost{border-color:var(--line);color:var(--ink);background:transparent}
.btn-ghost:hover{border-color:var(--ink);color:var(--amber2)}
.paw{width:34px;height:34px;fill:var(--ink);flex:none}
.emb{height:34px;width:auto;object-fit:contain;flex:none;display:block}
html[data-theme="light"] .emb{filter:invert(1)}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0}

/* promo ribbon */
.promo{background:var(--ink);color:var(--bg)}
.promo.hide{display:none}
.promo-in{display:flex;align-items:center;gap:14px;padding:9px 22px;font-family:'Barlow Condensed';font-weight:600;font-size:.98rem}
.promo-cta{margin-left:auto;background:var(--bg);color:var(--ink);border:none;padding:6px 14px;border-radius:2px;font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.05em;cursor:pointer}
.promo-x{background:none;border:none;color:var(--bg);font-size:1.3rem;cursor:pointer;line-height:1}

/* header */
.site-head{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 82%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.head-in{display:flex;align-items:center;gap:16px;height:64px}
.brand{display:flex;align-items:center;gap:10px}
.brand-word{font-family:'Anton',sans-serif;font-size:1.5rem;letter-spacing:.08em}
.nav{display:flex;gap:20px;margin-left:12px}
.nav a{font-family:'Barlow Condensed';font-weight:600;font-size:.96rem;letter-spacing:.03em;text-transform:uppercase;color:var(--mut);transition:.15s;white-space:nowrap}
.nav a:hover{color:var(--amber2)}
.head-right{margin-left:auto;display:flex;align-items:center;gap:12px}
.theme-btn{background:none;border:1px solid var(--line);color:var(--ink);width:34px;height:34px;border-radius:2px;cursor:pointer;font-size:1rem}
.theme-btn:hover{border-color:var(--amber);color:var(--amber2)}
.lang{display:flex;gap:1px}
.lang button{background:none;border:none;color:var(--mut);font-size:.82rem;font-weight:600;letter-spacing:.05em;cursor:pointer;padding:4px 5px;font-family:'Barlow Condensed'}
.lang button.on{color:var(--amber2)}
.lang button:hover{color:var(--ink)}
.burger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:6px}
.burger span{width:24px;height:2px;background:var(--ink);display:block}
.drawer{display:none}

/* hero */
.hero,.loc-hero{position:relative;overflow:hidden;padding:88px 0 72px;text-align:center}
.loc-hero{padding:84px 0 52px}
.hero-bg{position:absolute;inset:0;z-index:0;background-size:cover;background-position:center;filter:grayscale(1) contrast(1.06) brightness(.34)}
.hero-shade{position:absolute;inset:0;z-index:0;background:radial-gradient(ellipse 80% 70% at 50% 40%,transparent,rgba(0,0,0,.55)),linear-gradient(to bottom,rgba(0,0,0,.4),transparent 30%,rgba(0,0,0,.75))}
html[data-theme="light"] .hero-bg{filter:grayscale(1) contrast(1.05) brightness(.9)}
html[data-theme="light"] .hero-shade{background:linear-gradient(to bottom,rgba(255,255,255,.5),rgba(255,255,255,.2) 40%,rgba(255,255,255,.7))}
.hero-in,.loc-hero-in{position:relative;z-index:1}
.hero-logo{width:min(320px,60vw);height:auto;margin:0 auto 4px;filter:drop-shadow(0 8px 30px rgba(0,0,0,.6))}
html[data-theme="light"] .hero-logo{filter:invert(1) drop-shadow(0 8px 24px rgba(0,0,0,.2))}
.kicker{font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.3em;font-size:.86rem;color:var(--amber2);font-weight:600;margin-bottom:16px;display:flex;gap:10px;align-items:center;justify-content:center}
.hero-title{font-size:clamp(3rem,10vw,7rem);text-shadow:0 4px 30px rgba(0,0,0,.4)}
.hero-sub{max-width:640px;margin:20px auto 0;color:var(--mut);font-size:1.16rem}
.hero-cta{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:32px}
.finder-msg{margin-top:16px;color:var(--amber2);font-weight:600;min-height:1.2em}
.hero-stats{display:flex;gap:44px;justify-content:center;margin-top:50px;flex-wrap:wrap}
.hero-stats b{font-family:'Anton';font-size:2rem;color:var(--amber2);display:block;line-height:1}
.hero-stats span{font-size:.8rem;text-transform:uppercase;letter-spacing:.14em;color:var(--mut)}
.stars{color:var(--amber2)}

.sec{padding:80px 0}
.sec-alt{background:var(--panel)}
.sec-head{text-align:center;max-width:660px;margin:0 auto 46px}
.sec-head h2{font-size:clamp(2rem,5vw,3rem);text-transform:uppercase;display:inline-block;position:relative}
.sec-head h2::after{content:"";display:block;width:54px;height:3px;background:var(--ink);margin:16px auto 0;opacity:.85}
.sec-head p{color:var(--mut);margin-top:14px;font-size:1.08rem}

/* hero est line */
.hero-est{font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.34em;font-size:.74rem;color:var(--mut);margin-top:14px}

/* features / amenities strip */
.features{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--panel)}
.feat-in{display:grid;grid-template-columns:repeat(6,1fr);gap:0}
.feat{display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center;padding:26px 12px;border-left:1px solid var(--line)}
.feat:first-child{border-left:0}
.feat svg{width:26px;height:26px;stroke:var(--ink);fill:none;stroke-width:1.6;opacity:.9}
.feat span{font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.04em;font-size:.82rem;color:var(--mut);line-height:1.2}
.feat:hover span{color:var(--ink)}

/* location card image gradient */
.lc-img{position:relative}
.lc-img::after{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,transparent 55%,rgba(0,0,0,.35))}
html[data-theme="light"] .lc-img::after{background:linear-gradient(to bottom,transparent 60%,rgba(0,0,0,.12))}
.lc-img.emblem::after{display:none}

/* location grid */
.loc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.loc-card{position:relative;background:var(--card);border:1px solid var(--line);border-radius:6px;transition:.2s;overflow:hidden;display:block}
.sec-alt .loc-card{background:var(--panel2)}
.loc-card:hover{border-color:var(--ink);transform:translateY(-4px);box-shadow:0 18px 40px -20px var(--shadow)}
.loc-card:hover .lc-img{filter:grayscale(0);transform:scale(1.04)}
.loc-card.near{border-color:var(--amber2);box-shadow:0 0 0 1px var(--amber2)}
.lc-img{height:190px;background-size:cover;background-position:center;filter:grayscale(1) contrast(1.05) brightness(.8);transition:.4s}
.lc-img.emblem{display:flex;align-items:center;justify-content:center;filter:none;background:radial-gradient(circle at 50% 40%,var(--panel2),#0a0a0b)}
.lc-img.emblem .emb{height:96px;opacity:.85}
.lc-body{padding:24px 26px 30px}
.loc-card h3{font-size:1.9rem;text-transform:uppercase;margin-bottom:6px}
.lc-addr{color:var(--mut);font-size:.98rem;min-height:2.6em}
.lc-rate{display:inline-block;margin-top:12px;font-size:.95rem}
.lc-new{color:var(--amber2);font-weight:600}
.lc-dist{display:block;color:var(--amber2);font-size:.86rem;font-weight:600;margin-top:6px;min-height:1em}
.lc-go{display:block;margin-top:16px;color:var(--amber2);font-family:'Barlow Condensed';font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.lc-flag{position:absolute;top:14px;right:44px;color:var(--amber2);font-size:.9rem}
.open-badge{display:inline-flex;align-items:center;gap:5px;font-size:.72rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding:2px 7px;border-radius:20px;vertical-align:middle}
.open-badge.open{background:rgba(70,180,90,.16);color:#5fce78}
.open-badge.closed{background:rgba(200,80,60,.16);color:#e08a6a}
.loc-card .open-badge{position:absolute;top:13px;right:14px}

/* tabs */
.tabs{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:26px}
.tab{background:var(--card);border:1px solid var(--line);color:var(--mut);padding:9px 18px;border-radius:3px;font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.05em;cursor:pointer;transition:.15s}
.tab:hover{color:var(--ink)}
.tab.on{background:linear-gradient(135deg,var(--amber2),var(--amber));color:#1a1408;border-color:transparent}
.tab-panel{display:none}
.tab-panel.on{display:block}
.svc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.svc{background:var(--card);border:1px solid var(--line);border-radius:5px;padding:18px 20px;display:flex;flex-direction:column;gap:10px}
.svc-name{font-family:'Barlow Condensed';font-weight:600;font-size:1.16rem}
.svc-meta{display:flex;justify-content:space-between;align-items:baseline;gap:10px}
.svc-price{color:var(--amber2);font-family:'Barlow Condensed';font-weight:700;font-size:1.2rem}
.svc-time{color:var(--mut);font-size:.86rem}

/* calculator */
.calc{max-width:760px;margin:0 auto;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:26px}
.calc-top{display:flex;align-items:center;gap:14px;margin-bottom:18px}
.calc-top label{font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--mut)}
.calc-top select{flex:1;background:var(--bg);border:1px solid var(--line);color:var(--ink);padding:10px 12px;border-radius:3px;font:inherit;font-family:'Barlow Condensed';font-size:1.05rem}
.calc-items{display:grid;gap:8px;margin-bottom:20px}
.calc-item{display:flex;align-items:center;gap:12px;padding:11px 14px;background:var(--bg);border:1px solid var(--line);border-radius:4px;cursor:pointer;transition:.15s}
.calc-item:hover{border-color:var(--amber)}
.calc-item input{width:18px;height:18px;accent-color:var(--amber);flex:none}
.calc-item .ci-name{flex:1;font-size:1rem}
.calc-item .ci-price{color:var(--amber2);font-family:'Barlow Condensed';font-weight:700}
.calc-item .ci-time{color:var(--mut);font-size:.82rem;margin-left:10px}
.calc-bar{display:flex;align-items:center;gap:20px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:18px}
.calc-sum{display:flex;flex-direction:column}
.calc-sum span{font-size:.74rem;text-transform:uppercase;letter-spacing:.12em;color:var(--mut)}
.calc-sum b{font-family:'Anton';font-size:1.5rem;color:var(--amber2)}
.calc-bar .btn{margin-left:auto}

/* about */
.onas{display:grid;grid-template-columns:1.5fr 1fr;gap:50px;align-items:center}
.onas-text h2{font-size:clamp(2rem,5vw,3rem);text-transform:uppercase;margin-bottom:18px}
.onas-text p{color:var(--mut);margin-bottom:14px;font-size:1.08rem}
.values{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-top:26px}
.val{border-left:2px solid var(--amber);padding-left:14px}
.val h4{font-size:1.1rem;text-transform:uppercase}
.val p{font-size:.9rem;margin:4px 0 0}
.onas-emblem{display:flex;justify-content:center}
.onas-photo{width:100%;border-radius:8px;border:1px solid var(--line);filter:grayscale(1) contrast(1.05);transition:.4s}
.onas-photo:hover{filter:grayscale(0) contrast(1.05)}

/* reviews */
.rev{position:relative;max-width:820px;margin:0 auto;overflow:hidden}
.rev-track{display:flex;transition:transform .5s cubic-bezier(.4,0,.2,1)}
.rev-slide{min-width:100%;padding:8px 40px;text-align:center}
.rev-slide p{font-size:1.35rem;line-height:1.5;font-family:'Barlow Condensed';font-weight:500}
.rev-by{margin-top:18px}
.rev-by b{color:var(--amber2);font-size:1.1rem;text-transform:uppercase;letter-spacing:.04em}
.rev-by span{display:block;color:var(--mut);font-size:.85rem}
.rev-arrow{position:absolute;top:50%;transform:translateY(-50%);background:none;border:1px solid var(--line);color:var(--ink);width:40px;height:40px;border-radius:50%;font-size:1.4rem;cursor:pointer;z-index:2}
.rev-arrow:hover{border-color:var(--amber);color:var(--amber2)}
.rev-prev{left:0}.rev-next{right:0}
.rev-dots{display:flex;gap:8px;justify-content:center;margin-top:24px}
.rev-dot{width:9px;height:9px;border-radius:50%;border:none;background:var(--line);cursor:pointer;padding:0}
.rev-dot.on{background:var(--amber2)}

/* gallery */
.masonry{columns:3;column-gap:12px}
.masonry img{width:100%;border-radius:5px;margin-bottom:12px;cursor:zoom-in;transition:.35s;filter:grayscale(1) contrast(1.03)}
.masonry img:hover{filter:grayscale(0) contrast(1.03);transform:scale(1.01)}
.gallery-empty{border:1.5px dashed var(--line);border-radius:8px;padding:52px 24px;text-align:center;background:var(--card)}
.gallery-empty p{color:var(--mut);font-size:1.1rem;margin-bottom:20px}
.ge-btns{display:flex;gap:12px;justify-content:center}

/* before/after */
.ba-wrap{max-width:720px;margin:44px auto 0;text-align:center}
.ba-title{text-transform:uppercase;font-size:1.5rem;margin-bottom:16px}
.ba{position:relative;width:100%;max-width:520px;margin:0 auto;aspect-ratio:4/5;border-radius:8px;overflow:hidden;border:1px solid var(--line);user-select:none}
.ba-after{position:absolute;inset:0;background:#111 center/cover no-repeat;background-image:url(assets/after.jpg);filter:grayscale(1) contrast(1.04)}
.ba-before{position:absolute;inset:0;background:#111 center/cover no-repeat;background-image:url(assets/before.jpg);filter:grayscale(1) contrast(1.04);clip-path:inset(0 50% 0 0)}
.ba-lbl,.ba-after-lbl{position:absolute;bottom:12px;font-family:'Barlow Condensed';font-weight:700;letter-spacing:.1em;color:#fff;font-size:.85rem;background:rgba(0,0,0,.45);padding:4px 10px;border-radius:3px;z-index:2}
.ba-lbl{left:12px}.ba-after-lbl{right:12px}
.ba-handle{position:absolute;top:0;bottom:0;left:50%;width:3px;background:var(--amber2);transform:translateX(-50%);z-index:3;pointer-events:none}
.ba-handle span{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:38px;height:38px;border-radius:50%;background:var(--amber2);color:#1a1408;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.9rem}
#baRange{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;margin:0}
.ba-note{color:var(--mut);font-size:.82rem;margin-top:12px}

/* faq */
.faq{display:flex;flex-direction:column;gap:10px}
.faq-item{border:1px solid var(--line);border-radius:5px;background:var(--card);overflow:hidden}
.faq-q{width:100%;display:flex;justify-content:space-between;align-items:center;gap:14px;padding:18px 20px;background:none;border:none;color:var(--ink);font-family:'Barlow Condensed';font-weight:600;font-size:1.14rem;text-align:left;cursor:pointer}
.faq-q span{color:var(--amber2);font-size:1.5rem;transition:transform .25s;flex:none}
.faq-item.open .faq-q span{transform:rotate(45deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .3s}
.faq-a p{padding:0 20px 18px;color:var(--mut)}

/* contact */
.contact-wrap{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start}
.ct-row{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px;border:1px solid var(--line);border-radius:6px;background:var(--card);margin-bottom:12px;flex-wrap:wrap}
.ct-row h4{font-size:1.3rem;text-transform:uppercase;display:flex;align-items:center;gap:8px}
.ct-row p{color:var(--mut);font-size:.95rem}
.ct-sub{font-size:.85rem!important}
.ct-act{display:flex;gap:8px;flex-wrap:wrap}
.ct-map iframe{width:100%;height:100%;min-height:430px;border:0;border-radius:8px;filter:grayscale(.4) contrast(1.05) brightness(.85)}
html[data-theme="light"] .ct-map iframe,html[data-theme="light"] .loc-map iframe{filter:none}

/* location page */
.back-link{display:inline-block;color:var(--mut);font-size:.9rem;letter-spacing:.05em;margin-bottom:20px}
.back-link:hover{color:var(--amber2)}
.lh-rate{display:inline-block;margin-top:12px;font-size:1rem}
.info-bar{background:var(--panel);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.info-in{display:flex;gap:40px;padding:22px;flex-wrap:wrap}
.ib{display:flex;flex-direction:column;gap:4px}
.ib span{font-size:.74rem;text-transform:uppercase;letter-spacing:.14em;color:var(--mut)}
.ib b,.ib a{font-family:'Barlow Condensed';font-size:1.12rem;color:var(--ink)}
.ib a:hover{color:var(--amber2)}
.svc-table{width:100%;border-collapse:collapse;max-width:820px;margin:0 auto}
.svc-table th{text-align:left;font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.08em;color:var(--mut);font-size:.82rem;padding:0 14px 12px;border-bottom:1px solid var(--line)}
.svc-table th:nth-child(n+2),.svc-table td:nth-child(n+2){text-align:right;white-space:nowrap}
.svc-table td{padding:16px 14px;border-bottom:1px solid var(--line)}
.st-name{font-size:1.06rem}
.st-price{color:var(--amber2);font-family:'Barlow Condensed';font-weight:700;font-size:1.14rem}
.st-time{color:var(--mut);font-size:.9rem}
.menu-cta{text-align:center;margin-top:34px}
.team-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;max-width:900px;margin:0 auto}
.tm-card{display:block;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:24px 16px;text-align:center;transition:.2s;cursor:pointer}
.tm-card:hover{border-color:var(--ink);transform:translateY(-3px);box-shadow:0 14px 30px -18px var(--shadow)}
.tm-card:hover .tm-ava.has-photo img{filter:grayscale(0) contrast(1.05)}
.tm-go{display:block;margin-top:10px;color:var(--amber2);font-family:'Barlow Condensed';font-weight:600;letter-spacing:.05em;text-transform:uppercase;font-size:.78rem;opacity:0;transition:.2s}
.tm-card:hover .tm-go{opacity:1}
.tm-ava{width:78px;height:78px;margin:0 auto 14px;border-radius:50%;background:radial-gradient(circle at 40% 30%,var(--panel2),#0a0a0b);display:flex;align-items:center;justify-content:center;border:1px solid var(--line)}
.tm-ava .paw{width:40px;height:40px}
.tm-ava .emb{height:44px;opacity:.9}
.tm-ava.has-photo{padding:0;overflow:hidden}
.tm-ava.has-photo img{width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.05);transition:.35s}
.tm-card:hover .tm-ava.has-photo img{filter:grayscale(0) contrast(1.05)}
.tm-card h4{font-size:1.25rem;text-transform:uppercase}
.tm-card span{color:var(--mut);font-size:.82rem;text-transform:uppercase;letter-spacing:.08em}
.masters-loc{margin-bottom:36px}
.masters-loc .ml-head{text-align:center;text-transform:uppercase;font-size:1.4rem;margin-bottom:18px;letter-spacing:.02em;display:flex;gap:10px;align-items:center;justify-content:center}
.masters-loc .ml-head a{color:var(--mut);font-size:.85rem;font-weight:500;text-transform:none;letter-spacing:0}
.masters-loc .ml-head a:hover{color:var(--ink)}
.loc-map iframe{width:100%;height:440px;border:0;border-radius:8px;filter:grayscale(.4) contrast(1.05) brightness(.85)}
.sib-strip{margin-top:26px;text-align:center;color:var(--mut);font-family:'Barlow Condensed';letter-spacing:.03em}
.sib-strip a{color:var(--amber2);margin:0 8px;text-transform:uppercase;font-weight:600}

/* footer */
.site-foot{background:color-mix(in srgb,var(--bg) 60%,#000);border-top:1px solid var(--line);padding:44px 0 0}
html[data-theme="light"] .site-foot{background:var(--panel2)}
.foot-in{display:flex;justify-content:space-between;gap:30px;flex-wrap:wrap;padding-bottom:28px}
.foot-tag{color:var(--mut);margin-top:10px;font-size:.95rem}
.foot-locs{display:flex;gap:14px;flex-wrap:wrap;align-items:center;color:var(--mut)}
.foot-locs a:hover{color:var(--amber2)}
.foot-social{display:flex;gap:16px}
.foot-social a{color:var(--amber2);font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.06em}
.foot-bar{border-top:1px solid var(--line);padding:18px 22px;color:var(--mut);font-size:.85rem;text-align:center}

/* modal */
.modal{position:fixed;inset:0;z-index:90;background:rgba(0,0,0,.7);display:none;align-items:center;justify-content:center;padding:20px}
.modal.open{display:flex}
.modal-card{background:var(--panel);border:1px solid var(--line);border-radius:10px;max-width:460px;width:100%;padding:30px;position:relative}
.modal-x{position:absolute;top:14px;right:16px;background:none;border:none;color:var(--mut);font-size:1.6rem;cursor:pointer;line-height:1}
.modal-card h3{font-size:1.6rem;text-transform:uppercase}
.modal-card>p{color:var(--mut);margin:8px 0 20px}
.mo-list{display:flex;flex-direction:column;gap:10px}
.mo-loc{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:16px;border:1px solid var(--line);border-radius:6px;transition:.15s}
.mo-loc:hover{border-color:var(--amber);background:var(--card)}
.mo-loc b{font-family:'Barlow Condensed';font-size:1.2rem;text-transform:uppercase;display:block}
.mo-loc span{color:var(--mut);font-size:.85rem}
.mo-go{color:var(--amber2);font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;font-size:.82rem;white-space:nowrap}

/* mobile CTA bar */
.mobar{position:fixed;left:0;right:0;bottom:0;z-index:45;padding:10px 16px;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(10px);border-top:1px solid var(--line);display:none}

/* lightbox */
.lightbox{position:fixed;inset:0;z-index:95;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center}
.lightbox.open{display:flex}
.lightbox img{max-width:90vw;max-height:86vh;border-radius:4px}
.lb-close,.lb-prev,.lb-next{position:absolute;background:none;border:none;color:#fff;cursor:pointer;font-size:2.4rem;padding:16px}
.lb-close{top:8px;right:14px;font-size:2.6rem}
.lb-prev{left:6px;top:50%;transform:translateY(-50%)}
.lb-next{right:6px;top:50%;transform:translateY(-50%)}

#toTop{position:fixed;right:20px;bottom:20px;width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:var(--panel);color:var(--amber2);font-size:1.2rem;cursor:pointer;opacity:0;pointer-events:none;transition:.25s;z-index:44}
#toTop.show{opacity:1;pointer-events:auto}
#toTop:hover{border-color:var(--amber);transform:translateY(-2px)}

.js .reveal{opacity:0;transform:translateY(22px);transition:opacity .6s,transform .6s}
.js .reveal.in{opacity:1;transform:none}

/* hairstyle constructor */
.konstr{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}
.konstr-form{display:flex;flex-direction:column;gap:18px}
.kcat-h{font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);font-size:.82rem;margin-bottom:9px}
.kchips{display:flex;flex-wrap:wrap;gap:8px}
.kchip{background:var(--bg);border:1px solid var(--line);color:var(--ink);padding:8px 14px;border-radius:3px;font-family:'Barlow Condensed';font-weight:600;letter-spacing:.03em;cursor:pointer;transition:.15s}
.kchip:hover{border-color:var(--ink)}
.kchip.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.kchip.dis{opacity:.4;cursor:default}
.sec-alt .kchip{background:var(--panel2)}
.konstr-result{background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden;display:flex;flex-direction:column;position:sticky;top:84px}
.sec-alt .konstr-result{background:var(--panel2)}
.kr-face{position:relative;aspect-ratio:3/4;background:#0f0f10;overflow:hidden;border-bottom:1px solid var(--line)}
#krVideo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scaleX(-1);display:none}
#krImg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.04);transition:filter .4s}
.kr-overlay{position:absolute;left:50%;top:15%;width:82%;transform:translateX(-50%);cursor:grab;touch-action:none;z-index:2}
.kr-overlay:active{cursor:grabbing}
.kr-overlay svg{width:100%;height:auto;display:block;filter:drop-shadow(0 4px 10px rgba(0,0,0,.45))}
.kr-hint{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:rgba(0,0,0,.34);color:#fff;text-align:center;padding:20px}
.kr-hint .cam-ic{width:40px;height:40px;stroke:#fff;fill:none;stroke-width:1.5;opacity:.92}
.kr-hint span{font-size:.82rem;color:rgba(255,255,255,.7)}
.kr-ctrl{position:absolute;left:0;right:0;bottom:0;z-index:4;display:none;align-items:center;gap:10px;padding:11px 14px;background:linear-gradient(to top,rgba(0,0,0,.65),transparent)}
.kr-ctrl input[type=range]{flex:1;accent-color:#fff}
.kr-ctrl button{background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.4);color:#fff;min-width:38px;height:34px;border-radius:4px;cursor:pointer;font-size:1rem}
.kr-ctrl button:hover{background:rgba(255,255,255,.28)}
.kr-face:not(.cam) .kr-overlay{display:none!important}
.kr-face.cam #krVideo{display:block}
.kr-face.cam #krImg{display:none}
.kr-face.cam .kr-hint{display:none}
.kr-face.cam .kr-ctrl{display:flex}
.kpalette{display:flex;flex-wrap:wrap;gap:12px}
.kswatch{display:flex;flex-direction:column;align-items:center;gap:6px;background:none;border:none;cursor:pointer;padding:2px}
.ksw-dot{width:30px;height:30px;border-radius:50%;border:2px solid var(--line);box-shadow:inset 0 0 0 2px var(--bg);transition:.15s}
.kswatch:hover .ksw-dot{border-color:var(--mut)}
.kswatch.on .ksw-dot{border-color:var(--ink);transform:scale(1.1)}
.ksw-l{font-family:'Barlow Condensed';font-size:.72rem;text-transform:uppercase;letter-spacing:.03em;color:var(--mut)}
.kswatch.on .ksw-l{color:var(--ink)}
.kr-body{padding:22px 24px;display:flex;flex-direction:column;gap:8px}
.kr-kicker{font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.18em;font-size:.72rem;color:var(--mut)}
.kr-body h3{font-size:1.5rem;line-height:1.1}
.kr-body>p{color:var(--mut);font-size:.98rem}
.kr-serv-lbl{font-family:'Barlow Condensed';text-transform:uppercase;letter-spacing:.06em;font-size:.76rem;color:var(--mut);margin-top:8px}
.kr-services{display:flex;flex-direction:column}
.kserv{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:.98rem}
.kserv b{color:var(--amber2);font-family:'Barlow Condensed';white-space:nowrap}
.kr-cta{display:flex;align-items:center;gap:16px;margin-top:16px}
.kr-price{display:flex;flex-direction:column}
.kr-price span{font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:var(--mut)}
.kr-price b{font-family:'Anton';font-size:1.5rem;color:var(--amber2)}
.kr-cta .btn{margin-left:auto}

/* gift cards */
.gift{max-width:680px;margin:0 auto;text-align:center;border:1px solid var(--line);border-radius:10px;padding:46px 30px;background:var(--card)}
.gift-emb .emb{height:66px;margin:0 auto 16px}
.gift h2{font-size:clamp(1.8rem,4vw,2.6rem);text-transform:uppercase}
.gift p{color:var(--mut);max-width:520px;margin:14px auto 24px;font-size:1.06rem}
.gift-cta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}

@media(max-width:860px){.konstr{grid-template-columns:1fr}.konstr-result{position:static}}
@media(max-width:980px){.masonry{columns:2}}
@media(max-width:860px){
  .onas{grid-template-columns:1fr}.onas-emblem{order:-1}
  .contact-wrap{grid-template-columns:1fr}.ct-map iframe{min-height:320px}
  .values{grid-template-columns:1fr}
  .feat-in{grid-template-columns:repeat(3,1fr)}
  .feat:nth-child(3n+1){border-left:0}.feat:nth-child(n+4){border-top:1px solid var(--line)}
}
@media(max-width:520px){
  .feat-in{grid-template-columns:repeat(2,1fr)}
  .feat{border-left:0!important}.feat:nth-child(2n){border-left:1px solid var(--line)!important}
  .feat:nth-child(n+3){border-top:1px solid var(--line)}
}
@media(max-width:940px){
  .nav{display:none}.head-cta{display:none}.burger{display:flex}
  .drawer{display:block;max-height:0;overflow:hidden;transition:max-height .35s;background:var(--panel);border-bottom:1px solid var(--line)}
  .drawer.open{max-height:720px}
  .drawer nav{display:flex;flex-direction:column;gap:2px;padding:14px 22px}
  .drawer nav a{padding:12px 0;text-transform:uppercase;font-family:'Barlow Condensed';font-weight:600;color:var(--ink);border-bottom:1px solid var(--line)}
  .drawer .btn{margin-top:12px;justify-content:center}
}
@media(max-width:760px){
  .info-in{gap:22px}.masonry{columns:1}
  .mobar{display:block}.mobar+*{margin-bottom:70px}
  body{padding-bottom:64px}
  .promo-in{font-size:.86rem;flex-wrap:wrap}
  .rev-slide{padding:8px 34px}.rev-slide p{font-size:1.15rem}
  .calc-bar .btn{margin-left:0;width:100%}
}
"""

# ---------------------------------------------------------------------------
# JS
# ---------------------------------------------------------------------------
APP_JS = r"""
(function(){
  var I=window.I18N||{}, G=window.GRZ||{locs:[]};
  var LANG='pl';
  function cur(){return I[LANG]||I.pl||{};}

  /* ---------- i18n ---------- */
  function setLang(l){
    LANG=l; var d=cur();
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      var k=el.getAttribute('data-i18n'); if(d[k]!=null) el.textContent=d[k];
    });
    document.documentElement.lang=l;
    document.querySelectorAll('#lang button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-l')===l);});
    try{localStorage.setItem('grz_lang',l);}catch(e){}
    renderOpen(); buildCalc();
  }
  var saved; try{saved=localStorage.getItem('grz_lang');}catch(e){}
  document.querySelectorAll('#lang button').forEach(function(b){b.addEventListener('click',function(){setLang(b.getAttribute('data-l'));});});

  /* ---------- theme ---------- */
  var tb=document.getElementById('themeBtn');
  if(tb)tb.addEventListener('click',function(){
    var r=document.documentElement, now=r.getAttribute('data-theme')==='light'?'':'light';
    if(now)r.setAttribute('data-theme','light');else r.removeAttribute('data-theme');
    try{localStorage.setItem('grz_theme',now);}catch(e){}
  });

  /* ---------- burger ---------- */
  var burger=document.getElementById('burger'),drawer=document.getElementById('drawer');
  if(burger){burger.addEventListener('click',function(){drawer.classList.toggle('open');});
    drawer.querySelectorAll('a,.btn').forEach(function(a){a.addEventListener('click',function(){drawer.classList.remove('open');});});}

  /* ---------- promo ---------- */
  var promo=document.getElementById('promo');
  try{if(localStorage.getItem('grz_promo')==='0'&&promo)promo.classList.add('hide');}catch(e){}
  var px=document.getElementById('promoX');
  if(px)px.addEventListener('click',function(){promo.classList.add('hide');try{localStorage.setItem('grz_promo','0');}catch(e){}});

  /* ---------- reveal ---------- */
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12});
  document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});

  /* ---------- scroll progress + toTop ---------- */
  var pg=document.getElementById('progress'),tt=document.getElementById('toTop');
  function onScroll(){
    var h=document.documentElement, sc=h.scrollTop, max=h.scrollHeight-h.clientHeight;
    if(pg)pg.style.width=(max>0?(sc/max*100):0)+'%';
    if(tt)tt.classList.toggle('show',sc>500);
  }
  window.addEventListener('scroll',onScroll); onScroll();
  if(tt)tt.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});

  /* ---------- count-up ---------- */
  var counters=document.querySelectorAll('[data-count]');
  var cio=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return; cio.unobserve(e.target);
    var el=e.target, end=parseInt(el.getAttribute('data-count'),10), suf=end>100?'+':'', t0=null;
    function step(ts){if(!t0)t0=ts;var p=Math.min((ts-t0)/1100,1);el.textContent=Math.floor(p*end)+suf;if(p<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);
  });},{threshold:.5});
  counters.forEach(function(el){cio.observe(el);});

  /* ---------- open-now badges ---------- */
  function isOpen(o){if(!o)return null;var h=new Date().getHours();return h>=o[0]&&h<o[1];}
  function renderOpen(){
    var d=cur();
    document.querySelectorAll('[data-open]').forEach(function(el){
      var loc=G.locs.filter(function(x){return x.slug===el.getAttribute('data-open');})[0];
      if(!loc){el.textContent='';return;}
      var st=isOpen(loc.open);
      el.classList.remove('open','closed');
      if(st===true){el.classList.add('open');el.textContent='● '+(d.open_now||'Open');}
      else{el.classList.add('closed');el.textContent='● '+(d.closed_now||'Closed');}
    });
  }

  /* ---------- price tabs ---------- */
  document.querySelectorAll('.tab').forEach(function(b){
    b.addEventListener('click',function(){
      var s=b.getAttribute('data-tab');
      document.querySelectorAll('.tab').forEach(function(x){x.classList.toggle('on',x===b);});
      document.querySelectorAll('.tab-panel').forEach(function(p){p.classList.toggle('on',p.getAttribute('data-panel')===s);});
    });
  });

  /* ---------- booking modal ---------- */
  var modal=document.getElementById('bookModal');
  function openModal(){if(modal)modal.classList.add('open');}
  function closeModal(){if(modal)modal.classList.remove('open');}
  document.querySelectorAll('.js-book').forEach(function(b){b.addEventListener('click',openModal);});
  if(modal){modal.addEventListener('click',function(e){if(e.target===modal||e.target.classList.contains('modal-x'))closeModal();});}

  /* ---------- nearest finder ---------- */
  function haversine(a,b,c,d){var R=6371,dl=(c-a)*Math.PI/180,dn=(d-b)*Math.PI/180;
    var x=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a*Math.PI/180)*Math.cos(c*Math.PI/180)*Math.sin(dn/2)*Math.sin(dn/2);
    return R*2*Math.atan2(Math.sqrt(x),Math.sqrt(1-x));}
  var fb=document.getElementById('finderBtn'),fm=document.getElementById('finderMsg');
  if(fb)fb.addEventListener('click',function(){
    var d=cur();
    if(!navigator.geolocation){document.getElementById('lokale').scrollIntoView({behavior:'smooth'});return;}
    fm.textContent=d.finder_wait||'…';
    navigator.geolocation.getCurrentPosition(function(pos){
      var la=pos.coords.latitude, ln=pos.coords.longitude, best=null;
      G.locs.forEach(function(l){var km=haversine(la,ln,l.lat,l.lng);l._km=km;if(!best||km<best._km)best=l;});
      document.querySelectorAll('[data-dist]').forEach(function(el){
        var l=G.locs.filter(function(x){return x.slug===el.getAttribute('data-dist');})[0];
        if(l&&l._km!=null)el.textContent='≈ '+l._km.toFixed(1)+' '+(d.km||'km');
      });
      document.querySelectorAll('.loc-card').forEach(function(c){c.classList.toggle('near',c.getAttribute('data-slug')===best.slug);});
      fm.textContent=(d.finder_res||'')+' '+best.short+' (≈ '+best._km.toFixed(1)+' '+(d.km||'km')+')';
      var card=document.querySelector('.loc-card.near'); if(card)card.scrollIntoView({behavior:'smooth',block:'center'});
    },function(){fm.textContent=d.finder_deny||'';document.getElementById('lokale').scrollIntoView({behavior:'smooth'});});
  });

  /* ---------- calculator ---------- */
  var cLoc=document.getElementById('calcLoc'),cItems=document.getElementById('calcItems'),
      cTot=document.getElementById('calcTotal'),cTime=document.getElementById('calcTime'),cBook=document.getElementById('calcBook');
  function buildCalc(){
    if(!cLoc)return; var d=cur(), keep=cLoc.value;
    cLoc.innerHTML=G.locs.map(function(l){return '<option value="'+l.slug+'">'+l.short+'</option>';}).join('');
    if(keep)cLoc.value=keep;
    renderItems();
  }
  function renderItems(){
    if(!cItems)return;
    var loc=G.locs.filter(function(l){return l.slug===cLoc.value;})[0]||G.locs[0];
    cItems.innerHTML=loc.services.map(function(s,i){
      return '<label class="calc-item"><input type="checkbox" data-num="'+s.num+'" data-min="'+s.min+'">'
        +'<span class="ci-name">'+s.name+'</span>'
        +'<span class="ci-price">'+s.price+'</span><span class="ci-time">'+s.time+'</span></label>';
    }).join('');
    cItems.querySelectorAll('input').forEach(function(x){x.addEventListener('change',calcSum);});
    cBook.href=loc.book_url; cBook.target=loc.book_type==='phone'?'':'_blank';
    calcSum();
  }
  function calcSum(){
    var sum=0,mn=0;
    cItems.querySelectorAll('input:checked').forEach(function(x){sum+=+x.getAttribute('data-num');mn+=+x.getAttribute('data-min');});
    cTot.textContent=sum+' zł';
    var h=Math.floor(mn/60),m=mn%60; cTime.textContent=(h?h+' g ':'')+(m?m+' min':(h?'':'0 min'));
  }
  if(cLoc){cLoc.addEventListener('change',renderItems);}

  /* ---------- reviews carousel ---------- */
  var track=document.getElementById('revTrack');
  if(track){
    var slides=track.children.length,idx=0,dotsWrap=document.getElementById('revDots'),timer;
    function go(i){idx=(i+slides)%slides;track.style.transform='translateX(-'+(idx*100)+'%)';
      dotsWrap.querySelectorAll('.rev-dot').forEach(function(dt,j){dt.classList.toggle('on',j===idx);});}
    function auto(){clearInterval(timer);timer=setInterval(function(){go(idx+1);},5000);}
    dotsWrap.querySelectorAll('.rev-dot').forEach(function(dt){dt.addEventListener('click',function(){go(+dt.getAttribute('data-i'));auto();});});
    document.querySelector('.rev-next').addEventListener('click',function(){go(idx+1);auto();});
    document.querySelector('.rev-prev').addEventListener('click',function(){go(idx-1);auto();});
    var sx=null;track.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;},{passive:true});
    track.addEventListener('touchend',function(e){if(sx==null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)go(idx+(dx<0?1:-1));sx=null;auto();},{passive:true});
    auto();
  }

  /* ---------- faq ---------- */
  document.querySelectorAll('.faq-q').forEach(function(q){
    q.addEventListener('click',function(){
      var it=q.parentElement,a=it.querySelector('.faq-a'),open=it.classList.toggle('open');
      a.style.maxHeight=open?a.scrollHeight+'px':0;
    });
  });

  /* ---------- before/after ---------- */
  var baR=document.getElementById('baRange'),baB=document.getElementById('baBefore'),baH=document.getElementById('baHandle');
  if(baR){function baSet(v){baB.style.clipPath='inset(0 '+(100-v)+'% 0 0)';baH.style.left=v+'%';}
    baR.addEventListener('input',function(){baSet(baR.value);}); baSet(50);}

  /* ---------- lightbox ---------- */
  var lb=document.getElementById('lightbox'),lbImg=document.getElementById('lbImg'),lbImgs=[],lbIdx=0;
  function lbShow(i){lbIdx=(i+lbImgs.length)%lbImgs.length;lbImg.src=lbImgs[lbIdx].src;}
  document.querySelectorAll('img.lb').forEach(function(im,i){lbImgs.push(im);
    im.addEventListener('click',function(){lb.classList.add('open');lbShow(i);});});
  if(lb){
    lb.querySelector('.lb-close').addEventListener('click',function(){lb.classList.remove('open');});
    lb.querySelector('.lb-next').addEventListener('click',function(e){e.stopPropagation();lbShow(lbIdx+1);});
    lb.querySelector('.lb-prev').addEventListener('click',function(e){e.stopPropagation();lbShow(lbIdx-1);});
    lb.addEventListener('click',function(e){if(e.target===lb)lb.classList.remove('open');});
    document.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;
      if(e.key==='Escape')lb.classList.remove('open');if(e.key==='ArrowRight')lbShow(lbIdx+1);if(e.key==='ArrowLeft')lbShow(lbIdx-1);});
  }

  /* ---------- hairstyle constructor ---------- */
  var kForm=document.getElementById('konstrForm');
  if(kForm){
    var STYLES=['Fade','Undercut','Pompadour','Tekstura','Crew cut','Grzywka','Zaczesane do tyłu','Przedziałek','Loki','Irokez','Jeżyk','Kok','Na łyso'];
    var COLORS=['Naturalny','Brąz','Rozjaśnienie','Platyna / siwy','Cover'];
    var HCOL={'Naturalny':'#22221e','Brąz':'#4a3324','Rozjaśnienie':'#c2a877','Platyna / siwy':'#d3d0c8','Cover':'#3b3b37'};
    var TINT={'Naturalny':'grayscale(1) contrast(1.04)','Brąz':'sepia(.55) saturate(1.5) brightness(.92) contrast(1.02)','Rozjaśnienie':'grayscale(.1) sepia(.28) brightness(1.26) contrast(.95)','Platyna / siwy':'grayscale(1) brightness(1.32) contrast(.9)','Cover':'grayscale(1) brightness(.72) contrast(1.12)'};
    var HAIR={
     'Fade':'M74,114 C68,74 94,50 120,50 C146,50 172,74 166,114 C160,88 150,72 120,72 C90,72 80,88 74,114 Z',
     'Undercut':'M84,88 C86,52 154,52 156,88 C150,62 90,62 84,88 Z',
     'Pompadour':'M80,84 C78,42 116,28 134,42 C154,44 162,66 158,86 C150,58 96,58 80,84 Z',
     'Tekstura':'M76,90 l7,-16 8,13 9,-19 8,17 10,-21 10,19 9,-15 7,13 5,9 C150,60 92,60 76,90 Z',
     'Crew cut':'M78,74 C80,52 100,46 120,46 C140,46 160,52 162,74 C150,60 90,60 78,74 Z',
     'Grzywka':'M74,110 C72,70 96,50 120,50 C144,50 168,70 166,110 C160,84 150,72 120,72 C104,72 92,78 84,88 L90,102 96,88 102,102 108,88 114,102 120,88 126,100 Z',
     'Zaczesane do tyłu':'M80,80 C78,50 116,42 130,52 C150,54 160,72 155,92 C150,66 96,64 80,80 Z',
     'Przedziałek':'M76,98 C74,64 98,50 120,50 C144,50 168,66 166,100 C160,78 150,66 121,66 L118,58 115,66 C104,68 84,78 76,98 Z',
     'Loki':'M74,94 q2,-13 12,-14 q3,-11 15,-9 q6,-9 19,-6 q9,-4 18,3 q12,0 15,12 q7,4 5,16 C150,64 92,64 74,94 Z',
     'Irokez':'M109,40 C107,32 133,32 131,40 L128,90 112,90 Z',
     'Jeżyk':'M82,72 C84,56 100,50 120,50 C140,50 156,56 158,72 C150,62 90,62 82,72 Z',
     'Kok':'M80,84 C80,54 104,48 120,48 C138,48 158,58 156,86 C150,62 96,62 80,84 Z',
     'Na łyso':''
    };
    var PHOTO={'Loki':'assets/style/dlugie_nb.jpg','Kok':'assets/style/dlugie_nb.jpg','Na łyso':'assets/style/lyso_nb.jpg','Pompadour':'assets/style/srednie_nb.jpg','Zaczesane do tyłu':'assets/style/srednie_nb.jpg','Tekstura':'assets/style/srednie_nb.jpg','Grzywka':'assets/style/srednie_nb.jpg','Przedziałek':'assets/style/srednie_nb.jpg'};
    function photoFor(st){return PHOTO[st]||'assets/style/krotkie_nb.jpg';}
    var ksel={style:'Fade',color:'Naturalny'};
    var vid=document.getElementById('krVideo'), kimg=document.getElementById('krImg'),
        ov=document.getElementById('krOverlay'), hair=document.getElementById('krHair'),
        stage=document.getElementById('krStage'), stream=null;

    function kRender(){
      kForm.innerHTML='';
      var r1=document.createElement('div'); r1.className='kcat';
      r1.innerHTML='<div class="kcat-h">Fryzura</div>';
      var w1=document.createElement('div'); w1.className='kchips';
      STYLES.forEach(function(o){var b=document.createElement('button');b.type='button';b.className='kchip'+(ksel.style===o?' on':'');b.textContent=o;b.addEventListener('click',function(){ksel.style=o;kRender();kResult();});w1.appendChild(b);});
      r1.appendChild(w1); kForm.appendChild(r1);
      var r2=document.createElement('div'); r2.className='kcat';
      r2.innerHTML='<div class="kcat-h">Kolor włosów</div>';
      var pal=document.createElement('div'); pal.className='kpalette';
      COLORS.forEach(function(o){var b=document.createElement('button');b.type='button';b.className='kswatch'+(ksel.color===o?' on':'');b.title=o;b.innerHTML='<span class="ksw-dot" style="background:'+HCOL[o]+'"></span><span class="ksw-l">'+o+'</span>';b.addEventListener('click',function(){ksel.color=o;kRender();kResult();});pal.appendChild(b);});
      r2.appendChild(pal); kForm.appendChild(r2);
    }
    function shade(hex,amt){var n=parseInt(hex.slice(1),16);var r=Math.max(0,Math.min(255,(n>>16)+amt));var g=Math.max(0,Math.min(255,((n>>8)&255)+amt));var b=Math.max(0,Math.min(255,(n&255)+amt));return '#'+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1);}
    function drawHair(){
      var hp=HAIR[ksel.style];
      if(!hp){ hair.innerHTML=''; ov.style.display='none'; return; }
      ov.style.display='';
      var base=HCOL[ksel.color], lite=shade(base,34), drk=shade(base,-30);
      var defs='<defs><linearGradient id="hg" x1="0" y1="0" x2="0.2" y2="1">'
        +'<stop offset="0" stop-color="'+lite+'"/><stop offset=".5" stop-color="'+base+'"/><stop offset="1" stop-color="'+drk+'"/></linearGradient>'
        +'<clipPath id="hc"><path d="'+hp+'"/></clipPath>'
        +'<filter id="hb" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="0.6"/></filter></defs>';
      var strands='';
      for(var i=0;i<30;i++){var x=62+i*3.9, w1=Math.sin(i*1.3)*4, w2=Math.sin(i*0.7+1)*5;
        strands+='<path d="M'+x.toFixed(1)+',36 q'+w1.toFixed(1)+',32 '+w2.toFixed(1)+',64" stroke="'+lite+'" stroke-width="0.65" fill="none" opacity="'+(0.22+0.16*Math.abs(Math.sin(i))).toFixed(2)+'"/>';
        strands+='<path d="M'+(x+1.6).toFixed(1)+',40 q'+(w1*0.8).toFixed(1)+',30 '+(w2*0.9).toFixed(1)+',58" stroke="'+drk+'" stroke-width="0.5" fill="none" opacity="0.2"/>';}
      hair.innerHTML=defs
        +'<path d="'+hp+'" fill="url(#hg)" filter="url(#hb)"/>'
        +'<g clip-path="url(#hc)">'+strands+'</g>'
        +'<path d="'+hp+'" fill="none" stroke="'+drk+'" stroke-width="0.9" opacity=".55"/>';
    }
    function kResult(){
      var src=photoFor(ksel.style);
      if(kimg.getAttribute('src')!==src) kimg.src=src;
      kimg.style.filter=TINT[ksel.color]||'grayscale(1)';
      drawHair();
      var lyso=ksel.style==='Na łyso', svc=[],price=0;
      if(lyso){svc.push(['Głowa na łyso','od 60 zł']);price+=60;}
      else{svc.push(['Grizzly Cut — strzyżenie','od 90 zł']);price+=90;}
      if(ksel.color==='Rozjaśnienie'){svc.push(['Rozjaśnianie','od 200 zł']);price+=200;}
      else if(ksel.color!=='Naturalny'){svc.push(['COVER — koloryzacja','od 70 zł']);price+=70;}
      var parts=[ksel.style]; if(ksel.color!=='Naturalny')parts.push(ksel.color);
      var T=function(id){return document.getElementById(id);};
      T('krTitle').textContent=parts.join(' · ');
      T('krAdvice').textContent='Przymierz look na sobie w kamerze i pokaż go barberowi w Grizzly — dopniemy detale pod Twój typ włosów i zarost.';
      T('krServices').innerHTML=svc.map(function(x){return '<div class="kserv"><span>'+x[0]+'</span><b>'+x[1]+'</b></div>';}).join('');
      T('krPrice').textContent=price+' zł';
    }

    /* camera */
    var camOn=document.getElementById('krCamOn'),camOff=document.getElementById('krCamOff'),
        snap=document.getElementById('krSnap'),scale=document.getElementById('krScale');
    function startCam(){
      if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){alert('Kamera niedostępna w tej przeglądarce.');return;}
      navigator.mediaDevices.getUserMedia({video:{facingMode:'user'},audio:false}).then(function(st){
        stream=st; vid.srcObject=st; var p=vid.play(); if(p&&p.catch)p.catch(function(){});
        stage.classList.add('cam');
        function manual(){ stage.classList.remove('ar'); ov.style.left='50%'; ov.style.top='14%'; ov.style.width=scale.value+'%'; ov.style.transform='translateX(-50%)'; }
        if(window.startGrizzlyCam){
          window.__hairMul=(scale.value/82);
          stage.classList.add('ar'); ov.style.transform='none';
          window.startGrizzlyCam(vid,ov,null,function(){ manual(); });
        } else { manual(); }
      }).catch(function(){ alert('Nie udało się włączyć kamery. Sprawdź uprawnienia (kłódka w pasku adresu).'); });
    }
    function stopCam(){ if(window.stopGrizzlyCam)window.stopGrizzlyCam(); if(stream){stream.getTracks().forEach(function(t){t.stop();});stream=null;} vid.srcObject=null; stage.classList.remove('cam'); stage.classList.remove('ar'); }
    if(camOn)camOn.addEventListener('click',startCam);
    if(camOff)camOff.addEventListener('click',stopCam);
    if(scale)scale.addEventListener('input',function(){ if(stage.classList.contains('ar')){window.__hairMul=scale.value/82;} else {ov.style.width=scale.value+'%';} });

    /* drag overlay */
    (function(){
      var drag=false,ox=0,oy=0,sl=50,st=14;
      function down(e){if(stage.classList.contains('ar'))return;drag=true;var p=e.touches?e.touches[0]:e;ox=p.clientX;oy=p.clientY;sl=parseFloat(ov.style.left)||50;st=parseFloat(ov.style.top)||14;ov.style.transform='none';if(e.cancelable)e.preventDefault();}
      function move(e){if(!drag)return;var p=e.touches?e.touches[0]:e;var r=stage.getBoundingClientRect();
        ov.style.left=Math.max(2,Math.min(98,sl+((p.clientX-ox)/r.width*100)))+'%';
        ov.style.top=Math.max(0,Math.min(78,st+((p.clientY-oy)/r.height*100)))+'%';}
      function up(){drag=false;}
      ov.addEventListener('mousedown',down); window.addEventListener('mousemove',move); window.addEventListener('mouseup',up);
      ov.addEventListener('touchstart',down,{passive:false}); window.addEventListener('touchmove',move,{passive:false}); window.addEventListener('touchend',up);
    })();

    /* snapshot */
    if(snap)snap.addEventListener('click',function(){
      if(!stream){alert('Najpierw włącz kamerę.');return;}
      try{
        var r=stage.getBoundingClientRect(),c=document.createElement('canvas');
        c.width=Math.round(r.width);c.height=Math.round(r.height);var cx=c.getContext('2d');
        var vw=vid.videoWidth||c.width,vh=vid.videoHeight||c.height,sc=Math.max(c.width/vw,c.height/vh);
        cx.save();cx.translate(c.width,0);cx.scale(-1,1);
        cx.drawImage(vid,(c.width-vw*sc)/2,(c.height-vh*sc)/2,vw*sc,vh*sc);cx.restore();
        var svgStr=new XMLSerializer().serializeToString(hair);
        var im=new Image();
        im.onload=function(){ cx.drawImage(im,ov.offsetLeft,ov.offsetTop,ov.offsetWidth,ov.offsetHeight);
          var a=document.createElement('a');a.download='grizzly-look.png';a.href=c.toDataURL('image/png');a.click(); };
        im.onerror=function(){alert('Nie udało się zapisać zdjęcia.');};
        im.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svgStr);
      }catch(err){alert('Nie udało się zapisać zdjęcia.');}
    });

    kRender(); kResult();
  }

  /* ---------- init ---------- */
  var start=saved||'pl';   // Polish is the default language
  buildCalc();
  setLang(start);
})();
"""

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
           '<rect width="100" height="100" rx="18" fill="#12100d"/>'
           '<g fill="#f0a63a">'
           '<ellipse cx="50" cy="64" rx="22" ry="18"/>'
           '<ellipse cx="26" cy="45" rx="7.5" ry="10"/>'
           '<ellipse cx="42" cy="34" rx="8" ry="11.5"/>'
           '<ellipse cx="58" cy="34" rx="8" ry="11.5"/>'
           '<ellipse cx="74" cy="45" rx="7.5" ry="10"/>'
           '</g></svg>')

# ---------------------------------------------------------------------------
# AR face-tracking module (TikTok/Instagram-style hair mask via MediaPipe)
# ---------------------------------------------------------------------------
AR_JS = r"""
import { FaceLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22/vision_bundle.mjs";

let lm=null, running=false, raf=null, last=0;

async function ensure(){
  if(lm) return lm;
  const files = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.22/wasm");
  const opts=d=>({ baseOptions:{ modelAssetPath:"https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task", delegate:d }, runningMode:"VIDEO", numFaces:1, outputFaceBlendshapes:false });
  try{ lm = await FaceLandmarker.createFromOptions(files, opts("GPU")); }
  catch(e){ lm = await FaceLandmarker.createFromOptions(files, opts("CPU")); }
  return lm;
}

function place(overlay, pts, video){
  const stage = overlay.parentElement, sr = stage.getBoundingClientRect();
  const vw=video.videoWidth, vh=video.videoHeight;
  if(!vw||!vh) return;
  const scale=Math.max(sr.width/vw, sr.height/vh);
  const dw=vw*scale, dh=vh*scale, ox=(sr.width-dw)/2, oy=(sr.height-dh)/2;
  const P=i=>({ x: ox + (1-pts[i].x)*dw, y: oy + pts[i].y*dh });   // 1-x : video is mirrored
  const top=P(10), chin=P(152), L=P(234), R=P(454), eL=P(33), eR=P(263), fL=P(54), fR=P(284);
  // head width across the temples (a bit wider than cheek width) for a natural cap
  const templeW=Math.hypot(fR.x-fL.x, fR.y-fL.y);
  const faceW=Math.max(Math.hypot(R.x-L.x, R.y-L.y), templeW);
  const faceH=Math.hypot(chin.x-top.x, chin.y-top.y);
  const roll=Math.atan2(eL.y-eR.y, eL.x-eR.x);          // radians (mirrored eyes)
  const mul=(window.__hairMul||1);
  const hairW=faceW*2.12*mul;
  const hairH=hairW/1.2;                                // svg viewBox 120x100
  // hairline point (slightly above forehead landmark 10), centred on forehead
  const hlX=top.x, hlY=top.y - faceH*0.05;
  // the hair path's forehead edge sits ~80% down the svg box → align it to the hairline
  overlay.style.width=hairW+'px';
  overlay.style.height=hairH+'px';
  overlay.style.left=(hlX-hairW/2)+'px';
  overlay.style.top=(hlY-hairH*0.80)+'px';
  overlay.style.transformOrigin='50% 80%';              // pivot at the hairline
  overlay.style.transform='rotate('+(roll*180/Math.PI)+'deg)';
}

window.startGrizzlyCam = async function(video, overlay, onReady, onError){
  try{
    const engine = await ensure();
    running=true; if(onReady) onReady();
    const loop=()=>{
      if(!running) return;
      try{
        if(video.readyState>=2 && video.videoWidth){
          const t=performance.now();
          const res = engine.detectForVideo(video, t);
          if(res && res.faceLandmarks && res.faceLandmarks[0]){
            place(overlay, res.faceLandmarks[0], video);
            overlay.style.opacity='1';
          } else { overlay.style.opacity='.12'; }
        }
      }catch(e){}
      raf=requestAnimationFrame(loop);
    };
    loop();
    return true;
  }catch(e){ if(onError) onError(e); return false; }
};
window.stopGrizzlyCam = function(){ running=false; if(raf) cancelAnimationFrame(raf); };
window.__grizzlyARready = true;
"""

# ---------------------------------------------------------------------------
def w(name, content):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)

def main():
    w("styles.css", CSS)
    w("app.js", APP_JS)
    w("ar.js", AR_JS)
    w("favicon.svg", FAVICON)
    w("translations.js", "window.I18N=" + json.dumps(I18N, ensure_ascii=False) +
      ";\nwindow.GRZ=" + json.dumps(js_data(), ensure_ascii=False) + ";")
    w("index.html", build_index())
    nbarber = 0
    for l in LOCATIONS:
        w(f"lokal-{l['slug']}.html", build_location(l))
        for (nm, role) in l["staff"]:
            w(f"barber-{bslug(l['slug'], nm)}.html", build_barber(l, nm, role))
            nbarber += 1
    print("done —", 1 + len(LOCATIONS) + nbarber, "html pages (", nbarber, "barbers )")

if __name__ == "__main__":
    main()
