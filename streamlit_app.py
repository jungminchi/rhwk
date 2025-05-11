import streamlit as st
import random
import time
from car_data import car_data

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

    if terrain in car.get("tires", ""):
        score += 50
        performance_details["지형 적합성"] = f"지형 ({terrain})에 적합하여 50점 추가"

    if obstacle == "낮은 지상고" and car.get("ride_height", "") == "Low":
        score -= 40
        performance_details["장애물 적합성"] = f"장애물 ({obstacle})에 적합하지 않아 -40점 차감"

    score += random.uniform(0.1, 0.5)  # 작은 랜덤 요소 추가
    return score, performance_details

def show_card(car, title):
    st.subheader(title)
    st.image(car.get("image", "https://via.placeholder.com/300"), width=300)
    st.write(f"**차량명:** {car['name']}")
    st.write(f"**등급:** {car.get('rarity', 'Unknown')}")
    st.metric("최고 속도 (km/h)", car.get("Top Speed", "-"))
    st.metric("0-100km/h 가속 (s)", car.get("Acceleration", "-"))
    st.metric("핸들링 점수", car.get("Handling", "-"))
    st.write(f"**구동방식:** {car.get('Drive Type', '-')} | **차량 종류:** {car.get('Type', '-')}")

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
            new_cars = random.sample(available_cars, min(5, len(available_cars)))
            st.session_state.unlocked_cars = new_cars
            st.session_state.my_collection.extend(new_cars)
            st.session_state.pack_opened = True

        st.session_state.show_animation = False
        st.rerun()

    if st.session_state.pack_opened and st.session_state.unlocked_cars:
        st.subheader("🎉 다음 차량을 획득했습니다:")
        for car in st.session_state.unlocked_cars:
            show_card(car, car['name'])
        st.session_state.unlocked_cars = []

with tab2:
    st.header("📁 내 컬렉션")
    st.write(f"💰 현재 보유한 코인: {st.session_state.coins} 코인")
    
    if not st.session_state.my_collection:
        st.info("아직 카드가 없습니다. 카드팩을 열어보세요!")
    else:
        for idx, car in enumerate(st.session_state.my_collection):
            col1, col2 = st.columns([2, 1])
            with col1:
                show_card(car, car['name'])
            with col2:
                rarity = car.get("rarity", "Common")
                sell_price = car_sell_prices.get(rarity, 100)
                if st.button(f"💰 판매 ({sell_price}코인)", key=f"sell_{idx}"):
                    st.session_state.coins += sell_price
                    st.session_state.my_collection.pop(idx)
                    st.success("판매 완료!")
                    st.rerun()

                upgrade_cost = car_upgrade_costs.get(rarity, 300)
                if st.button(f"🛠️ 강화 ({upgrade_cost}코인)", key=f"upgrade_{idx}"):
                    if st.session_state.coins >= upgrade_cost:
                        st.session_state.coins -= upgrade_cost
                        car["Top Speed"] += 5
                        car["Acceleration"] = max(1.0, car["Acceleration"] - 0.2)
                        car["Handling"] += 3
                        st.success("차량 강화 완료!")
                        st.rerun()
                    else:
                        st.warning("코인이 부족합니다.")

with tab3:
    st.header("⚔️ 레이싱")
    if len(st.session_state.my_collection) == 0:
        st.warning("내 차량이 없습니다.")
    else:
        selected_car = st.selectbox("내 차량 선택", st.session_state.my_collection, format_func=lambda x: x['name'])
        opponent = random.choice([car for brand in car_data.values() for car in brand.values() if car != selected_car])
        
        terrain = random.choice(["아스팔트", "흙길", "모래", "풀밭", "악천후"])
        obstacle = random.choice(["없음", "낮은 지상고"])
        map_name = random.choice(["맵1: 산악지역", "맵2: 도시", "맵3: 해변", "맵4: 숲길"])

        st.write(f"**맵:** {map_name}, **지형:** {terrain}, **장애물:** {obstacle}")

        col1, col2 = st.columns(2)
        with col1:
            show_card(selected_car, "🚘 내 차량")
        with col2:
            show_card(opponent, "🤖 CPU 차량")

        score1, details1 = calculate_performance(selected_car, terrain, obstacle)
        score2, details2 = calculate_performance(opponent, terrain, obstacle)

        if score1 > score2:
            st.success("🎉 승리! +300 코인\n\n**승리 이유:**")
            for key, detail in details1.items():
                st.write(f"- {key}: {detail}")
            st.session_state.coins += 300
        elif score1 < score2:
            st.error("😢 패배\n\n**패배 이유:**")
            for key, detail in details2.items():
                st.write(f"- {key}: {detail}")
        else:
            st.info("🤝 무승부")