import re
import streamlit as st


flu_infos = [
    {
        "流感种类": "甲型流感 / Influenza A",
        "症状": "高热、畏寒、头痛、乏力、咳嗽、流涕、鼻塞、咽痛",
        "症状_en": "fever, chills, headache, fatigue, cough, runny nose, nasal congestion, sore throat",
        "常用药品": "奥司他韦 / Oseltamivir, 扎那米韦 / Zanamivir",
        "剂量范围": "Oseltamivir: 75mg twice daily for 5 days\nZanamivir: 10mg inhaled twice daily for 5 days",
        "注意事项": "儿童、孕妇、老年人慎用 / Caution for children, pregnant women, elderly",
    },
    {
        "流感种类": "乙型流感 / Influenza B",
        "症状": "高热、乏力、咳嗽、流涕、鼻塞、咽痛",
        "症状_en": "fever, fatigue, cough, runny nose, nasal congestion, sore throat",
        "常用药品": "奥司他韦 / Oseltamivir, 扎那米韦 / Zanamivir",
        "剂量范围": "Oseltamivir: 75mg twice daily for 5 days\nZanamivir: 10mg inhaled twice daily for 5 days",
        "注意事项": "注意不良反应 / Watch for side effects",
    },
    {
        "流感种类": "丙型流感 / Influenza C",
        "症状": "咳嗽、流涕、鼻塞、低热",
        "症状_en": "cough, runny nose, nasal congestion, mild fever",
        "常用药品": "对乙酰氨基酚 / Paracetamol (symptomatic)",
        "剂量范围": "Paracetamol: 500–1000mg, 3–4 times/day",
        "注意事项": "避免重复用药 / Avoid overdosing",
    },
    {
        "流感种类": "风寒感冒 / Wind-cold Common Cold",
        "症状": "恶寒重、发热轻、无汗、头痛、肢体酸楚或疼痛，鼻塞声重、打喷嚏、时流清涕、咽痒、咳嗽、痰白稀薄，舌苔薄白，脉浮或浮紧",
        "症状_en": "severe chills, mild fever, no sweating, headache, body soreness or pain, nasal congestion, sneezing, clear nasal discharge, itchy throat, cough with thin white sputum, thin white tongue coating, floating or tight pulse",
        "常用药品": "通宣理肺片（丸） / Tongxuan Lufe Tablets (Pills), 感冒清热颗粒 / Ganmao Qingre Granules",
        "剂量范围": "Tongxuan Lufe Pills: 2 pills twice daily\nTongxuan Lufe Tablets: 6 tablets three times daily\nGanmao Qingre Granules: follow package instructions",
        "注意事项": "儿童、孕妇、老年人慎用 / Caution for children, pregnant women, elderly. Follow instructions carefully and watch for side effects.",
    },
    {
        "流感种类": "风热感冒 / Wind-heat Common Cold",
        "症状": "身热较著、微恶风、汗泄不畅、头胀痛，咽干甚则咽痛、鼻塞、流黄稠涕、咳嗽、痰黏或黄、口干欲饮，舌尖红，舌苔薄白干或薄黄，脉浮数",
        "症状_en": "marked fever, slight aversion to wind, poor sweating, distending headache, dry or sore throat, nasal congestion, thick yellow nasal discharge, cough with sticky or yellow sputum, thirst, red tongue tip, thin white or thin yellow tongue coating, floating rapid pulse",
        "常用药品": "银翘解毒片 / Yin Qiao Jiedu Tablets, 连花清瘟胶囊 / Lianhua Qingwen Capsules",
        "剂量范围": "Yin Qiao Jiedu Tablets: 4-6 tablets twice daily\nLianhua Qingwen Capsules: 4 capsules three times daily",
        "注意事项": "儿童、孕妇、老年人慎用 / Caution for children, pregnant women, elderly. Follow instructions carefully and watch for side effects.",
    },
    {
        "流感种类": "暑湿感冒 / Summer Dampness Cold",
        "症状": "发热、微恶风、身热不扬、汗出不畅、肢体困重或酸痛、头重如裹、胸闷脘痞、纳呆、心烦、大便或溏、小便短赤，鼻塞、流浊涕、口渴，舌苔白腻或黄腻，脉濡数或滑",
        "症状_en": "fever, slight aversion to wind, body feels hot but no obvious heat, poor sweating, heavy or aching limbs, heavy-headed sensation, chest tightness, poor appetite, irritability, loose stool or diarrhea, scanty dark urine, nasal congestion, turbid nasal discharge, thirst, white greasy or yellow greasy tongue coating, soft rapid or slippery pulse",
        "常用药品": "藿香正气水 / Huoxiang Zhengqi Liquid, 暑湿感冒颗粒 / Summer Dampness Cold Granules",
        "剂量范围": "Huoxiang Zhengqi Liquid: 5-10ml twice daily\nSummer Dampness Cold Granules: follow package instructions",
        "注意事项": "儿童、孕妇、老年人慎用 / Caution for children, pregnant women, elderly. Follow instructions carefully and watch for side effects.",
    },
    {
        "流感种类": "普通感冒 / Common Cold",
        "症状": "主要表现为鼻部症状，如喷嚏、鼻塞、流清水样鼻涕，也可表现为咳嗽、咽干、咽痒或烧灼感甚至鼻后滴漏感。随病情进展，鼻涕可变稠，可伴咽痛、头痛、流泪、味觉迟钝、呼吸不畅、声嘶等，有时可由于咽鼓管炎致听力减退。严重者有发热、轻度畏寒和头痛等",
        "症状_en": "sneezing, nasal congestion, clear watery nasal discharge, cough, dry or itchy throat, burning sensation, postnasal drip, thick nasal discharge as disease progresses, sore throat, headache, tearing, dull sense of taste, breathing difficulty, hoarseness, sometimes hearing loss due to eustachian tube inflammation, mild fever, slight chills, headache",
        "常用药品": "复方氨酚烷胺胶囊 / Compound Paracetamol and Amantadine Capsules, 氨酚伪麻美芬片 / Paracetamol Pseudoephedrine Dextromethorphan Tablets",
        "剂量范围": "Compound Paracetamol and Amantadine Capsules: 1 capsule twice daily\nParacetamol Pseudoephedrine Dextromethorphan Tablets: 1-2 tablets three times daily",
        "注意事项": "儿童、孕妇、老年人慎用 / Caution for children, pregnant women, elderly. Follow instructions carefully and watch for side effects.",
    },
    {
        "流感种类": "流行性感冒 / Influenza",
        "症状": "由流感病毒引起的急性呼吸道传染病，具有高度传染性。主要表现为高热、头痛、乏力、肌肉酸痛等症状，可伴或不伴有鼻塞、流涕、咽痛、咳嗽等症状",
        "症状_en": "acute respiratory infection caused by influenza virus, highly contagious, characterized by high fever, headache, fatigue, muscle aches, may also have nasal congestion, runny nose, sore throat, cough",
        "常用药品": "奥司他韦 / Oseltamivir, 连花清瘟胶囊 / Lianhua Qingwen Capsules",
        "剂量范围": "Oseltamivir: 75mg twice daily for 5 days\nLianhua Qingwen Capsules: 4 capsules three times daily",
        "注意事项": "儿童、孕妇、老年人慎用 / Caution for children, pregnant women, elderly. Follow instructions carefully and watch for side effects.",
    },
    {
        "流感种类": "细菌性感冒 / Bacterial Infection Cold",
        "症状": "鼻部症状：出现流浓稠的黄色或绿色鼻涕， 咳嗽咳痰：咳嗽症状持续，痰液通常为黄色、绿色或脓性",
        "症状_en": "nasal symptoms: thick yellow or green nasal discharge; persistent cough with sputum, sputum usually yellow, green, or purulent",
        "常用药品": "阿莫西林 / Amoxicillin, 头孢克洛 / Cefaclor",
        "剂量范围": "Amoxicillin: 0.5g every 6-8 hours (max 4g per day)\nCefaclor: 0.25g three times daily (severe cases can double dose, but max 4g per day)\nChildren: 20-40mg/kg/day divided into 3-4 doses",
        "注意事项": "Avoid alcohol during medication / 禁止饮酒，防止双硫仑样反应；严格按剂量疗程用药 / Strict adherence to dosage and course.",
    },
    {
        "流感种类": "胃肠型感冒 / Gastrointestinal Cold",
        "症状": "以胃肠道症状为主，如频繁的恶心、呕吐、腹痛、腹泻，同时可伴有发热、头痛、乏力等感冒症状",
        "症状_en": "mainly gastrointestinal symptoms such as frequent nausea, vomiting, abdominal pain, diarrhea, accompanied by fever, headache, fatigue",
        "常用药品": "甲氧氯普胺 / Metoclopramide, 双歧杆菌四联活菌片 / Bifidobacterium Quadruple Live Tablets",
        "剂量范围": "Metoclopramide: 5-10mg three times daily\nBifidobacterium Quadruple Live Tablets: 3 tablets three times daily",
        "注意事项": "患病期间饮食要清淡 / Eat light and digestible food during illness, avoid spicy, greasy, irritating food",
    },
    {
        "流感种类": "禽流感 / Avian Influenza",
        "症状": "高热、咳嗽、喉咙痛、肌肉酸痛、呼吸困难",
        "症状_en": "fever, cough, sore throat, muscle aches, breathing difficulties",
        "常用药品": "奥司他韦 / Oseltamivir",
        "剂量范围": "Oseltamivir: 75mg twice daily for 7-10 days",
        "注意事项": "避免与禽类接触 / Avoid contact with birds",
    },
    {
        "流感种类": "猪流感 / Swine Flu (H1N1)",
        "症状": "发热、咳嗽、喉咙痛、鼻塞、身体疼痛、头痛、寒战、疲劳",
        "症状_en": "fever, cough, sore throat, nasal congestion, body aches, headache, chills, fatigue",
        "常用药品": "奥司他韦 / Oseltamivir, 扎那米韦 / Zanamivir",
        "剂量范围": "Same as seasonal flu: 75mg Oseltamivir twice daily for 5 days",
        "注意事项": "勤洗手，避免接触感染者 / Wash hands frequently, avoid infected individuals",
    },
    {
        "流感种类": "季节性流感 / Seasonal Influenza",
        "症状": "高热、咳嗽、喉咙痛、流鼻涕、肌肉酸痛、疲劳",
        "症状_en": "fever, cough, sore throat, runny nose, muscle aches, fatigue",
        "常用药品": "奥司他韦 / Oseltamivir, 扎那米韦 / Zanamivir",
        "剂量范围": "Oseltamivir: 75mg twice daily for 5 days",
        "注意事项": "接种疫苗预防 / Vaccination recommended",
    },
    {
        "流感种类": "流感相关肺炎 / Influenza-related Pneumonia",
        "症状": "咳嗽、呼吸急促、胸痛、发热",
        "症状_en": "cough, shortness of breath, chest pain, fever",
        "常用药品": "抗病毒药物 + 抗生素 / Antiviral drugs + Antibiotics",
        "剂量范围": "根据医生指示使用 / Use as prescribed by doctor",
        "注意事项": "需住院治疗 / Hospitalization may be required",
    },
    {
        "流感种类": "流感脑炎 / Influenza-associated Encephalitis",
        "症状": "高热、头痛、意识障碍、癫痫发作",
        "症状_en": "high fever, headache, altered consciousness, seizures",
        "常用药品": "抗病毒药物 + 支持治疗 / Antiviral drugs + supportive care",
        "剂量范围": "根据病情调整 / Adjust according to condition",
        "注意事项": "立即就医 / Seek medical attention immediately",
    },
    {
        "流感种类": "流感心肌炎 / Influenza-associated Myocarditis",
        "症状": "胸痛、心悸、呼吸急促、疲劳",
        "症状_en": "chest pain, palpitations, shortness of breath, fatigue",
        "常用药品": "抗病毒药物 + 支持治疗 / Antiviral drugs + supportive care",
        "剂量范围": "根据医生建议 / According to doctor's advice",
        "注意事项": "限制活动量，密切观察心脏功能 / Limit activity, monitor heart function closely",
    },
    {
        "流感种类": "新型冠状病毒感染流感样疾病 / COVID-19 Influenza-like Illness",
        "症状": "发热、干咳、乏力、呼吸困难、味觉或嗅觉丧失",
        "症状_en": "fever, dry cough, fatigue, breathing difficulties, loss of taste or smell",
        "常用药品": "无特效药，支持治疗 / No specific antiviral, supportive care",
        "剂量范围": "对症处理 / Symptomatic treatment",
        "注意事项": "隔离治疗，遵循防疫指南 / Isolation and follow public health guidance",
    }
]

# 页面基本设置
st.set_page_config(page_title="流感类型智能查询器 / Flu Type Finder", page_icon="🦠", layout="centered")

# 自定义全局CSS样式（字体、按钮统一、整体间距调整）
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 16px;
    }
    @media (max-width: 768px) {
        html, body, [class*="css"] {
            font-size: 14px;
        }
    }
    @media (min-width: 1600px) {
        html, body, [class*="css"] {
            font-size: 18px;
        }
    }
    /* 按钮统一美化 */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 6px 16px;
        margin: 5px 2px;
        border: none;
        border-radius: 6px;
        font-size: 14px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }
    /* 让查询结果行距更舒服 */
    .stMarkdown {
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🦠 流感类型智能查询器 / Flu Type Finder")
st.markdown("请输入相关病症关键词（支持中英文），点击查询：")

# 搜索函数
def search_flu(symptom):
    symptom = re.sub(r"[^\w\s]", "", symptom.strip().lower())  # 删除标点符号
    result = ""
    found = False
    for flu in flu_infos:
        if re.search(symptom, flu["症状"]) or re.search(symptom, flu["症状_en"], re.IGNORECASE):
            found = True
            result += f"---\n\n"
            result += f"🌿 **流感种类 / Flu Type:** {flu['流感种类']}\n\n"
            result += f"💊 **常用药品 / Medications:** {flu['常用药品']}\n\n"
            result += f"📋 **剂量范围 / Dosage:** {flu['剂量范围']}\n\n"
            result += f"⚠️ **注意事项 / Notes:** {flu['注意事项']}\n\n"
    if not found:
        result = "❌ 未找到匹配项 / No matching flu type found."
    return result

# 输入框
symptom_input = st.text_input("病症关键词 / Symptom Keyword")

# 查询按钮
if st.button("🔍 查询 / Search"):
    if symptom_input:
        st.markdown(search_flu(symptom_input))
    else:
        st.warning("请输入病症关键词 / Please enter a symptom关键词.")

# 快捷常见症状
st.markdown("### 📝 常见症状快捷入口 / Common Symptoms")

col1, col2 = st.columns(2)

with col1:
    st.subheader("中文症状")
    common_symptoms_cn = ["咳嗽", "头痛", "鼻塞", "咽痛", "高热"]
    for sym in common_symptoms_cn:
        if st.button(sym, key=f"cn_{sym}"):
            st.markdown(search_flu(sym))

with col2:
    st.subheader("English Symptoms")
    common_symptoms_en = ["cough", "headache", "sore throat", "fatigue", "runny nose"]
    for sym in common_symptoms_en:
        if st.button(sym, key=f"en_{sym}"):
            st.markdown(search_flu(sym))
