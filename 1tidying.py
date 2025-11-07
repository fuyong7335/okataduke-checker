from PIL import Image
import streamlit as st
import base64

# --- タイプ別リンク ---
TYPE_LINKS = {
    'freeze': 'https://okataduke-freeze.onrender.com',
    'emotion': 'https://okataduke-emotion.onrender.com',
    'burnout': 'https://okataduke-burnout.onrender.com',
    'family': 'https://okataduke-family.onrender.com',
}

# --- ロゴ画像をbase64で埋め込み ---
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded

image_base64 = get_base64_image("logo.jpg")
homepage_url = "https://rakulife.jp/"

st.markdown(
    f"""
    <a href="{homepage_url}" target="_blank">
        <img src="data:image/png;base64,{image_base64}" width="150">
    </a>
    """,
    unsafe_allow_html=True
)

# --- フォント変更 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Serif JP', serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- アプリのタイトル ---
st.title("🧹 おかたづけタイプ診断")
st.write("10問に答えるだけで、あなたの片づけ傾向が分かります！")

# --- タイプ定義 ---
TYPES = {
    'freeze': '思考フリーズタイプ',
    'emotion': '感情ためこみタイプ',
    'burnout': '一気に燃え尽きタイプ',
    'family': '振り回されタイプ'
}

# --- 質問と選択肢 ---
questions = [
    ("Q1. 片づけが進まないとき、どう感じますか？", [
        ("やるべきことが多すぎて動けない", 'freeze'),
        ("昔のものを手にとってしまう", 'emotion'),
        ("一気に片付けて疲れてやめてしまう", 'burnout'),
        ("家族のだれも片づけないのでやる気が出ない", 'family')
    ]),
    ("Q2. 片づけをしようと思ったとき、まず何をしますか？", [
        ("片付け本やSNSを探してしまう", 'freeze'),
        ("懐かしいものを見返してしまう", 'emotion'),
        ("やる気の波が来たときだけ一気にやる", 'burnout'),
        ("ほかのスペースが気になってしまう", 'family')
    ]),
    ("Q3. 収納を考えるとき、どうなりますか？", [
        ("情報を調べすぎて決められない", 'freeze'),
        ("収納すると見えなくなり不安になる", 'emotion'),
        ("とりあえず収納できるものを買って一気にやりたくなる", 'burnout'),
        ("家族のモノが多くてうまくいかない", 'family')
    ]),
    ("Q4. モノを手放すときに感じることは？", [
        ("必要なものか決められない", 'freeze'),
        ("感情が揺れて、なかなか判断できない", 'emotion'),
        ("スパっと決めて捨てたあとに後悔しがち", 'burnout'),
        ("家族のモノは勝手にすてられない", 'family')
    ]),
    ("Q5. 理想の片付け状態は？", [
        ("何がどこにあるかすぐに分かる状態", 'freeze'),
        ("思い出の品も大切にしつつ、すっきりしている", 'emotion'),
        ("掃除がラクで、効率的に保てる状態", 'burnout'),
        ("家族も使いやすく、整理された空間", 'family')
    ]),
    ("Q6. 「片付けなきゃ」と思った時、どう反応しますか？", [
        ("どこから始めればいいのかわからない", 'freeze'),
        ("写真や手紙に目がいって手が止まる", 'emotion'),
        ("気分が乗ったらどんどん進めたくなる", 'burnout'),
        ("だれも片付けない気がして不満になる", 'family')
    ]),
    ("Q7. 片付けたあと、どう感じることが多いですか？", [
        ("ちゃんとできたかなと不安になる", 'freeze'),
        ("思い出を処分したことに罪悪感を感じる", 'emotion'),
        ("達成感よりも、どっと疲れてしまう", 'burnout'),
        ("すぐに家族がちらかしてしまう", 'family')
    ]),
    ("Q8. モノが多くなる原因は？", [
        ("取捨選択が苦手で残してしまう", 'freeze'),
        ("思い出が多すぎて手放せない", 'emotion'),
        ("一気にやろうとして整理が偏る", 'burnout'),
        ("一人の意思で管理できない物が多い", 'family')
    ]),
    ("Q9. 片付けについてよく調査することは？", [
        ("収納アイデアや片付けのコツ", 'freeze'),
        ("捨て方や思い出の整理方法", 'emotion'),
        ("部屋のビフォー＆アフターや時短掃除法", 'burnout'),
        ("家族で片付けられる仕組みづくり", 'family')
    ]),
    ("Q10. あなたの中で片付けのテーマは？", [
        ("決断力をつけること", 'freeze'),
        ("感情と向き合うこと", 'emotion'),
        ("やる気を持続させること", 'burnout'),
        ("家族や人との関係を整えること", 'family')
    ])
]

# --- 回答初期化 ---
scores = {'freeze': 0, 'emotion': 0, 'burnout': 0, 'family': 0}

# --- フォーム表示 ---
with st.form("diagnosis_form"):
    for idx, (question, options) in enumerate(questions):
        answer = st.radio(question, [label for label, _ in options], key=f"q{idx}")
        for label, type_key in options:
            if answer == label:
                scores[type_key] += 1
                break
    submitted = st.form_submit_button("診断する")

# --- 結果表示 ---
if submitted:
    top_type = max(scores, key=scores.get)
    type_label = TYPES[top_type]
    link_url = TYPE_LINKS[top_type]

    st.markdown("## 🔍 診断結果")
    st.markdown(f"あなたは **「{type_label}」** のようです。")
    
    # リンクボタンを使用
    st.link_button("詳しいアドバイスはこちら", link_url)