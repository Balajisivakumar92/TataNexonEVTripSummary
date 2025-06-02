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
        "C": "Average – Room for improvement in efficiency or behavior",
        "D": "Below Average – Consider adjusting driving habits",
        "F": "Poor – Inefficient or unsafe, needs serious improvement"
    }
    return meanings.get(grade, "Unknown")

def personalized_scorecard(eff_grade, performance_score, safety_score):
    print("\n====== 🧾 Personalized Scorecard ======")
    print(f"📊 Efficiency Grade      : {eff_grade} → {grade_meaning(eff_grade)}")
    print(f"🎯 Performance Rating    : {interpret_performance(performance_score)}")
    if safety_score is not None:
        print(f"🛡️ Safety Rating         : {interpret_safety(safety_score)}")

    # Determine overall grade
    print("📈 Overall Grade         :", end=" ")
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

    print(f"{overall} → {grade_meaning(overall)}")

def tips_by_vehicle(vehicle_type, battery_capacity_kwh):
    print("\n====== 🔧 Vehicle Specific Tips ======")
    if vehicle_type.lower() == "hatchback":
        print("- Hatchbacks are generally light. Use Eco mode to maximize regenerative braking.")
    elif vehicle_type.lower() == "sedan":
        print("- Sedans benefit from smoother acceleration on highways.")
    elif vehicle_type.lower() == "suv":
        print("- SUVs consume more power; try to limit idle and AC usage.")
    else:
        print("- Consider adjusting driving based on your EV’s size and weight.")

    if battery_capacity_kwh <= 30:
        print("- Small battery: Prioritize short trips and plan charges ahead.")
    elif battery_capacity_kwh <= 50:
        print("- Mid-range battery: Best suited for city + short highway usage.")
    else:
        print("- Large battery: Take advantage of range for longer, steady drives.")

def ev_trip_summary(date, distance_km, wh_per_km, avg_speed_kmph, idle_percent, performance_score,
                    vehicle_type="suv", battery_capacity_kwh=45, cost_per_kwh=8,
                    top_speed=0, acceleration_pct=0, deceleration_pct=0, cruising_pct=0,
                    safety_score=None, harsh_braking_events=None):

    energy_used_kwh = (distance_km * wh_per_km) / 1000
    km_per_kwh = 1000 / wh_per_km
    eff_grade, eff_text = evaluate_efficiency_grade(wh_per_km)
    estimated_cost = energy_used_kwh * cost_per_kwh
    estimated_range = km_per_kwh * battery_capacity_kwh
    safety_feedback = interpret_safety(safety_score) if safety_score is not None else "N/A"

    print("\n======= ⚡ EV Trip Summary =======")
    print(f"📅 Date                 : {date}")
    print(f"🚗 Vehicle Type         : {vehicle_type.title()}")
    print(f"🛣️ Distance Travelled   : {distance_km:.2f} km")
    print(f"⚡ Energy Efficiency     : {wh_per_km:.1f} Wh/km ({eff_text})")
    print(f"🔁 km per kWh           : {km_per_kwh:.2f} km/kWh")
    print(f"🚀 Top Speed             : {top_speed:.1f} km/h")
    print(f"🚗 Avg Speed             : {avg_speed_kmph:.2f} km/h")
    print(f"🕒 Idle Time             : {idle_percent:.0f}%")
    print(f"🎯 Performance Score     : {performance_score}/10")
    print(f"🛡️ Safety Score          : {safety_score if safety_score is not None else 'N/A'}")
    print(f"💥 Harsh Braking Events  : {harsh_braking_events if harsh_braking_events is not None else 'N/A'}")
    print(f"🔋 Battery Capacity      : {battery_capacity_kwh} kWh")
    print(f"🔌 Total Energy Used     : {energy_used_kwh:.2f} kWh")
    print(f"💸 Estimated Cost        : ₹{estimated_cost:.2f}")
    print(f"📏 Estimated Range       : ≈ {estimated_range:.0f} km")

    personalized_scorecard(eff_grade, performance_score, safety_score)

    print("\n====== 📍 Driving Pattern Insights ======")
    print(f"🕹️ Acceleration Time     : {acceleration_pct:.1f}%")
    print(f"🛑 Deceleration Time     : {deceleration_pct:.1f}%")
    print(f"🛞 Cruising Time         : {cruising_pct:.1f}%")
    if acceleration_pct > 25:
        print("- ⚠️ High acceleration % → Contributes to energy loss.")
    if deceleration_pct > 25:
        print("- ⚠️ Frequent braking → Anticipate better.")
    if cruising_pct > 30:
        print("- ✅ Good cruising percentage.")
    if idle_percent > 10:
        print("- ⛔ High idle % → Drain without benefit.")

    print("\n====== 🛡️ Safety Summary ======")
    if safety_score is not None:
        print(f"- Safety Rating: {safety_feedback}")
        if safety_score < 7:
            print("- ⚠️ Try maintaining more consistent speeds.")
    if harsh_braking_events is not None:
        if harsh_braking_events > 3:
            print("- 🚨 Excessive harsh braking. Improve anticipation.")
        elif harsh_braking_events > 0:
            print("- ⚠️ Some harsh braking. Try smoother stops.")
        else:
            print("- ✅ No harsh braking.")

    tips_by_vehicle(vehicle_type, battery_capacity_kwh)

    print("===================================")

# === Input Section ===
print("🔋 Enter Your EV Trip Details")
date = input("Date (e.g., 31 May 2025): ")
# vehicle_type = input("Vehicle Type (Hatchback/Sedan/SUV): ")
distance_km = float(input("Distance travelled (km): "))
wh_per_km = float(input("Energy efficiency (Wh/km): "))
avg_speed_kmph = float(input("Average speed (km/h): "))
idle_percent = float(input("Idle time percentage (%): "))
performance_score = float(input("Performance score (out of 10): "))
# battery_capacity_kwh = float(input("Battery capacity (kWh): "))
top_speed = float(input("Top speed (km/h): "))
acceleration_pct = float(input("Acceleration time %: "))
deceleration_pct = float(input("Deceleration time %: "))
cruising_pct = float(input("Cruising time %: "))
safety_score_input = input("Safety score (optional, press Enter to skip): ")
harsh_braking_input = input("Number of harsh braking events (optional, press Enter to skip): ")

safety_score = float(safety_score_input) if safety_score_input else None
harsh_braking_events = int(harsh_braking_input) if harsh_braking_input else None

# Run
ev_trip_summary(
    date, distance_km, wh_per_km, avg_speed_kmph, idle_percent,
    performance_score, top_speed=top_speed, acceleration_pct=acceleration_pct,
    deceleration_pct=deceleration_pct, cruising_pct=cruising_pct,
    safety_score=safety_score, harsh_braking_events=harsh_braking_events
)