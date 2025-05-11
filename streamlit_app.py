import streamlit as st
import random
import time
from car_data import car_data

def show_card(car, title):
    st.subheader(title)
    st.write(f"**차량명:** {car['name']}")
    st.write(f"**등급:** {car.get('rarity', 'Unknown')}")
    st.metric("최고 속도 (km/h)", car.get("Top Speed", "-"))
    st.metric("0-100km/h 가속 (s)", car.get("Acceleration", "-"))
    st.metric("핸들링 점수", car.get("Handling", "-"))
    st.write(f"**구동방식:** {car.get('Drive Type', '-')} | **차량 종류:** {car.get('Type', '-')} | **타이어 유형:** {car.get('Tire Type', 'Standard')}")

def calculate_performance(car, terrain, obstacle):
    score = 0
    performance_details = {}

    acceleration = car.get("Acceleration", 0)
    if isinstance(acceleration, (int, float)):
        score += (300 - acceleration * 50)
        performance_details["가속"] = f"{acceleration}s로 {300 - acceleration * 50}점 추가"
    else:
        performance_details["가속"] = "정보 없음"

    score += car.get("Top Speed", 0)
    performance_details["최고 속도"] = f"{car.get('Top Speed', 0)}km/h로 {car.get('Top Speed', 0)}점 추가"

    score += car.get("Handling", 0)
    performance_details["핸들링"] = f"{car.get('Handling', 0)}으로 {car.get('Handling', 0)}점 추가"

    tire_type = car.get("Tire Type", "Standard")
    terrain_factor = tire_factors.get(tire_type, {}).get(terrain, 1.0)
    score *= terrain_factor  
    performance_details["타이어 보정"] = f"타이어 유형 ({tire_type})에 따른 지형 보정값: {terrain_factor}배"

    if obstacle == "낮은 지상고" and car.get("ride_height", "") == "Low":
        score -= 40
        performance_details["장애물 적합성"] = f"장애물 ({obstacle})에 적합하지 않아 -40점 차감"

    score += random.uniform(0.1, 0.5)  
    return score, performance_details

def sell_car(car):
    rarity = car.get('rarity', 'Common')
    sell_price = car_sell_prices.get(rarity, 100)
    st.session_state.coins += sell_price
    st.session_state.my_collection.remove(car)

st.set_page_config(page_title="Top Drives 스타일 자동차 배틀", layout="wide")

if "coins" not in st.session_state:
    st.session_state.coins = 0
if "unlocked_cars" not in st.session_state:
    st.session_state.unlocked_cars = []
if "my_collection" not in st.session_state:
    st.session_state.my_collection = []
if "pack_opened" not in st.session_state:
    st.session_state.pack_opened = False
if "first_pack" not in st.session_state:
    st.session_state.first_pack = True
if "show_animation" not in st.session_state:
    st.session_state.show_animation = False

car_upgrade_costs = {"Common": 300, "Rare": 500, "Epic": 800, "Legendary": 1200}
car_sell_prices = {"Common": 100, "Rare": 200, "Epic": 400, "Legendary": 800}

tire_factors = {
    "Performance": {"아스팔트/맑음": 1.0, "아스팔트/비": 0.65, "비포장 도로/맑음": 0.30, "비포장 도로/비": 0.25, "자갈": 0.10, "모래": 0.20, "눈": 0.15, "얼음": 0.05, "슬릭": 0.01},
    "Standard": {"아스팔트/맑음": 1.0, "아스팔트/비": 0.80, "비포장 도로/맑음": 0.35, "비포장 도로/비": 0.30, "자갈": 0.25, "모래": 0.30, "눈": 0.25, "얼음": 0.15, "슬릭": 0.03},
    "All-Terrain": {"아스팔트/맑음": 1.0, "아스팔트/비": 0.70, "비포장 도로/맑음": 0.40, "비포장 도로/비": 0.35, "자갈": 0.30, "모래": 0.35, "눈": 0.30, "얼음": 0.20, "슬릭": 0.04},
    "Off-Road": {"아스팔트/맑음": 1.0, "아스팔트/비": 0.50, "비포장 도로/맑음": 0.45, "비포장 도로/비": 0.40, "자갈": 0.35, "모래": 0.40, "눈": 0.40, "얼음": 0.25, "슬릭": 0.05}
}

tab1, tab2, tab3 = st.tabs(["🎁 카드팩 열기", "📁 내 컬렉션", "⚔️ CPU 전투"])

with tab1:
    st.header("🎁 카드팩 열기")
    pack_price = 500

    if st.session_state.first_pack:
        if st.button("🆓 첫 카드팩 열기 (무료)") :
            st.session_state.show_animation = True
            st.session_state.first_pack = False
            st.rerun()
    else:
        if st.button(f"🪙 {pack_price} 코인으로 카드팩 구매 및 열기"):
            if st.session_state.coins >= pack_price:
                st.session_state.coins -= pack_price
                st.session_state.show_animation = True
                st.rerun()
            else:
                st.warning("코인이 부족합니다.")

    if st.session_state.show_animation:
        st.image("https://media1.giphy.com/media/oF5oUYTOhvFnO/giphy.webp", caption="카드팩 개봉 중...", use_column_width=True)
        time.sleep(3)

        all_cars = [car for brand in car_data.values() for car in brand.values()]
        owned_names = {c["name"] for c in st.session_state.my_collection}
        available_cars = [car for car in all_cars if car.get("name") not in owned_names]

        if not available_cars:
            st.warning("모든 차량을 이미 수집했습니다! 🎉")
        else:
            car_rarities = ['Legendary', 'Epic', 'Rare', 'Common']
            car_rarity_weights = [0.01, 0.12, 0.34, 0.53]
            new_cars = []
            for _ in range(5):
                chosen_rarity = random.choices(car_rarities, car_rarity_weights)[0]
                filtered_cars = [car for car in available_cars if car['rarity'] == chosen_rarity]
                if filtered_cars:
                    new_car = random.choice(filtered_cars)
                    new_cars.append(new_car)
                else:
                    st.warning(f"{chosen_rarity} 등급의 차량이 부족합니다.")
            
            st.session_state.unlocked_cars = new_cars
            st.session_state.my_collection.extend(new_cars)
        st.session_state.show_animation = False
        st.rerun()

    if st.session_state.pack_opened and st.session_state.unlocked_cars:
        st.subheader("🎉 다음 차량을 획득했습니다:")
        for car in st.session_state.unlocked_cars:
            show_card(car, car['name'])
            if st.button(f"{car['name']} 차량 판매", key=f"sell_{car['name']}"):
                sell_car(car)
                st.success(f"{car['name']} 차량을 판매하고 {car_sell_prices.get(car.get('rarity', 'Common'), 100)} 코인을 얻었습니다!")

        st.session_state.unlocked_cars = []


with tab2:
    st.header("📁 내 컬렉션")
    st.write(f"💰 현재 보유한 코인: {st.session_state.coins} 코인")
    
    if not st.session_state.my_collection:
        st.info("아직 카드가 없습니다. 카드팩을 열어보세요!")
    else:
        for idx, car in enumerate(st.session_state.my_collection):
            show_card(car, f"{idx+1}. {car['name']}")
            if st.button(f"{car['name']} 차량 판매", key=f"sell_{car['name']}_{id(car)}"):

                sell_car(car)
                st.success(f"{car['name']} 차량을 판매하고 {car_sell_prices.get(car.get('rarity', 'Common'), 100)} 코인을 얻었습니다!")

with tab3:
    st.header("⚔️ race")
    if len(st.session_state.my_collection) == 0:
        st.warning("내 차량이 없습니다.")
    else:
        selected_car = st.selectbox("내 차량 선택", st.session_state.my_collection, format_func=lambda x: x['name'])

        opponent_car = random.choice([car for car in car_data['Hyundai'].values()])

        terrain = random.choice(["아스팔트/맑음", "아스팔트/비", "비포장 도로/맑음", "비포장 도로/비", "자갈", "모래", "눈", "얼음", "슬릭"])
        obstacle = random.choice(["없음", "낮은 지상고"])

        st.write(f"**경기 지형:** {terrain}")
        st.write(f"**장애물:** {obstacle}")

        if selected_car and opponent_car:
            score1, performance1 = calculate_performance(selected_car, terrain, obstacle)
            score2, performance2 = calculate_performance(opponent_car, terrain, obstacle)

        st.write(f"**내 차량 성능:** {score1}점")
        st.write(f"**상대 차량 성능:** {score2}점")
        st.write(f"내 차량 성능 세부 사항: {performance1}")
        st.write(f"상대 차량 성능 세부 사항: {performance2}")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("내 차량")
            show_card(selected_car, selected_car['name'])

        with col2:
            st.subheader("상대 차량")
            show_card(opponent_car, opponent_car['name'])

        if score1 > score2:
            st.success("🎉 당신이 이겼습니다!")
        elif score1 < score2:
            st.error("💥 당신이 졌습니다!")
        else:
            st.warning("무승부입니다.")