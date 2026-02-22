import streamlit as st
import time

# --- НАЛАШТУВАННЯ ДИЗАЙНУ (CSS) ---
st.set_page_config(page_title="DESTI", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .header-box {
        background: #e0e5ec; padding: 25px; border-radius: 20px;
        box-shadow: inset 6px 6px 12px #b8b9be, inset -6px -6px 12px #ffffff;
        text-align: center; margin-bottom: 30px;
    }
    .desti-logo { font-size: 18px; letter-spacing: 5px; color: #888; font-weight: 300; margin-bottom: 5px; text-transform: uppercase; }
    
    /* АДАПТАЦІЯ ДЛЯ МОБІЛОК */
    .main-container {
        background: rgba(240, 242, 246, 0.8); 
        padding: 20px; 
        border-radius: 25px;
        box-shadow: 10px 10px 30px #bebebe, -10px -10px 30px #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin: 0 auto;
    }
    
    @media (max-width: 640px) {
        .main-container { padding: 15px; border-radius: 15px; }
        h1 { font-size: 1.5rem !important; }
    }

    .stButton>button {
        border-radius: 15px; border: none; background: #e0e8ec;
        box-shadow: 6px 6px 12px #b8b9be, -6px -6px 12px #ffffff;
        transition: all 0.8s ease; color: #444; font-weight: 600; width: 100%;
        padding: 10px;
    }
    .stButton>button:active { box-shadow: inset 4px 4px 8px #b8b9be, inset -4px -4px 8px #ffffff; transform: scale(0.98); }
    .stTextArea textarea, .stTextInput input {
        border-radius: 15px !important; border: none !important; background: #e0e5ec !important;
        box-shadow: inset 3px 3px 6px #b8b9be, inset -3px -3px 6px #ffffff !important;
    }
    .link-button {
        display: block; text-align: center; padding: 15px 20px; background-color: #e0e5ec;
        color: #444; text-decoration: none; border-radius: 15px;
        box-shadow: 4px 4px 8px #b8b9be, -4px -4px 8px #ffffff;
        font-weight: 600; margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ЛОГІКА АНАЛІЗУ ---
def smart_analyze(text, category_map):
    text = text.lower()
    score = {cat: 0 for cat in category_map.keys()}
    for cat, words in category_map.items():
        for word in words:
            if word in text: score[cat] += 1
    return max(score, key=score.get) if any(score.values()) else "змішаний"

BOOK_MAP = {"аналітичний": ["аналіз", "чому", "структур", "причин", "логіка"], "гуманітарний": ["стиль", "герої", "мова", "емоці"]}
CRISIS_MAP = {"фахівець": ["помилки", "сам", "виправлю"], "лідер": ["команда", "допоможу", "разом"]}

if 'stage' not in st.session_state:
    st.session_state.stage = 'intro'
    st.session_state.data = {}

def slow_type(text, element, speed=0.03):
    full_text = ""
    for char in text:
        full_text += char
        element.markdown(f"<h1 style='text-align: center; color: #2c3e50;'>✨ {full_text} ✨</h1>", unsafe_allow_html=True)
        time.sleep(speed)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- ЕТАПИ ---
if st.session_state.stage == 'intro':
    st.markdown('<div class="header-box">', unsafe_allow_html=True)
    st.markdown('<div class="desti-logo">DESTI</div>', unsafe_allow_html=True)
    placeholder = st.empty()
    slow_type("Хто ти є?", placeholder)
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>готовий спробувати віднайти себе?</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 4, 1]) # Розширив колонку для мобілок
    with col2:
        answer = st.text_input("Введіть відповідь тут (наприклад, 'Готовий'):", key="start_input")
        if answer.lower() == 'готовий':
            st.session_state.stage = 'rules'; st.rerun()

elif st.session_state.stage == 'rules':
    st.subheader("📜 Інструкція досліду")
    st.markdown("""
        Перед початком досліду, прошу ознайомитися із цими мініправилами, щоб все було достатньо чітко:
        
        1. **Ви тут, щоб мати змогу дослідити своє професійне бажання з глибини.** Будьте чесними і не спирайтеся на думку, що "так кажуть краще".
        
        2. **Я надам характеристику, проте рішення лише за вами.** Я тут, щоб направити вас.
        
        3. **Ловіть Трепет.** Відчули драйв до варіанту? Це і є ваш "трепет".
    """)
    if st.button("Поїхали"): st.session_state.stage = 'book_question'; st.rerun()

elif st.session_state.stage == 'book_question':
    st.subheader("📖 Етап 1: Глибина сприйняття")
    ans = st.text_area("Згадайте момент читання книги: аналізуєте приховане чи фокусуєтесь на стилі?")
    if st.button("Далі") and ans:
        st.session_state.data['book_type'] = smart_analyze(ans, BOOK_MAP)
        st.session_state.stage = 'crisis_question'; st.rerun()

elif st.session_state.stage == 'crisis_question':
    st.subheader("🆘 Етап 2: Випробування")
    ans = st.text_area("Дії в кризі: фахові помилки чи допомога іншим?")
    if st.button("Далі") and ans:
        st.session_state.data['crisis_role'] = smart_analyze(ans, CRISIS_MAP)
        st.session_state.stage = 'choice_logic'; st.rerun()

elif st.session_state.stage == 'choice_logic':
    st.subheader("⚙️ Етап 3: Стиль мислення")
    if st.button("Діяти по шаблону"): st.session_state.data['logic_style'] = "шаблон"; st.session_state.stage = 'choice_place'; st.rerun()
    if st.button("Власні погляди та аналіз"): st.session_state.data['logic_style'] = "аналіз"; st.session_state.stage = 'choice_place'; st.rerun()

elif st.session_state.stage == 'choice_place':
    st.subheader("🏠 Етап 4: Формат життя")
    if st.button("Робота в офісі"): st.session_state.data['work_place'] = "офіс"; st.session_state.stage = 'choice_interaction'; st.rerun()
    if st.button("Фріланс"): st.session_state.data['work_place'] = "фріланс"; st.session_state.stage = 'choice_interaction'; st.rerun()

elif st.session_state.stage == 'choice_interaction':
    st.subheader("👥 Етап 5: Взаємодія")
    if st.button("Робота із людьми"): st.session_state.data['interaction'] = "люди"; st.session_state.stage = 'choice_depth'; st.rerun()
    if st.button("Робота із програмами"): st.session_state.data['interaction'] = "програми"; st.session_state.stage = 'choice_depth'; st.rerun()

elif st.session_state.stage == 'choice_depth':
    st.subheader("📉 Етап 6: Глибина процесу")
    if st.button("Аналізувати поверхово"): st.session_state.data['depth'] = "поверхово"; st.session_state.stage = 'trepet_selection'; st.rerun()
    if st.button("Аналізувати чітко та глибоко"): st.session_state.data['depth'] = "чітко та глибоко"; st.session_state.stage = 'trepet_selection'; st.rerun()

elif st.session_state.stage == 'trepet_selection':
    st.subheader("🎯 Вибір сфер")
    options = ["Економіка та фінанси", "Архітектура", "Юриспруденція", "Beauty-індустрія", "IT та Програмування", "Дизайн", "Інженерія", "Медицина та Охорона здоров'я", "Освіта та Викладання"]
    selections = st.multiselect("Оберіть 2-3 сфери:", options)
    if st.button("Зафіксувати вибір") and selections:
        st.session_state.data['selected_spheres'] = selections; st.session_state.stage = 'deep_drill'; st.rerun()

elif st.session_state.stage == 'deep_drill':
    st.subheader("🔍 Перевірка Трепету")
    spheres = st.session_state.data['selected_spheres']
    valid_spheres = []
    with st.form("deep_questions"):
        for s in spheres:
            if s == "Beauty-індустрія":
                q = st.radio("Зробити людину красивішою?", ["Драйв", "Нічого"], index=None)
                if q == "Драйв": valid_spheres.append(s)
            elif s == "IT та Програмування":
                q = st.radio("Годинами писати код?", ["Так", "Ні"], index=None)
                if q == "Так": valid_spheres.append(s)
            elif s == "Юриспруденція":
                q = st.radio("Битися за справедливість?", ["Так", "Ні"], index=None)
                if q == "Так": valid_spheres.append(s)
            elif s == "Економіка та фінанси":
                q = st.radio("Відповідальність за гроші?", ["Так", "Ні"], index=None)
                if q == "Так": valid_spheres.append(s)
            elif s == "Архітектура":
                q = st.radio("Створювати простір для життя?", ["Так", "Ні"], index=None)
                if q == "Так": valid_spheres.append(s)
            elif s == "Дизайн":
                q = st.radio("Виражати ідеї через візуал?", ["Так", "Ні"], index=None)
                if q == "Так": valid_spheres.append(s)
            elif s == "Інженерія":
                q = st.radio("Розбиратися в механізмах?", ["Так", "Ні"], index=None)
                if q == "Так": valid_spheres.append(s)
            elif s == "Медицина та Охорона здоров'я":
                q = st.radio("Відповідальність за здоров'я?", ["Так", "Ні"], index=None)
                if q == "Так": valid_spheres.append(s)
            elif s == "Освіта та Викладання":
                q = st.radio("Пояснювати складне просто?", ["Так", "Ні"], index=None)
                if q == "Так": valid_spheres.append(s)
        
        if st.form_submit_button("Отримати висновок"):
            st.session_state.data['final_results'] = list(set(valid_spheres))
            st.session_state.stage = 'final'; st.rerun()

elif st.session_state.stage == 'final':
    st.balloons()
    st.header("🏁 Твій шлях")
    results = st.session_state.data.get('final_results', [])
    if results:
        for res in results: st.success(f"✅ **{res}**")
        st.write("---")
        if st.button("Так, погнали глибше! 🚀"):
            st.session_state.stage = 'deep_dive_start'; st.rerun()
    else:
        st.warning("Сфери не підтверджено.")
    if st.button("Почати знову"): st.session_state.clear(); st.rerun()

elif st.session_state.stage == 'deep_dive_start':
    st.subheader("🎯 Обери ОДНУ сферу:")
    choice = st.selectbox("Сфера:", st.session_state.data.get('final_results', []))
    if st.button("Аналізувати професії"):
        st.session_state.data['target_sphere'] = choice
        st.session_state.stage = 'profession_selection'; st.rerun()

elif st.session_state.stage == 'profession_selection':
    sphere = st.session_state.data['target_sphere']
    st.subheader(f"🔍 {sphere}")
    
    links = {
        "IT та Програмування": "https://www.indeed.com/career-advice/finding-a-job/it-job-demand",
        "Beauty-індустрія": "https://www.indeed.com/career-advice/finding-a-job/beauty-industry-jobs",
        "Економіка та фінанси": "https://www.indeed.com/career-advice/finding-a-job/top-economics-degree-jobs",
        "Юриспруденція": "https://sg.indeed.com/career-advice/finding-a-job/jobs-in-law",
        "Архітектура": "https://uk.indeed.com/career-advice/finding-a-job/jobs-in-architecture",
        "Дизайн": "https://uk.indeed.com/career-advice/finding-a-job/career-in-designing",
        "Інженерія": "https://www.indeed.com/career-advice/finding-a-job/in-demand-engineering-jobs",
        "Медицина та Охорона здоров'я": "https://www.indeed.com/career-advice/finding-a-job/medical-careers-in-demand",
        "Освіта та Викладання": "https://ie.indeed.com/career-advice/finding-a-job/careers-in-education"
    }

    st.write(f"Ми підібрали найкращі напрямки для сфери **{sphere}**.")
    st.markdown(f'<a href="{links[sphere]}" target="_blank" class="link-button">Переглянути деталі та зарплати ↗️</a>', unsafe_allow_html=True)
    
    if st.button("Завершити"):
        st.session_state.stage = 'final_done'; st.rerun()

elif st.session_state.stage == 'final_done':
    st.success("Глибокий аналіз завершено! ✨")
    if st.button("Почати новий пошук"): st.session_state.clear(); st.rerun()

st.markdown('</div>', unsafe_allow_html=True)