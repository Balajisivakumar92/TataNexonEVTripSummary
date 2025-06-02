from flask import Flask, render_template, request

app = Flask(__name__)

# Your logic functions
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
    if score >= 8: return "Excellent ✅"
    elif score >= 6: return "Good 👍"
    elif score >= 4: return "Average ⚠️"
    else: return "Poor ❌"

def interpret_safety(score):
    if score >= 9: return "Excellent ✅"
    elif score >= 7: return "Safe 👍"
    elif score >= 5: return "Moderate ⚠️"
    else: return "Risky ❌"

def grade_meaning(grade):
    return {
        "A": "Excellent – Highly efficient and well-optimized",
        "B": "Good – Performs well with minor inefficiencies",
        "C": "Average – Room for improvement in efficiency or behavior",
        "D": "Below Average – Consider adjusting driving habits",
        "F": "Poor – Inefficient or unsafe, needs serious improvement"
    }.get(grade, "Unknown")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            date = request.form["date"]
            distance_km = float(request.form["distance"])
            wh_per_km = float(request.form["wh_per_km"])
            avg_speed = float(request.form["avg_speed"])
            idle = float(request.form["idle"])
            perf_score = float(request.form["perf_score"])
            top_speed = float(request.form["top_speed"])
            accel_pct = float(request.form["accel_pct"])
            decel_pct = float(request.form["decel_pct"])
            cruise_pct = float(request.form["cruise_pct"])
            vehicle_type = request.form["vehicle_type"]
            battery_capacity = float(request.form["battery_capacity"])

            safety_score = request.form.get("safety_score")
            safety_score = float(safety_score) if safety_score else None

            braking_events = request.form.get("braking_events")
            braking_events = int(braking_events) if braking_events else None

            energy_used_kwh = (distance_km * wh_per_km) / 1000
            km_per_kwh = 1000 / wh_per_km
            eff_grade, eff_text = evaluate_efficiency_grade(wh_per_km)
            cost = energy_used_kwh * 8
            est_range = km_per_kwh * battery_capacity

            result = {
                "date": date,
                "vehicle": vehicle_type.title(),
                "distance": f"{distance_km:.2f} km",
                "wh_per_km": f"{wh_per_km:.1f} Wh/km ({eff_text})",
                "km_per_kwh": f"{km_per_kwh:.2f}",
                "top_speed": f"{top_speed} km/h",
                "avg_speed": f"{avg_speed} km/h",
                "idle": f"{idle}%",
                "perf_score": f"{perf_score}/10 → {interpret_performance(perf_score)}",
                "safety_score": f"{safety_score}/10 → {interpret_safety(safety_score)}" if safety_score is not None else "N/A",
                "braking_events": braking_events,
                "eff_grade": eff_grade,
                "grade_meaning": grade_meaning(eff_grade),
                "energy_used_kwh": f"{energy_used_kwh:.2f} kWh",
                "cost": f"₹{cost:.2f}",
                "range": f"≈ {est_range:.0f} km",
            }
        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)