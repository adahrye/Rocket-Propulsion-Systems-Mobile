
from pathlib import Path
import json
import html
import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).resolve().parent
MODEL = joblib.load(BASE / "rocket_model.pkl")
META = json.loads((BASE / "model_metadata.json").read_text(encoding="utf-8"))

st.set_page_config(
    page_title="AstraSim | Rocket Propulsion Validator",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700&family=Inter:wght@400;600;700&display=swap');

:root {
  --ink: #14213d;
  --muted: #5f6b7a;
  --cream: #fffaf4;
  --card: #ffffff;
  --line: #eadfd5;
  --salmon: #f47d67;
  --orange: #f5a261;
  --green: #158a63;
  --red: #c94444;
}

.stApp {
  background: linear-gradient(180deg, #fffaf4 0%, #f5f7fb 100%);
  color: var(--ink);
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
  font-family: 'Orbitron', sans-serif !important;
  color: var(--ink);
}

.block-container {
  max-width: 760px;
  padding-top: 1rem;
  padding-bottom: 3rem;
}

.hero {
  background: linear-gradient(135deg, #ffffff, #fff4eb);
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 20px;
  box-shadow: 0 12px 30px rgba(20,33,61,.08);
  margin-bottom: 14px;
}

.kicker {
  color: var(--salmon);
  font-size: .72rem;
  font-weight: 800;
  letter-spacing: .14em;
}

.title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(2rem, 9vw, 3.6rem);
  font-weight: 700;
  margin: 2px 0;
  color: var(--ink);
}

.subtitle {
  color: var(--muted);
  font-size: .95rem;
  line-height: 1.45;
}

[data-testid="stForm"] {
  background: rgba(255,255,255,.95);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 16px;
  box-shadow: 0 10px 26px rgba(20,33,61,.06);
}

div.stButton > button, div.stFormSubmitButton > button {
  width: 100%;
  border: 0;
  border-radius: 14px;
  background: linear-gradient(90deg, var(--salmon), var(--orange));
  color: white;
  font-family: 'Orbitron', sans-serif;
  font-weight: 700;
  min-height: 48px;
  box-shadow: 0 8px 20px rgba(244,125,103,.25);
}

[data-testid="stMetric"] {
  background: white;
  border: 1px solid var(--line);
  padding: 12px;
  border-radius: 14px;
}

.result-card {
  background: white;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 16px;
  margin: 10px 0;
  box-shadow: 0 10px 24px rgba(20,33,61,.06);
}

.result-label {
  color: var(--muted);
  font-size: .75rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
}

.result-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.25rem;
  margin-top: 6px;
}

.good { color: var(--green); }
.bad { color: var(--red); }

.small-note {
  color: var(--muted);
  font-size: .78rem;
  line-height: 1.4;
}

@media (max-width: 640px) {
  .block-container {
    padding-left: .75rem;
    padding-right: .75rem;
  }
  .hero {
    padding: 16px;
    border-radius: 18px;
  }
  [data-testid="stForm"] {
    padding: 12px;
  }
  .stSlider {
    margin-bottom: -.25rem;
  }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="kicker">MOBILE ROCKET PROPULSION SIMULATOR</div>
  <div class="title">ASTRASIM</div>
  <div class="subtitle">
    Choose an engine configuration, press launch, and immediately view the rocket animation and prediction.
  </div>
</div>
""", unsafe_allow_html=True)

ranges = META["numeric_ranges"]

# Defaults
defaults = {k: float(v["median"]) for k, v in ranges.items()}

with st.form("rocket_controls"):
    st.subheader("1. Configure the engine")

    fuel = st.selectbox("Fuel type", META["fuel_types"])
    oxidizer = st.selectbox("Oxidizer type", META["oxidizer_types"])

    st.markdown("**Key controls**")
    chamber_pressure = st.slider(
        "Chamber pressure (bar)",
        float(ranges["chamber_pressure_bar"]["min"]),
        float(ranges["chamber_pressure_bar"]["max"]),
        defaults["chamber_pressure_bar"],
    )
    specific_impulse = st.slider(
        "Specific impulse (s)",
        float(ranges["specific_impulse_s"]["min"]),
        float(ranges["specific_impulse_s"]["max"]),
        defaults["specific_impulse_s"],
    )
    stability_margin = st.slider(
        "Combustion stability margin",
        float(ranges["combustion_stability_margin"]["min"]),
        float(ranges["combustion_stability_margin"]["max"]),
        defaults["combustion_stability_margin"],
        step=0.001,
    )

    with st.expander("Advanced engine controls"):
        of_ratio = st.slider(
            "Oxidizer-to-fuel ratio",
            float(ranges["oxidizer_fuel_ratio"]["min"]),
            float(ranges["oxidizer_fuel_ratio"]["max"]),
            defaults["oxidizer_fuel_ratio"],
        )
        combustion_temp = st.slider(
            "Combustion temperature (K)",
            float(ranges["combustion_temperature_K"]["min"]),
            float(ranges["combustion_temperature_K"]["max"]),
            defaults["combustion_temperature_K"],
        )
        heat_ratio = st.slider(
            "Heat-capacity ratio",
            float(ranges["heat_capacity_ratio"]["min"]),
            float(ranges["heat_capacity_ratio"]["max"]),
            defaults["heat_capacity_ratio"],
            step=0.001,
        )
        expansion_ratio = st.slider(
            "Nozzle expansion ratio",
            float(ranges["nozzle_expansion_ratio"]["min"]),
            float(ranges["nozzle_expansion_ratio"]["max"]),
            defaults["nozzle_expansion_ratio"],
        )
        ambient_pressure = st.slider(
            "Ambient pressure (bar)",
            float(ranges["ambient_pressure_bar"]["min"]),
            float(ranges["ambient_pressure_bar"]["max"]),
            defaults["ambient_pressure_bar"],
            step=0.001,
        )

    submitted = st.form_submit_button("🚀 INITIATE ENGINE TEST")

# Keep advanced defaults available when expander has not been changed.
of_ratio = locals().get("of_ratio", defaults["oxidizer_fuel_ratio"])
combustion_temp = locals().get("combustion_temp", defaults["combustion_temperature_K"])
heat_ratio = locals().get("heat_ratio", defaults["heat_capacity_ratio"])
expansion_ratio = locals().get("expansion_ratio", defaults["nozzle_expansion_ratio"])
ambient_pressure = locals().get("ambient_pressure", defaults["ambient_pressure_bar"])

inputs = pd.DataFrame([{
    "fuel_type": fuel,
    "oxidizer_type": oxidizer,
    "chamber_pressure_bar": chamber_pressure,
    "oxidizer_fuel_ratio": of_ratio,
    "combustion_temperature_K": combustion_temp,
    "heat_capacity_ratio": heat_ratio,
    "nozzle_expansion_ratio": expansion_ratio,
    "ambient_pressure_bar": ambient_pressure,
    "specific_impulse_s": specific_impulse,
    "combustion_stability_margin": stability_margin,
}])

if submitted:
    probability = float(MODEL.predict_proba(inputs)[0, 1])
    prediction = int(probability >= META.get("decision_threshold", 0.5))
    confidence = probability if prediction else 1 - probability
    state = "failure" if prediction else "launch"
    status = "POTENTIAL PHYSICS VIOLATION" if prediction else "NO VIOLATION DETECTED"
    result_class = "bad" if prediction else "good"

    st.subheader("2. Launch result")

    rocket_html = f"""
    <!doctype html>
    <html>
    <head>
    <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; overflow: hidden; font-family: Arial, sans-serif; }}
    .scene {{
      height: 330px;
      position: relative;
      overflow: hidden;
      border-radius: 20px;
      background:
        radial-gradient(circle at 15% 18%, #ffffff 0 1px, transparent 2px),
        radial-gradient(circle at 80% 22%, #ffffff 0 1px, transparent 2px),
        radial-gradient(circle at 68% 68%, #ffffff 0 1px, transparent 2px),
        linear-gradient(180deg, #14213d 0%, #274060 75%, #3b4e68 100%);
      border: 1px solid rgba(20,33,61,.15);
    }}
    .rocket-wrap {{
      position: absolute;
      left: 50%;
      bottom: 42px;
      transform: translateX(-50%);
    }}
    .rocket {{
      width: 90px;
      height: 210px;
      position: relative;
      filter: drop-shadow(0 14px 20px rgba(0,0,0,.35));
    }}
    .nose {{
      position: absolute; top: 0; left: 17px;
      width: 56px; height: 65px;
      background: linear-gradient(90deg,#d7dce7,#fff 50%,#a8b0c4);
      clip-path: polygon(50% 0,100% 100%,0 100%);
    }}
    .body {{
      position: absolute; top: 54px; left: 17px;
      width: 56px; height: 108px;
      border-radius: 8px 8px 16px 16px;
      background: linear-gradient(90deg,#aeb7c9,#fff 44%,#8d97ad);
    }}
    .band {{
      position: absolute; top: 110px; left: 17px;
      width: 56px; height: 18px;
      background: linear-gradient(90deg,#f47d67,#f5a261);
    }}
    .window {{
      position: absolute; top: 73px; left: 32px;
      width: 26px; height: 26px; border-radius: 50%;
      background: radial-gradient(circle at 35% 30%,#d8fbff,#3979a8 48%,#112848 75%);
      border: 4px solid #475267;
    }}
    .fin-left {{
      position: absolute; left: 2px; top: 132px;
      width: 32px; height: 58px;
      background: linear-gradient(145deg,#f5a261,#b83c45);
      clip-path: polygon(100% 0,100% 100%,0 100%);
    }}
    .fin-right {{
      position: absolute; right: 2px; top: 132px;
      width: 32px; height: 58px;
      background: linear-gradient(215deg,#f5a261,#b83c45);
      clip-path: polygon(0 0,100% 100%,0 100%);
    }}
    .nozzle {{
      position: absolute; left: 32px; top: 158px;
      width: 27px; height: 24px;
      background: linear-gradient(90deg,#333a4a,#858fa3,#2b3140);
      clip-path: polygon(18% 0,82% 0,100% 100%,0 100%);
    }}
    .flame {{
      position: absolute; left: 30px; top: 178px;
      width: 30px; height: 52px;
      opacity: .95;
      background: linear-gradient(#fff7bf 0 18%,#ffb14a 36%,#ff6248 68%,transparent 100%);
      clip-path: polygon(50% 100%,5% 15%,28% 22%,50% 0,72% 22%,95% 15%);
      filter: drop-shadow(0 0 12px #ff6f42);
    }}
    .pad {{
      position: absolute; left: 50%; bottom: 28px;
      transform: translateX(-50%);
      width: 165px; height: 14px; border-radius: 50%;
      background: radial-gradient(ellipse,#8c96a6,#20293a 70%);
    }}
    .launch .rocket-wrap {{ animation: liftoff 2.4s ease-in forwards; }}
    .launch .flame {{ animation: flame .13s 18 alternate; }}
    .failure .rocket-wrap {{ animation: shake .12s 18 alternate; }}
    .failure .flame {{ animation: sputter .18s 12 alternate; }}
    @keyframes liftoff {{
      0% {{ bottom: 42px; }}
      20% {{ bottom: 52px; }}
      100% {{ bottom: 370px; }}
    }}
    @keyframes flame {{
      from {{ transform: scaleY(.82); }}
      to {{ transform: scaleY(1.18); }}
    }}
    @keyframes shake {{
      from {{ transform: translateX(calc(-50% - 4px)) rotate(-1.5deg); }}
      to {{ transform: translateX(calc(-50% + 4px)) rotate(1.5deg); }}
    }}
    @keyframes sputter {{
      from {{ transform: scaleY(.35); opacity: .25; }}
      to {{ transform: scaleY(.95); opacity: .9; }}
    }}
    </style>
    </head>
    <body>
      <div class="scene {state}">
        <div class="pad"></div>
        <div class="rocket-wrap">
          <div class="rocket">
            <div class="nose"></div>
            <div class="body"></div>
            <div class="band"></div>
            <div class="window"></div>
            <div class="fin-left"></div>
            <div class="fin-right"></div>
            <div class="nozzle"></div>
            <div class="flame"></div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

    components.html(rocket_html, height=345, scrolling=False)

    st.markdown(
        f'<div class="result-card">'
        f'<div class="result-label">System status</div>'
        f'<div class="result-value {result_class}">{status}</div>'
        f'<div class="small-note">Model confidence: {confidence:.1%}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    c1.metric("Violation risk", f"{probability:.1%}")
    c2.metric("Safe probability", f"{1-probability:.1%}")

    if prediction:
        st.warning("Review this configuration: the model associated it with the violation class.")
    else:
        st.success("The model did not detect a physics violation in this configuration.")

    with st.expander("View all selected values"):
        st.dataframe(inputs.T.rename(columns={0: "Selected value"}), use_container_width=True)

st.caption(
    "Educational demonstration only. This model does not replace engineering analysis, simulation, or physical testing."
)
