# -*- coding: utf-8 -*-
"""
Grizzly Barber Shop — static multi-location site generator (feature-rich).
Edit the data below, then run:  python3 build.py
Preview:  python3 -m http.server 8790
"""
import json, os, re, glob, html
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
VER = "3"  # cache-bust; bump after CSS/JS changes

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
  "nav_lokale":"Lokale","nav_uslugi":"Cennik","nav_kalk":"Kalkulator","nav_onas":"O nas",
  "nav_opinie":"Opinie","nav_galeria":"Galeria","nav_faq":"FAQ","nav_kontakt":"Kontakt","btn_book":"Rezerwuj",
  "promo_text":"Program lojalnościowy — zbieraj wizyty i łap rabaty w każdym lokalu.","promo_cta":"Rezerwuj",
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
  "faq4q":"Macie program lojalnościowy?","faq4a":"Tak, zbierasz wizyty i łapiesz rabaty. Zapytaj swojego barbera.",
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
  "nav_lokale":"Локації","nav_uslugi":"Прайс","nav_kalk":"Калькулятор","nav_onas":"Про нас",
  "nav_opinie":"Відгуки","nav_galeria":"Галерея","nav_faq":"FAQ","nav_kontakt":"Контакти","btn_book":"Записатись",
  "promo_text":"Програма лояльності — збирай візити й лови знижки в кожній локації.","promo_cta":"Записатись",
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
  "faq4q":"Є програма лояльності?","faq4a":"Так, збираєш візити й ловиш знижки. Запитай свого барбера.",
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
  "nav_lokale":"Локации","nav_uslugi":"Прайс","nav_kalk":"Калькулятор","nav_onas":"О нас",
  "nav_opinie":"Отзывы","nav_galeria":"Галерея","nav_faq":"FAQ","nav_kontakt":"Контакты","btn_book":"Записаться",
  "promo_text":"Программа лояльности — копи визиты и лови скидки в каждой локации.","promo_cta":"Записаться",
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
  "faq4q":"Есть программа лояльности?","faq4a":"Да, копишь визиты и ловишь скидки. Спроси своего барбера.",
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
  "nav_lokale":"Locations","nav_uslugi":"Prices","nav_kalk":"Calculator","nav_onas":"About",
  "nav_opinie":"Reviews","nav_galeria":"Gallery","nav_faq":"FAQ","nav_kontakt":"Contact","btn_book":"Book now",
  "promo_text":"Loyalty program — collect visits and unlock discounts at every shop.","promo_cta":"Book now",
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
  "faq4q":"Do you have a loyalty program?","faq4a":"Yes, collect visits and unlock discounts. Ask your barber.",
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
<link rel="icon" href="{rel}favicon.svg">
</head>
<body>
<script>var r=document.documentElement;r.classList.remove('no-js');r.classList.add('js');try{{var th=localStorage.getItem('grz_theme');if(th)r.setAttribute('data-theme',th);}}catch(e){{}}</script>
<div id="progress"></div>
"""

def _nav_links(rel, keys):
    return "".join(f'<a href="{rel}index.html#{sec}">{t(key)}</a>' for sec, key in keys)

def header(rel=""):
    top = [("lokale","nav_lokale"),("uslugi","nav_uslugi"),("opinie","nav_opinie"),
           ("galeria","nav_galeria"),("kontakt","nav_kontakt")]
    full = [("lokale","nav_lokale"),("uslugi","nav_uslugi"),("kalkulator","nav_kalk"),
            ("opinie","nav_opinie"),("galeria","nav_galeria"),("faq","nav_faq"),("kontakt","nav_kontakt")]
    return f"""<header class="site-head">
<div class="wrap head-in">
  <a class="brand" href="{rel}index.html">{PAW}<span class="brand-word">GRIZZLY</span></a>
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
    <a class="brand" href="{rel}index.html">{PAW}<span class="brand-word">GRIZZLY</span></a>
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

# ---------------------------------------------------------------------------
# INDEX
# ---------------------------------------------------------------------------
def location_card(l):
    if l["rating"]:
        meta = f'<span class="lc-rate"><span class="stars">★</span> <b>{esc(l["rating"])}</b> · {esc(l["reviews"])} {t("reviews_word")}</span>'
    else:
        meta = f'<span class="lc-rate lc-new">{t("new_loc")}</span>'
    flag = '<span class="lc-flag">★</span>' if l["flagship"] else ""
    return f"""<a class="loc-card reveal" data-slug="{l['slug']}" href="lokal-{l['slug']}.html">
  {flag}{open_badge(l['slug'])}
  <h3>{esc(l['short'])}</h3>
  <p class="lc-addr">{esc(l['address'])}</p>
  {meta}
  <span class="lc-dist" data-dist="{l['slug']}"></span>
  <span class="lc-go">{t('view_loc')} →</span>
</a>"""

def svc_chip(s):
    n, p, tm = s
    return f'<div class="svc"><div class="svc-name">{esc(n)}</div><div class="svc-meta"><span class="svc-price">{esc(p)}</span><span class="svc-time">{esc(tm)}</span></div></div>'

def build_index():
    cards = "".join(location_card(l) for l in LOCATIONS)
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
  <div class="hero-bg"></div>
  <div class="wrap hero-in">
    <p class="kicker" data-i18n="hero_kicker">{ta('hero_kicker')}</p>
    <h1 class="hero-title">GRIZZLY BARBER SHOP</h1>
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

<section id="lokale" class="sec">
  <div class="wrap">
    <div class="sec-head reveal"><h2 data-i18n="lokale_title">{ta('lokale_title')}</h2><p data-i18n="lokale_sub">{ta('lokale_sub')}</p></div>
    <div class="loc-grid">{cards}</div>
  </div>
</section>

<section id="uslugi" class="sec sec-alt">
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

<section id="o-nas" class="sec sec-alt">
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
    <div class="onas-emblem reveal">{PAW}</div>
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

<section id="kontakt" class="sec sec-alt">
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
        cards = "".join(
            f'<div class="tm-card reveal"><div class="tm-ava">{PAW}</div><h4>{esc(nm)}</h4><span>{esc(role)}</span></div>'
            for (nm, role) in l["staff"])
        team = f"""<section class="sec sec-alt"><div class="wrap">
  <div class="sec-head reveal"><h2 data-i18n="loc_team_title">{ta('loc_team_title')}</h2></div>
  <div class="team-grid">{cards}</div></div></section>"""
    rate = f'<span class="lh-rate"><span class="stars">★</span> <b>{esc(l["rating"])}</b> · {esc(l["reviews"])} {t("reviews_word")}</span>' if l["rating"] else ""
    phone_row = f'<div class="ib"><span data-i18n="phone_label">{ta("phone_label")}</span><a href="{esc(l["book_url"])}">{esc(l["phone"])}</a></div>' if l["phone"] else ""
    # sibling locations strip
    others = "".join(
        f'<a href="lokal-{o["slug"]}.html">{esc(o["short"])}</a>'
        for o in LOCATIONS if o["slug"] != l["slug"])

    body = f"""{header()}
<main>
<section class="loc-hero">
  <div class="hero-bg"></div>
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
# CSS
# ---------------------------------------------------------------------------
CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#12100d; --panel:#1b1712; --panel2:#221d17; --ink:#f3ede1; --mut:#a99e8c;
  --amber:#d08c2c; --amber2:#f0a63a; --line:rgba(210,180,120,.14); --maxw:1160px;
  --card:#1b1712; --shadow:rgba(0,0,0,.7);
}
html[data-theme="light"]{
  --bg:#f4efe6; --panel:#fbf7ef; --panel2:#efe7d8; --ink:#20180e; --mut:#6f6353;
  --amber:#b6741c; --amber2:#c8892f; --line:rgba(120,90,40,.18); --card:#fbf7ef; --shadow:rgba(120,90,40,.18);
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
.btn-amber{background:linear-gradient(135deg,var(--amber2),var(--amber));color:#1a1408;box-shadow:0 6px 22px -8px rgba(208,140,44,.6)}
.btn-amber:hover{filter:brightness(1.08);transform:translateY(-1px)}
.btn-ghost{border-color:var(--line);color:var(--ink);background:transparent}
.btn-ghost:hover{border-color:var(--amber);color:var(--amber2)}
.paw{width:34px;height:34px;fill:var(--amber2);filter:drop-shadow(0 2px 6px rgba(208,140,44,.35));flex:none}

/* promo ribbon */
.promo{background:linear-gradient(135deg,var(--amber),var(--amber2));color:#1a1408}
.promo.hide{display:none}
.promo-in{display:flex;align-items:center;gap:14px;padding:9px 22px;font-family:'Barlow Condensed';font-weight:600;font-size:.98rem}
.promo-cta{margin-left:auto;background:#1a1408;color:var(--amber2);border:none;padding:6px 14px;border-radius:2px;font-family:'Barlow Condensed';font-weight:600;text-transform:uppercase;letter-spacing:.05em;cursor:pointer}
.promo-x{background:none;border:none;color:#1a1408;font-size:1.3rem;cursor:pointer;line-height:1}

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
.hero,.loc-hero{position:relative;overflow:hidden;padding:118px 0 84px;text-align:center}
.loc-hero{padding:92px 0 56px}
.hero-bg{position:absolute;inset:0;z-index:0;
  background:radial-gradient(ellipse 60% 55% at 50% 0%,rgba(208,140,44,.16),transparent 70%),
    radial-gradient(ellipse 90% 60% at 50% 120%,rgba(0,0,0,.55),transparent),
    repeating-linear-gradient(115deg,rgba(255,255,255,.014) 0 2px,transparent 2px 9px)}
html[data-theme="light"] .hero-bg{background:radial-gradient(ellipse 60% 55% at 50% 0%,rgba(200,137,47,.18),transparent 70%),repeating-linear-gradient(115deg,rgba(120,90,40,.03) 0 2px,transparent 2px 9px)}
.hero-in,.loc-hero-in{position:relative;z-index:1}
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
.sec-head{text-align:center;max-width:640px;margin:0 auto 42px}
.sec-head h2{font-size:clamp(2rem,5vw,3rem);text-transform:uppercase}
.sec-head p{color:var(--mut);margin-top:12px;font-size:1.08rem}

/* location grid */
.loc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.loc-card{position:relative;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:30px 26px;transition:.2s;overflow:hidden}
.sec-alt .loc-card{background:var(--panel2)}
.loc-card:hover{border-color:var(--amber);transform:translateY(-4px);box-shadow:0 18px 40px -20px var(--shadow)}
.loc-card.near{border-color:var(--amber2);box-shadow:0 0 0 1px var(--amber2)}
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
.onas-emblem .paw{width:min(260px,60vw);height:auto;opacity:.9}

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
.masonry img{width:100%;border-radius:5px;margin-bottom:12px;cursor:zoom-in;transition:.2s}
.masonry img:hover{filter:brightness(1.1)}
.gallery-empty{border:1.5px dashed var(--line);border-radius:8px;padding:52px 24px;text-align:center;background:var(--card)}
.gallery-empty p{color:var(--mut);font-size:1.1rem;margin-bottom:20px}
.ge-btns{display:flex;gap:12px;justify-content:center}

/* before/after */
.ba-wrap{max-width:720px;margin:44px auto 0;text-align:center}
.ba-title{text-transform:uppercase;font-size:1.5rem;margin-bottom:16px}
.ba{position:relative;width:100%;aspect-ratio:16/9;border-radius:8px;overflow:hidden;border:1px solid var(--line);user-select:none}
.ba-after{position:absolute;inset:0;background:linear-gradient(135deg,#2b2118,#4a3826 60%,#6a5236)}
.ba-before{position:absolute;inset:0;width:50%;overflow:hidden;background:linear-gradient(135deg,#1a1712,#2a251d 60%,#3a342a)}
.ba-before::after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(45deg,rgba(0,0,0,.25) 0 6px,transparent 6px 12px)}
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
.tm-card{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:24px 16px;text-align:center}
.tm-ava{width:78px;height:78px;margin:0 auto 14px;border-radius:50%;background:radial-gradient(circle at 40% 30%,var(--panel2),#0d0b08);display:flex;align-items:center;justify-content:center;border:1px solid var(--line)}
.tm-ava .paw{width:40px;height:40px}
.tm-card h4{font-size:1.25rem;text-transform:uppercase}
.tm-card span{color:var(--amber2);font-size:.82rem;text-transform:uppercase;letter-spacing:.08em}
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

@media(max-width:980px){.masonry{columns:2}}
@media(max-width:860px){
  .onas{grid-template-columns:1fr}.onas-emblem{order:-1}
  .contact-wrap{grid-template-columns:1fr}.ct-map iframe{min-height:320px}
  .values{grid-template-columns:1fr}
}
@media(max-width:940px){
  .nav{display:none}.head-cta{display:none}.burger{display:flex}
}
@media(max-width:760px){
  .drawer{display:block;max-height:0;overflow:hidden;transition:max-height .3s;background:var(--panel);border-bottom:1px solid var(--line)}
  .drawer.open{max-height:520px}
  .drawer nav{display:flex;flex-direction:column;gap:2px;padding:14px 22px}
  .drawer nav a{padding:12px 0;text-transform:uppercase;font-family:'Barlow Condensed';font-weight:600;color:var(--ink);border-bottom:1px solid var(--line)}
  .drawer .btn{margin-top:12px;justify-content:center}
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
  var nav=(navigator.language||'pl').slice(0,2);
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
  if(baR){function baSet(v){baB.style.width=v+'%';baH.style.left=v+'%';}
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

  /* ---------- init ---------- */
  var start=saved||({pl:'pl',uk:'uk',ru:'ru',en:'en'}[nav]||'pl');
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
def w(name, content):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)

def main():
    w("styles.css", CSS)
    w("app.js", APP_JS)
    w("favicon.svg", FAVICON)
    w("translations.js", "window.I18N=" + json.dumps(I18N, ensure_ascii=False) +
      ";\nwindow.GRZ=" + json.dumps(js_data(), ensure_ascii=False) + ";")
    w("index.html", build_index())
    for l in LOCATIONS:
        w(f"lokal-{l['slug']}.html", build_location(l))
    print("done —", 1 + len(LOCATIONS), "html pages")

if __name__ == "__main__":
    main()
