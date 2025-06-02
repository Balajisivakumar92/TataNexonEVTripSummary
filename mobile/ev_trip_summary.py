import streamlit as st

# === Evaluation Functions ===

def evaluate_efficiency_grade(wh_per_km):
    if wh_per_km < 110:
        return ("A", "Excellent")
    elif wh_per_km < 130:
        return ("B", "Good")
    elif wh_per_km < 150:
        return ("C", "Average")
    elif wh_per_km < 170:
        return ("D", "Below Average")
    else:
        return ("F", "Poor")

def interpret_performance(score):
    if score >= 8:
        return "Excellent ✅"
    elif score >= 6:
        return "Good 👍"
    elif score >= 4:
        return "Average ⚠️"
    else:
        return "Poor ❌"

def interpret_safety(score):
    if score >= 9:
        return "Excellent ✅"
    elif score >= 7:
        return "Safe 👍"
    elif score >= 5:
        return "Moderate ⚠️"
    else:
        return "Risky ❌"

def grade_meaning(grade):
    meanings = {
        "A": "Excellent – Highly efficient and well-optimized",
        "B": "Good – Performs well with minor inefficiencies",
        "C": "Average – Room for improvement",
        "D": "Below Average – Adjust driving habits",
        "F": "Poor – Needs serious improvement"
    }
    return meanings.get(grade, "Unknown")

# === Streamlit App ===

st.set_page_config(page_title="EV Trip Summary", page_icon="⚡")
st.title("⚡ EV Trip Summary Tool")

# Mode Selector
simple_mode = st.checkbox("I want only energy efficiency and cost analysis")

# Common inputs for both modes
date = st.date_input("Trip Date")
distance_km = st.number_input("Distance Travelled (km)", min_value=0.0)
wh_per_km = st.number_input("Energy Efficiency (Wh/km)", min_value=0.0)
battery_capacity = st.number_input("Battery Capacity (kWh)", min_value=5.0, value=45.0)

# Calculated fields used in both modes
energy_used_kwh = (distance_km * wh_per_km) / 1000 if wh_per_km > 0 else 0
km_per_kwh = 1000 / wh_per_km if wh_per_km > 0 else 0
estimated_range = km_per_kwh * battery_capacity
eff_grade, eff_text = evaluate_efficiency_grade(wh_per_km)
grade_msg = grade_meaning(eff_grade)
kwh_per_100km = (wh_per_km * 100) / 1000
co2_saved_kg = distance_km * 0.12  # Approximate EV vs petrol saving

if simple_mode:
    # === Minimal Mode ===
    st.subheader("🔹 Minimal Input Mode")
    cost_per_kwh = st.number_input("Cost per kWh (₹)", min_value=0.0, value=8.0)
    estimated_cost = energy_used_kwh * cost_per_kwh
    cost_per_km = estimated_cost / distance_km if distance_km > 0 else 0

    if st.button("Calculate Efficiency & Cost"):
        st.subheader("⚡ Energy Efficiency & Cost Summary")
        st.markdown(f"📅 **Date**                 : {date}")
        st.markdown(f"🛣️ **Distance Travelled**   : {distance_km:.2f} km")
        st.markdown(f"⚡ **Energy Efficiency**     : {wh_per_km:.1f} Wh/km → {eff_grade} ({eff_text})")
        st.markdown(f"📝 **Grade Meaning**         : {grade_msg}")
        st.markdown(f"🔋 **Battery Capacity**      : {battery_capacity} kWh")
        st.markdown(f"🔌 **Total Energy Used**     : {energy_used_kwh:.2f} kWh")
        st.markdown(f"💸 **Estimated Cost**        : ₹{estimated_cost:.2f}")
        st.markdown(f"📏 **Estimated Range**       : ≈ {estimated_range:.0f} km")
        st.markdown(f"🧾 **Cost per km**           : ₹{cost_per_km:.2f}")
        st.markdown(f"⚙️ **Energy Use (kWh/100km)**: {kwh_per_100km:.2f} kWh")
        st.markdown(f"🌱 **CO₂ Emission Saved**     : ~{co2_saved_kg:.1f} kg")
        
        # === Conclusion ===
        st.subheader("🧠 Conclusion")
        conclusion = ""

        # Efficiency-based conclusion
        if eff_grade in ["A", "B"]:
            conclusion += f"✅ Your energy efficiency is rated **{eff_grade} ({eff_text})**, which is good. Keep up your driving habits!\n\n"
        elif eff_grade == "C":
            conclusion += f"⚠️ Your energy efficiency is **average ({eff_grade})**. Try smoother acceleration and less idling.\n\n"
        else:
            conclusion += f"❌ Efficiency is low ({eff_grade}). Consider improving driving style or checking vehicle condition.\n\n"

        # Cost efficiency
        if cost_per_km <= 1:
            conclusion += f"💸 Your **cost per km is low** (₹{cost_per_km:.2f}) — great savings compared to petrol vehicles!\n\n"
        elif cost_per_km <= 1.5:
            conclusion += f"💡 Your **cost per km** is ₹{cost_per_km:.2f}. Reasonable, but there’s room to optimize energy usage.\n\n"
        else:
            conclusion += f"⚠️ High running cost (₹{cost_per_km:.2f}/km). Check for aggressive driving or inefficient routes.\n\n"

        # Environmental impact
        if co2_saved_kg > 15:
            conclusion += f"🌱 You saved approximately **{co2_saved_kg:.1f} kg** of CO₂ compared to a petrol car. Great job helping the environment!"
        else:
            conclusion += f"🌿 Some CO₂ savings achieved — around **{co2_saved_kg:.1f} kg**. Small changes can increase impact."

        st.markdown(f"""{conclusion}""")

else:
    # === Full Mode ===
    st.subheader("🔹 Full Trip Evaluation Mode")
    vehicle_type = st.selectbox("Vehicle Type", ["Hatchback", "Sedan", "SUV"])
    avg_speed = st.number_input("Average Speed (km/h)", min_value=0.0)
    idle_pct = st.slider("Idle Time (%)", 0, 100)
    performance_score = st.slider("Performance Score (out of 10)", 0.0, 10.0)
    top_speed = st.number_input("Top Speed (km/h)", min_value=0.0)
    accel_pct = st.slider("Acceleration %", 0, 100)
    decel_pct = st.slider("Deceleration %", 0, 100)
    cruise_pct = st.slider("Cruising %", 0, 100)
    safety_score = st.slider("Safety Score (optional)", 0.0, 10.0, value=7.0)
    harsh_braking = st.number_input("Harsh Braking Events", min_value=0)
    estimated_cost = energy_used_kwh * 8  # Default cost per kWh
    cost_per_km = estimated_cost / distance_km if distance_km > 0 else 0

    if st.button("Generate Full Trip Summary"):
        # Summary
        st.subheader("======= ⚡ EV Trip Summary =======")
        st.markdown(f"📅 **Date**                 : {date}")
        st.markdown(f"🚗 **Vehicle Type**         : {vehicle_type.title()}")
        st.markdown(f"🛣️ **Distance Travelled**   : {distance_km:.2f} km")
        st.markdown(f"⚡ **Energy Efficiency**     : {wh_per_km:.1f} Wh/km → {eff_grade} ({eff_text})")
        st.markdown(f"📝 **Grade Meaning**         : {grade_msg}")
        st.markdown(f"🔁 **km per kWh**           : {km_per_kwh:.2f} km/kWh")
        st.markdown(f"🚀 **Top Speed**             : {top_speed:.1f} km/h")
        st.markdown(f"🚗 **Avg Speed**             : {avg_speed:.2f} km/h")
        st.markdown(f"🕒 **Idle Time**             : {idle_pct:.0f}%")
        st.markdown(f"🎯 **Performance Score**     : {performance_score}/10")
        st.markdown(f"🛡️ **Safety Score**          : {safety_score}")
        st.markdown(f"💥 **Harsh Braking Events**  : {harsh_braking}")
        st.markdown(f"🔋 **Battery Capacity**      : {battery_capacity} kWh")
        st.markdown(f"🔌 **Total Energy Used**     : {energy_used_kwh:.2f} kWh")
        st.markdown(f"💸 **Estimated Cost**        : ₹{estimated_cost:.2f}")
        st.markdown(f"📏 **Estimated Range**       : ≈ {estimated_range:.0f} km")
        st.markdown(f"🧾 **Cost per km**           : ₹{cost_per_km:.2f}")
        st.markdown(f"⚙️ **Energy Use (kWh/100km)**: {kwh_per_100km:.2f} kWh")
        st.markdown(f"🌱 **CO₂ Emission Saved**     : ~{co2_saved_kg:.1f} kg")

        # Scorecard
        st.subheader("====== 🧾 Personalized Scorecard ======")
        st.markdown(f"📊 **Efficiency Grade**      : {eff_grade} → {grade_msg}")
        st.markdown(f"🎯 **Performance Rating**    : {interpret_performance(performance_score)}")
        st.markdown(f"🛡️ **Safety Rating**         : {interpret_safety(safety_score)}")

        # Overall Grade
        if eff_grade in ['A', 'B'] and performance_score >= 7 and (safety_score is None or safety_score >= 8):
            overall = "A"
        elif eff_grade in ['B', 'C'] and performance_score >= 6 and (safety_score is None or safety_score >= 6):
            overall = "B"
        elif eff_grade in ['C', 'D'] or performance_score >= 5:
            overall = "C"
        elif eff_grade == 'F' or performance_score < 4:
            overall = "D"
        else:
            overall = "F"
        st.markdown(f"📈 **Overall Grade**         : {overall} → {grade_meaning(overall)}")

        # Driving Pattern Insights
        st.subheader("====== 📍 Driving Pattern Insights ======")
        st.markdown(f"🕹️ **Acceleration Time**     : {accel_pct:.1f}%")
        st.markdown(f"🛑 **Deceleration Time**     : {decel_pct:.1f}%")
        st.markdown(f"🛞 **Cruising Time**         : {cruise_pct:.1f}%")
        if accel_pct > 25:
            st.warning("- ⚠️ High acceleration % → Contributes to energy loss.")
        if decel_pct > 25:
            st.warning("- ⚠️ Frequent braking → Anticipate better.")
        if cruise_pct > 30:
            st.success("- ✅ Good cruising percentage.")
        if idle_pct > 10:
            st.error("- ⛔ High idle % → Drain without benefit.")

        # Safety Summary
        st.subheader("====== 🛡️ Safety Summary ======")
        if safety_score < 7:
            st.warning("- ⚠️ Try maintaining more consistent speeds.")
        if harsh_braking > 3:
            st.error("- 🚨 Excessive harsh braking. Improve anticipation.")
        elif harsh_braking > 0:
            st.warning("- ⚠️ Some harsh braking. Try smoother stops.")
        else:
            st.success("- ✅ No harsh braking.")

        # Vehicle Tips
        st.subheader("====== 🔧 Vehicle Specific Tips ======")
        if vehicle_type.lower() == "hatchback":
            st.markdown("- Hatchbacks are generally light. Use Eco mode to maximize regenerative braking.")
        elif vehicle_type.lower() == "sedan":
            st.markdown("- Sedans benefit from smoother acceleration on highways.")
        elif vehicle_type.lower() == "suv":
            st.markdown("- SUVs consume more power; try to limit idle and AC usage.")
        else:
            st.markdown("- Consider adjusting driving based on your EV’s size and weight.")

        if battery_capacity <= 30:
            st.markdown("- Small battery: Prioritize short trips and plan charges ahead.")
        elif battery_capacity <= 50:
            st.markdown("- Mid-range battery: Best suited for city + short highway usage.")
        else:
            st.markdown("- Large battery: Take advantage of range for longer, steady drives.")
        
        # === Conclusion ===
        st.subheader("🧠 Conclusion")
        conclusion = ""

        # Efficiency-based conclusion
        if eff_grade in ["A", "B"]:
            conclusion += f"✅ Your energy efficiency is rated **{eff_grade} ({eff_text})**, which is good. Keep up your driving habits!\n\n"
        elif eff_grade == "C":
            conclusion += f"⚠️ Your energy efficiency is **average ({eff_grade})**. Try smoother acceleration and less idling.\n\n"
        else:
            conclusion += f"❌ Efficiency is low ({eff_grade}). Consider improving driving style or checking vehicle condition.\n\n"

        # Cost efficiency
        if cost_per_km <= 1:
            conclusion += f"💸 Your **cost per km is low** (₹{cost_per_km:.2f}) — great savings compared to petrol vehicles!\n\n"
        elif cost_per_km <= 1.5:
            conclusion += f"💡 Your **cost per km** is ₹{cost_per_km:.2f}. Reasonable, but there’s room to optimize energy usage.\n\n"
        else:
            conclusion += f"⚠️ High running cost (₹{cost_per_km:.2f}/km). Check for aggressive driving or inefficient routes.\n\n"

        # Environmental impact
        if co2_saved_kg > 15:
            conclusion += f"🌱 You saved approximately **{co2_saved_kg:.1f} kg** of CO₂ compared to a petrol car. Great job helping the environment!"
        else:
            conclusion += f"🌿 Some CO₂ savings achieved — around **{co2_saved_kg:.1f} kg**. Small changes can increase impact."

        st.markdown(f"""{conclusion}""")