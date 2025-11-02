from PIL import Image
import streamlit as st
import base64

# タイプ別リンク（仮リンク → 後でリザストLPに差し替え）
TYPE_LINKS = {
    'freeze': 'https://example.com/freeze',
    'emotion': 'https://example.com/emotion',
    'burnout': 'https://example.com/burnout',
    'family': 'https://example.com/family'
}

# 画像をbase64に変換してHTMLに埋め込む
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded

# ロゴ画像とリンク
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

# フォント変更（明朝系）
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Serif JP', serif;
    }
    </style>
""", unsafe_allow_html=True)

# アプリタイトルと説明
st.title("🧹 おかたづけタイプ診断")
st.write("10問に答えるだけで、あなたの片づけ傾向が分かります！")

# タイプ分類
TYPES = {
    'freeze': '思考フリーズタイプ',
    'emotion': '感情ためこみタイプ',
    'burnout': '一気に燃え尽きタイプ',
    'family': '散らかされタイプ'
}

# 質問と選択肢
questions = [
    ("Q1. 片づけが進まないとき、どう感じますか？", [
        ("やるべきことが多すぎて動けない", 'freeze'),
        ("昔のものを手に取ると手が止まってしまう", 'emotion'),
        ("一気に片付けて疲れてやめてしまう", 'burnout'),
        ("誰かが散らかしていてやる気が出ない", 'family')
    ]),
    ("Q2. 片づけをしようと思ったとき、まず何をしますか？", [
        ("片付け本やSNSを探してしまう", 'freeze'),
        ("懐かしいものを見返してしまう", 'emotion'),
        ("やる気の波が来たときだけ一気にやる", 'burnout'),
        ("自分のスペース以外が気になってしまう", 'family')
    ]),
    ("Q3. 収納を考えるとき、どうなりますか？", [
        ("情報を調べすぎて決められない", 'freeze'),
        ("収納すると見えなくなりそうで不安になる", 'emotion'),
        ("とりあえず買って一気に整えたくなる", 'burnout'),
        ("家族のモノが多くてうまくいかない", 'family')
    ]),
    ("Q4. モノを手放すときに感じることは？", [
        ("本当に必要ないのか自信が持てない", 'freeze'),
        ("感情が揺れて、なかなか判断できない", 'emotion'),
        ("思いきって捨てたあとに後悔しがち", 'burnout'),
        ("他人のモノは勝手に触れないので進まない", 'family')
    ]),
    ("Q5. 理想の片付け状態は？", [
        ("何がどこにあるかすぐに分かる状態", 'freeze'),
        ("思い出の品も大切にしつつ、すっきりしている", 'emotion'),
        ("掃除がラクで、効率的に保てる状態", 'burnout'),
        ("家族も使いやすく、散らかりにくい空間", 'family')
    ]),
    ("Q6. 「片付けなきゃ」と思った時、どう反応しますか？", [
        ("どこから始めればいいか分からず止まる", 'freeze'),
        ("写真や手紙に目がいって手が止まる", 'emotion'),
        ("気分が乗ったらどんどん進めたくなる", 'burnout'),
        ("自分ばかり片付けている気がして不満になる", 'family')
    ]),
    ("Q7. 片付けたあと、どう感じることが多いですか？", [
        ("もっとやるべきだったかもと不安になる", 'freeze'),
        ("思い出を処分したことに罪悪感を感じる", 'emotion'),
        ("達成感よりも、どっと疲れてしまう", 'burnout'),
        ("すぐに家族がまた散らかしてしまう", 'family')
    ]),
    ("Q8. モノが多くなる原因は？", [
        ("取捨選択が苦手で残してしまう", 'freeze'),
        ("思い出が多すぎて手放せない", 'emotion'),
        ("一気にやろうとして整理が偏る", 'burnout'),
        ("自分の意思で管理できない物が多い", 'family')
    ]),
    ("Q9. 片付けについてよく調べることは？", [
        ("収納アイデアや片付けのコツ", 'freeze'),
        ("捨て方や思い出の整理方法", 'emotion'),
        ("ビフォーアフター写真や時短掃除法", 'burnout'),
        ("家族が散らかさない仕組みづくり", 'family')
    ]),
    ("Q10. あなたの中で片付けのテーマは？", [
        ("決断力をつけること", 'freeze'),
        ("感情と向き合うこと", 'emotion'),
        ("やる気を持続させること", 'burnout'),
        ("家族や人との関係を整えること", 'family')
    ])
]

# 回答カウント初期化
scores = {'freeze': 0, 'emotion': 0, 'burnout': 0, 'family': 0}

# 診断フォーム
with st.form("diagnosis_form"):
    for idx, (question, options) in enumerate(questions):
        items = [label for label, _ in options]
        answer = st.radio(question, items, key=f"q{idx}")
        for label, type_key in options:
            if answer == label:
                scores[type_key] += 1
                break
    submitted = st.form_submit_button("診断する")

# 結果表示
if submitted:
    top_type = max(scores, key=scores.get)
    type_label = TYPES[top_type]
    link_url = TYPE_LINKS[top_type]

    st.markdown("## 🔍 診断結果")
    st.markdown(f"あなたは **{type_label}** かもしれません。")
    st.markdown("あなたのタイプに合ったアドバイスを受け取るには、以下をクリックしてください：")
    st.markdown(f"[📩 アドバイスを受けとる]({link_url})")
