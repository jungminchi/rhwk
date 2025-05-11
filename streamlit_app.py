import streamlit as st
import random

st.set_page_config(page_title="자동차 카드 배틀", layout="wide")

def calculate_performance(car, terrain, obstacle):
    score = 0
    score += (300 - car["acceleration"] * 50)
    score += car["top_speed"]
    score += car["handling"]

    if terrain in car.get("tires", ""):
        score += 50

    if obstacle == "낮은 지상고" and car.get("ride_height", "") == "Low":
        score -= 40

    return score

def show_card(car, title):
    st.subheader(title)
    st.image(car.get("image", "https://via.placeholder.com/300"), width=300)
    st.write(f"**차량명:** {car['name']}")
    st.write(f"**등급:** {car.get('rarity', 'Unknown')}")
    st.metric("0-100km/h 가속 (s)", car["acceleration"])
    st.metric("최고 속도 (km/h)", car["top_speed"])
    st.metric("핸들링 점수", car["handling"])

def show_card(car, title):
    st.subheader(title)
    st.image(car.get("image", "https://via.placeholder.com/300"), width=300)
    st.write(f"**차량명:** {car['name']}")
    st.write(f"**등급:** {car['rarity']}")
    st.metric("0-100km/h 가속 (s)", car["acceleration"])
    st.metric("최고 속도 (km/h)", car["top_speed"])
    st.metric("핸들링 점수", car["handling"])

def show_card(car, title):
    st.subheader(title)
    st.image(car.get("image", "https://via.placeholder.com/300"), width=300)
    st.write(f"**차량명:** {car['name']}")
    st.write(f"**등급:** {car.get('rarity', 'Unknown')}")
    st.metric("0-100km/h 가속 (s)", car["acceleration"])
    st.metric("최고 속도 (km/h)", car["top_speed"])
    st.metric("핸들링 점수", car["handling"])

car_data = {
    "Hyundai": {
    "Elantra": {"Top Speed": 210, "Acceleration": 8.0, "Handling": 75, "Drive Type": "FWD", "Type": "세단", "rarity": "Common"},
    "Sonata": {"Top Speed": 200, "Acceleration": 9.0, "Handling": 78, "Drive Type": "FWD", "Type": "세단", "rarity": "Common"},
    "Tucson": {"Top Speed": 200, "Acceleration": 9.0, "Handling": 80, "Drive Type": "AWD", "Type": "SUV", "rarity": "Common"},
    "Santa Fe": {"Top Speed": 200, "Acceleration": 9.5, "Handling": 78, "Drive Type": "AWD", "Type": "SUV", "rarity": "Common"},
    "Ioniq 5": {"Top Speed": 185, "Acceleration": 5.2, "Handling": 83, "Drive Type": "AWD", "Type": "전기차", "rarity": "Uncommon"},
    "Veloster": {"Top Speed": 225, "Acceleration": 6.0, "Handling": 85, "Drive Type": "FWD", "Type": "스포츠카", "rarity": "Rare"},
    "Genesis G70": {"Top Speed": 250, "Acceleration": 6.0, "Handling": 85, "Drive Type": "RWD", "Type": "세단", "rarity": "Rare"},
    "Kona": {"Top Speed": 190, "Acceleration": 9.0, "Handling": 75, "Drive Type": "FWD", "Type": "소형 SUV", "rarity": "Common"},
    "Genesis GV70": {"Top Speed": 220, "Acceleration": 6.2, "Handling": 80, "Drive Type": "AWD", "Type": "SUV", "rarity": "Uncommon"},
    "Palisade": {"Top Speed": 200, "Acceleration": 9.5, "Handling": 78, "Drive Type": "AWD", "Type": "SUV", "rarity": "Common"}
},
"Porsche": {
    "911 Turbo S": {"Top Speed": 330, "Acceleration": 2.7, "Handling": 95, "Drive Type": "AWD", "Type": "스포츠카", "rarity": "Legendary"},
    "Macan": {"Top Speed": 250, "Acceleration": 5.4, "Handling": 85, "Drive Type": "AWD", "Type": "SUV", "rarity": "Rare"},
    "Cayenne": {"Top Speed": 270, "Acceleration": 4.8, "Handling": 90, "Drive Type": "AWD", "Type": "SUV", "rarity": "Epic"},
    "Taycan": {"Top Speed": 260, "Acceleration": 3.2, "Handling": 92, "Drive Type": "AWD", "Type": "전기차", "rarity": "Epic"},
    "Panamera": {"Top Speed": 305, "Acceleration": 3.6, "Handling": 92, "Drive Type": "AWD", "Type": "세단", "rarity": "Epic"},
    "718 Cayman": {"Top Speed": 285, "Acceleration": 4.1, "Handling": 93, "Drive Type": "RWD", "Type": "스포츠카", "rarity": "Epic"},
    "911 Carrera": {"Top Speed": 295, "Acceleration": 4.2, "Handling": 94, "Drive Type": "RWD", "Type": "스포츠카", "rarity": "Epic"},
    "911 GT3": {"Top Speed": 320, "Acceleration": 3.4, "Handling": 98, "Drive Type": "RWD", "Type": "슈퍼카", "rarity": "Legendary"},
    "911 Turbo": {"Top Speed": 305, "Acceleration": 3.2, "Handling": 97, "Drive Type": "AWD", "Type": "스포츠카", "rarity": "Legendary"},
    "Cayenne Turbo": {"Top Speed": 280, "Acceleration": 4.7, "Handling": 89, "Drive Type": "AWD", "Type": "SUV", "rarity": "Epic"}
},
    "Chevrolet": {
        "Corvette": {"Top Speed": 310, "Acceleration": 3.0, "Handling": 90, "Drive Type": "RWD", "Type": "스포츠카"},
        "Camaro": {"Top Speed": 290, "Acceleration": 3.5, "Handling": 88, "Drive Type": "RWD", "Type": "스포츠카"},
        "Silverado": {"Top Speed": 190, "Acceleration": 7.0, "Handling": 75, "Drive Type": "AWD", "Type": "픽업"},
        "Tahoe": {"Top Speed": 200, "Acceleration": 6.0, "Handling": 78, "Drive Type": "AWD", "Type": "SUV"},
        "Equinox": {"Top Speed": 210, "Acceleration": 7.2, "Handling": 80, "Drive Type": "AWD", "Type": "SUV"},
        "Malibu": {"Top Speed": 240, "Acceleration": 8.0, "Handling": 82, "Drive Type": "FWD", "Type": "세단"},
        "Traverse": {"Top Speed": 220, "Acceleration": 7.5, "Handling": 80, "Drive Type": "AWD", "Type": "SUV"},
        "Bolt EV": {"Top Speed": 160, "Acceleration": 6.5, "Handling": 85, "Drive Type": "FWD", "Type": "전기차"},
        "Impala": {"Top Speed": 240, "Acceleration": 8.0, "Handling": 82, "Drive Type": "FWD", "Type": "세단"}
    },
    "Audi": {
        "R8": {"Top Speed": 330, "Acceleration": 3.2, "Handling": 95, "Drive Type": "AWD", "Type": "스포츠카"},
        "RS7": {"Top Speed": 300, "Acceleration": 3.5, "Handling": 93, "Drive Type": "AWD", "Type": "세단"},
        "RS5": {"Top Speed": 280, "Acceleration": 3.7, "Handling": 92, "Drive Type": "AWD", "Type": "스포츠카"},
        "Q8": {"Top Speed": 250, "Acceleration": 5.0, "Handling": 80, "Drive Type": "AWD", "Type": "SUV"},
        "A5": {"Top Speed": 250, "Acceleration": 4.5, "Handling": 87, "Drive Type": "AWD", "Type": "스포츠카"},
        "A6": {"Top Speed": 250, "Acceleration": 5.5, "Handling": 85, "Drive Type": "AWD", "Type": "세단"},
        "S7": {"Top Speed": 290, "Acceleration": 4.0, "Handling": 90, "Drive Type": "AWD", "Type": "세단"},
        "Q7": {"Top Speed": 240, "Acceleration": 6.0, "Handling": 80, "Drive Type": "AWD", "Type": "SUV"},
        "A4": {"Top Speed": 240, "Acceleration": 7.0, "Handling": 78, "Drive Type": "AWD", "Type": "세단"},
        "S5": {"Top Speed": 260, "Acceleration": 5.1, "Handling": 85, "Drive Type": "AWD", "Type": "스포츠카"}
    },
    "Volkswagen": {
        "Golf GTI": {"Top Speed": 250, "Acceleration": 6.2, "Handling": 85, "Drive Type": "FWD", "Type": "해치백"},
        "Passat": {"Top Speed": 240, "Acceleration": 7.5, "Handling": 80, "Drive Type": "FWD", "Type": "세단"},
        "Tiguan": {"Top Speed": 210, "Acceleration": 8.5, "Handling": 75, "Drive Type": "AWD", "Type": "SUV"},
        "Arteon": {"Top Speed": 250, "Acceleration": 6.0, "Handling": 83, "Drive Type": "AWD", "Type": "세단"},
        "ID.4": {"Top Speed": 180, "Acceleration": 8.0, "Handling": 80, "Drive Type": "AWD", "Type": "전기차"},
        "Touareg": {"Top Speed": 250, "Acceleration": 6.5, "Handling": 85, "Drive Type": "AWD", "Type": "SUV"},
        "Jetta": {"Top Speed": 230, "Acceleration": 8.0, "Handling": 77, "Drive Type": "FWD", "Type": "세단"},
        "Polo": {"Top Speed": 210, "Acceleration": 8.5, "Handling": 75, "Drive Type": "FWD", "Type": "해치백"},
        "Golf R": {"Top Speed": 270, "Acceleration": 4.6, "Handling": 90, "Drive Type": "AWD", "Type": "해치백"},
        "Sharan": {"Top Speed": 200, "Acceleration": 9.0, "Handling": 70, "Drive Type": "FWD", "Type": "MPV"}
    }
}


for brand in car_data.values():
    for model_name, specs in brand.items():
        specs["name"] = model_name
        specs["top_speed"] = specs.pop("Top Speed")
        specs["acceleration"] = specs.pop("Acceleration")
        specs["handling"] = specs.pop("Handling")

def calculate_performance_score(car):
    weight_top_speed = 0.3
    weight_acceleration = 0.3
    weight_handling = 0.4
    score = (car["top_speed"] * weight_top_speed) + (car["acceleration"] * weight_acceleration) + (car["handling"] * weight_handling)
    return score

st.title("🚗 자동차 카드 배틀 게임")

if "unlocked_cars" not in st.session_state:
    st.session_state.unlocked_cars = []

if "pack_opened" not in st.session_state:
    st.session_state.pack_opened = False

if not st.session_state.pack_opened:
    st.header("🎁 카드팩을 열어보세요!")
    if st.button("🔓 카드팩 열기 (5개 무작위 차량)"):
        all_cars = [car for brand in car_data.values() for car in brand.values()]
        st.session_state.unlocked_cars = random.sample(all_cars, min(5, len(all_cars)))
        st.session_state.pack_opened = True
        st.rerun()

if st.session_state.pack_opened:
    st.sidebar.header("🧩 당신의 차량 선택")
    car_names = [f"{car['name']} [{car.get('rarity', 'Unknown')}]" for car in st.session_state.unlocked_cars]
    selected_label = st.sidebar.selectbox("당신의 차량을 선택하세요", car_names)

    selected_car = next((car for car in st.session_state.unlocked_cars if f"{car['name']} [{car.get('rarity', 'Unknown')}]" == selected_label), None)

    all_cars = [car for brand in car_data.values() for car in brand.values()]
    available_opponent_cars = [car for car in all_cars if car != selected_car]
    opponent_car = random.choice(available_opponent_cars)

    terrain = random.choice(["아스팔트", "흙길", "모래", "풀밭", "악천후"])
    obstacle = random.choice(["없음", "낮은 지상고"])

    st.subheader("🌍 맵 정보")
    st.write(f"**지형:** {terrain}")
    st.write(f"**장애물:** {obstacle}")

    col1, col2 = st.columns(2)
    with col1:
        show_card(selected_car, "🚘 당신의 차량")
    with col2:
        show_card(opponent_car, "🆚 상대 차량")

    selected_score = calculate_performance(selected_car, terrain, obstacle)
    opponent_score = calculate_performance(opponent_car, terrain, obstacle)

    st.markdown("---")
    st.subheader("⚔️ 비교 결과")
    st.write(f"🏁 당신의 성능 점수: **{round(selected_score, 1)}**")
    st.write(f"🏁 상대의 성능 점수: **{round(opponent_score, 1)}**")

    if selected_score > opponent_score:
        st.success("🎉 당신이 이겼습니다!")
    elif selected_score < opponent_score:
        st.error("😢 당신이 졌습니다.")
    else:
        st.info("🤝 비겼습니다!")

    if st.button("🔁 다시 카드 뽑기"):
        st.session_state.pack_opened = False
        st.rerun()