import streamlit as st
import time

# --- НАЛАШТУВАННЯ СТОРІНКИ ---
st.set_page_config(page_title="DESTI", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: ВИДАЛЕННЯ БІЛОГО ХЕДЕРА, НІМБ ТА ЦЕНТРУВАННЯ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');
    
    /* 1. ПРИБИРАЄМО БІЛИЙ ХЕДЕР ТА ЗАЙВІ ЕЛЕМЕНТИ */
    [data-testid="stHeader"], footer, #MainMenu {visibility: hidden; display: none !important;}
    
    /* 2. ЗАГАЛЬНИЙ ФОН ТА ШРИФТ */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Montserrat', sans-serif;
    }

    /* 3. СИМЕТРИЧНЕ ЦЕНТРУВАННЯ РІДНОГО КОНТЕЙНЕРА STREAMLIT */
    .block-container {
        padding-top: 5vh !important; 
        max-width: 800px !important;  
        margin: 0 auto !important;    
        text-align: center !important;
        z-index: 10 !important;       
        position: relative;
    }

    /* 4. ЛОГОТИП DESTI (ФІКСОВАНО ЗЛІВА ЗВЕРХУ) */
    .desti-logo {
        position: fixed; 
        top: 30px; 
        left: 50px;
        font-size: 36px; 
        font-weight: 800; 
        color: #FF00FF;
        text-shadow: 0 0 20px #FF00FF; 
        z-index: 2000;
        letter-spacing: 10px;
    }

    /* 5. МАГІЧНИЙ НІМБ (КУЛЬКА) */
    .orb {
        position: fixed; width: 500px; height: 500px;
        background: radial-gradient(circle, rgba(255, 0, 255, 0.25) 0%, rgba(0,0,0,0) 70%);
        border-radius: 50%; 
        z-index: 1; 
        transition: all 1.8s cubic-bezier(0.4, 0, 0.2, 1);
        filter: blur(50px);
        pointer-events: none;
    }

    /* 6. КНОПКИ (МИТТЄВЕ ЗНИКНЕННЯ) */
    [data-testid="stButton"] {
        display: flex;
        justify-content: center;
        width: 100%;
        transition: none !important;
    }
    .stButton>button {
        background: linear-gradient(145deg, #FF00FF, #8B008B) !important;
        color: white !important; border: none !important; 
        padding: 18px 30px !important; border-radius: 20px !important; 
        font-size: 18px !important; font-weight: 600 !important;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.4) !important;
        transition: none !important; 
        width: 100% !important; 
        margin-top: 15px !important; line-height: 1.4 !important;
    }
    .stButton>button:hover { 
        transform: scale(1.03) !important; 
        box-shadow: 0 0 30px #FF00FF !important; 
    }

    /* 7. ТЕКСТОВІ БЛОКИ */
    h1, h2, h3, p { text-align: center !important; position: relative; z-index: 10; width: 100%; }
    .typewriter-box { font-size: 22px; line-height: 1.6; margin-bottom: 20px; z-index: 10; position: relative; text-align: center !important; }
    .feedback-box { color: #FFB6C1; font-style: italic; margin-bottom: 25px; font-size: 19px; text-align: center !important; }

    /* 8. ФІНАЛЬНА РАМКА РЕЗУЛЬТАТІВ */
    .final-frame {
        border: 2px solid #FF00FF; padding: 40px; border-radius: 35px;
        background: rgba(255, 0, 255, 0.05); box-shadow: 0 0 40px rgba(255, 0, 255, 0.25);
        margin: 0 auto;
    }

    /* --- МОБІЛЬНА АДАПТАЦІЯ (MOBILE OPTIMIZATION) --- */
    @media (max-width: 768px) {
        .desti-logo {
            font-size: 24px;
            top: 15px;
            left: 20px;
            letter-spacing: 5px;
        }
        h1 {
            font-size: 45px !important; /* Зменшуємо гігантський текст на телефонах */
            padding-top: 80px !important;
        }
        .typewriter-box, p {
            font-size: 18px !important;
        }
        .orb {
            width: 300px;
            height: 300px;
        }
        .final-frame {
            padding: 20px;
        }
        /* Змушуємо колонки з результатами йти одна під одною */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- ЛОГІКА СТАНІВ ТА ПАМ'ЯТЬ ДЛЯ ТЕКСТУ ---
if 'step' not in st.session_state:
    st.session_state.step = 'welcome'
    st.session_state.typed_texts = [] 
    st.session_state.scores = {
        "IT": 0, "Engineering": 0, "Economics": 0, "Law": 0,
        "Design": 0, "Medicine": 0, "Management": 0, "Education": 0
    }
    st.session_state.feedback = ""

# --- ТАЙПРАЙТЕР ---
def typewriter(text, step_key):
    if step_key not in st.session_state.typed_texts:
        placeholder = st.empty()
        full_text = ""
        for char in text:
            full_text += char
            placeholder.markdown(f"<div class='typewriter-box'>{full_text}</div>", unsafe_allow_html=True)
            time.sleep(0.01)
        st.session_state.typed_texts.append(step_key)
    else:
        st.markdown(f"<div class='typewriter-box'>{text}</div>", unsafe_allow_html=True)

# --- КЕРУВАННЯ НІМБОМ ---
orb_pos = {
    'welcome': "top: 10%; left: 10%;",
    'background': "top: -10%; left: 60%;",
    'q1': "top: 50%; left: -10%;",
    'q1_f': "top: 30%; left: 30%;",
    'q2': "top: 60%; left: 70%;",
    'bridge': "top: 20%; left: 10%;",
    'filter': "top: 40%; left: 40%;",
    'final': "top: 0%; left: 0%; width: 100%; height: 100%; border-radius: 0%; opacity: 0.4;"
}
pos = orb_pos.get(st.session_state.step, "top: 40%; left: 40%;")
st.markdown(f'<div class="orb" style="{pos}"></div>', unsafe_allow_html=True)
st.markdown('<div class="desti-logo">DESTI</div>', unsafe_allow_html=True)

# --- ЕКРАНИ ТА АЛГОРИТМ ---
main_container = st.empty() 

with main_container.container():
    if st.session_state.step == 'welcome':
        st.markdown("<h1 style='font-size: 85px; margin-bottom: 0; padding-top:115px;'>ХТО ТИ Є?</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 22px; opacity: 0.7; margin-bottom: 30px;'>Твій шлях починається тут</p>", unsafe_allow_html=True)
        if st.button("ГОТОВИЙ"):
            main_container.empty() 
            st.session_state.step = 'background'
            st.rerun()

    elif st.session_state.step == 'background':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        typewriter("Уяви, що ти є постійним учасником молодіжного клубу. Зараз він розширює свої повноваження, тому проєктів достатньо як і роботи. Тому твоє завдання відповідати на наступні запитання чесно та відверто, не через 'треба', а через 'хочу'. Домовились?", "bg_text")
        if st.button("LET'S GO"):
            main_container.empty() 
            st.session_state.step = 'q1'
            st.rerun()

    elif st.session_state.step == 'q1':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown("### 1. Ситуація: Проєкт у Молодіжному центрі на межі провалу через серйозну помилку. Всі в паніці. Поки команда не знає, що робити, ти інтуїтивно обираєш свою роль:")
        if st.button("А: 'Заспокойтеся, все вирішимо!' — беру на себе емоційний стан команди та розхвильованих організаторів."):
            main_container.empty() 
            st.session_state.scores["Management"] += 22.5; st.session_state.scores["Education"] += 22.5
            st.session_state.feedback = "О, ти — той самий 'соціальний клей', на якому тримається будь-яка команда. Поки всі бігають по стелі, ти тримаєш штурвал емоцій."
            st.session_state.step = 'q1_f'
            st.rerun()
        if st.button("Б: 'Десь тут є логічна дірка...' — сідаю перевіряти розрахунки та шукати технічну помилку."):
            main_container.empty() 
            st.session_state.scores["IT"] += 11.25; st.session_state.scores["Economics"] += 11.25; st.session_state.scores["Engineering"] += 11.25
            st.session_state.feedback = "Холодний розум у вогні — це потужно. Поки інші панікують, ти вже вмикаєш Систему 2 і шукаєш баг."
            st.session_state.step = 'q1_f'
            st.rerun()
        if st.button("В: 'Не зупиняємось, є інший шлях!' — генерую нові ідеї, щоб проєкт продовжував жити попри факап."):
            main_container.empty() 
            st.session_state.scores["Design"] += 22.5
            st.session_state.feedback = "Круто! Ти не даєш обставинам поставити крапку. Твій мозок одразу шукає 'План Б' та 'План В'."
            st.session_state.step = 'q1_f'
            st.rerun()

    elif st.session_state.step == 'q1_f':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        typewriter(st.session_state.feedback, "q1_f_text")
        if st.button("ДАЛІ"):
            main_container.empty()
            st.session_state.step = 'q2'
            st.rerun()

    elif st.session_state.step == 'q2':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown("### 2. Після школи перед тобою два шляхи. Який обереш?")
        if st.button("А: Ризикнути і почати щось своє, де немає гарантій, але є свобода."):
            main_container.empty() 
            st.session_state.scores["Management"] += 22.5; st.session_state.scores["Design"] += 11.25
            st.session_state.step = 'bridge'
            st.rerun()
        if st.button("Б: Стати крутим профі у перевіреній сфері, де цінують стабільність та експертність."):
            main_container.empty() 
            st.session_state.scores["Law"] += 22.5; st.session_state.scores["Economics"] += 22.5; st.session_state.scores["Medicine"] += 11.25
            st.session_state.step = 'bridge'
            st.rerun()

    elif st.session_state.step == 'bridge':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        typewriter("Я знаю, ти думаєш, що я не маю таке запитувати, але це справді важливо для аналізу твоїх світоглядів, тому спробуй...", "bridge_text")
        if st.button("ДО ГОЛОВНОЇ ЧАСТИНИ"):
            main_container.empty()
            st.session_state.step = 'filter'
            st.rerun()

    elif st.session_state.step == 'filter':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown("### 3. Повертаємося до Центру: у вас знову проєкт. Тобі пропонують роль, але ти можеш її змінити. Що ближче?")
        if st.button("А: Створювати структуру для публікацій — розробляти логіку процесу."):
            main_container.empty() 
            st.session_state.scores["IT"] += 25
            st.session_state.feedback = "О, бачу системний підхід! Ти з тих, хто спочатку розбереться в деталях. Ідемо будувати цифрові світи?"
            st.session_state.step = 'branch_tech'
            st.rerun()
        if st.button("Б: Думати над ресурсами: що принесе проєкт та які прорахунки потрібні."):
            main_container.empty() 
            st.session_state.scores["Economics"] += 12.5
            st.session_state.feedback = "О, бачу системний підхід! Але давай уточнимо координати..."
            st.session_state.step = 'branch_analysis'
            st.rerun()
        if st.button("В: Зосередитися на атмосфері, візуалі та тому, як люди відчують цей проєкт."):
            main_container.empty() 
            st.session_state.scores["Design"] += 25
            st.session_state.feedback = "Твій вибір — про душу проєкту. Подивимося, як твоя творчість працює з людьми!"
            st.session_state.step = 'branch_creative'
            st.rerun()

    elif st.session_state.step == 'branch_tech':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='feedback-box'>{st.session_state.feedback}</div>", unsafe_allow_html=True)
        st.markdown("### Готовий до напруги без рожевих окулярів?")
        if st.button("ТАК: Природничі науки / Лабораторії"):
            main_container.empty(); st.session_state.step = 'bio_filter'; st.rerun()
        if st.button("НІ: Тільки цифри та код"):
            main_container.empty(); st.session_state.scores["IT"] += 25; st.session_state.step = 'library'; st.rerun()

    elif st.session_state.step == 'bio_filter':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown("### Ти бачиш себе саме в оточенні мікроскопів/пробірок на постійній основі?")
        if st.button("ТАК, живі системи — це моє"):
            main_container.empty(); st.session_state.scores["Medicine"] += 25; st.session_state.step = 'library'; st.rerun()
        if st.button("НІ, я б краще конструював/ла механізми"):
            main_container.empty(); st.session_state.scores["Engineering"] += 25; st.session_state.step = 'library'; st.rerun()

    elif st.session_state.step == 'branch_analysis':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='feedback-box'>{st.session_state.feedback}</div>", unsafe_allow_html=True)
        if st.button("Слідкувати за деталями та поведінкою людей, щоб осягнути їх наміри?"):
            main_container.empty(); st.session_state.scores["Law"] += 25; st.session_state.step = 'library'; st.rerun()
        if st.button("Проводити аналізи з математикою для підтвердження своїх слів?"):
            main_container.empty(); st.session_state.scores["Economics"] += 25; st.session_state.step = 'library'; st.rerun()
        if st.button("Вивчати зовнішні риси людини, щоб підкреслити її унікальність?"):
            main_container.empty(); st.session_state.scores["Design"] += 25; st.session_state.step = 'library'; st.rerun()

    elif st.session_state.step == 'branch_creative':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown("### З'явився момент підготовки до свята обдарованих дітей і організатори захотіли змін та удосконалень до нього. Знову перед вами вибір:")
        if st.button("Реорганізовувати саму програму і сценарій"):
            main_container.empty(); st.session_state.scores["Management"] += 25; st.session_state.step = 'ai_kids'; st.rerun()
        if st.button("Більше змінювати інтер'єр щоб він був більш привабливий для молоді"):
            main_container.empty(); st.session_state.scores["Design"] += 25; st.session_state.step = 'ai_kids'; st.rerun()

    elif st.session_state.step == 'ai_kids':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown("### Вам запропонували сформувати доступні пояснення на тему про 'Вплив ШІ на наше життя і загалом що це' і сказали що ви і будете це пояснювати їм.")
        if st.button("Взяли б таку вдповідальність, бо дітям треба було саме роз'яснити щоб вони це осягнули"):
            main_container.empty(); st.session_state.scores["Education"] += 25; st.session_state.step = 'library'; st.rerun()
        if st.button(" Не дуже горю бажанням до такої взаємодії саме на постійній основі, бо проєкт мав бути довгостроковий"):
            main_container.empty(); st.session_state.scores["Education"] += 12.5; st.session_state.scores["Law"] += 12.5; st.session_state.step = 'library'; st.rerun()

    elif st.session_state.step == 'library':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown("### Останнє. Ти в старій бібліотеці. Що забереш із собою?")
        if st.button("Стара книга (Досвід поколінь)."):
            main_container.empty(); st.session_state.profile = "Експертність та Глибина."; st.session_state.step = 'final'; st.rerun()
        if st.button("Порожній блокнот (Творення свого)."):
            main_container.empty(); st.session_state.profile = "Інновації та Свій шлях."; st.session_state.step = 'final'; st.rerun()

    elif st.session_state.step == 'final':
        st.markdown("<div style='padding-top:115px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='final-frame'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:#FF00FF; font-size:45px;'>РЕЗУЛЬТАТИ DESTI</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3>{st.session_state.profile}</h3>", unsafe_allow_html=True)
        
        links = {"IT": "https://www.indeed.com/career-advice/finding-a-job/it-job-demand", "Economics": "https://www.indeed.com/career-advice/finding-a-job/top-economics-degree-jobs", "Law": "https://sg.indeed.com/career-advice/finding-a-job/jobs-in-law", "Design": "https://uk.indeed.com/career-advice/finding-a-job/career-in-designing", "Engineering": "https://www.indeed.com/career-advice/finding-a-job/in-demand-engineering-jobs", "Medicine": "https://www.indeed.com/career-advice/finding-a-job/medical-careers-in-demand", "Management": "https://www.indeed.com/career-advice/finding-a-job/it-job-demand", "Education": "https://ie.indeed.com/career-advice/finding-a-job/careers-in-education"}

        res = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
        col1, col2 = st.columns(2)
        for i, (name, score) in enumerate(res[:4]):
            perc = min(int((score/95)*100), 100)
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"<div style='color:#FF00FF; font-size:30px; font-weight:800; margin-top:20px;'>{name}</div>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='margin:0; font-size:40px;'>{perc}%</h2>", unsafe_allow_html=True)
                st.markdown(f"<a href='{links.get(name)}' style='color:#FF00FF;'>Переглянути вакансії</a>", unsafe_allow_html=True)

        if st.button("ПЕРЕЗАПУСТИТИ"): 
            st.session_state.step = 'welcome'; st.session_state.typed_texts = []; main_container.empty(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
