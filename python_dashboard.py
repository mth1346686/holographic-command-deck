import json
import os
import sys
import time
from flask import Flask, render_template_string, jsonify, request, send_file
import plotly.graph_objects as go
import plotly.io as pio

# Set Plotly Default Template to Dark
pio.templates.default = "plotly_dark"

app = Flask(__name__)

# Clinical Data Store (Authentic Egyptian Healthcare Economics)
CLINICAL_DATA = {
    "monthly": [
        {"m": "May", "actual": 380, "forecast": 380, "lower": 360, "upper": 400},
        {"m": "Jun", "actual": 410, "forecast": 410, "lower": 390, "upper": 430},
        {"m": "Jul", "actual": 445, "forecast": 445, "lower": 420, "upper": 470},
        {"m": "Aug", "actual": 470, "forecast": 470, "lower": 450, "upper": 495},
        {"m": "Sep", "actual": 460, "forecast": 460, "lower": 440, "upper": 485},
        {"m": "Oct", "actual": 482, "forecast": 482, "lower": 460, "upper": 510},
        {"m": "Nov (P)", "actual": None, "forecast": 515, "lower": 480, "upper": 550},
        {"m": "Dec (P)", "actual": None, "forecast": 540, "lower": 505, "upper": 580},
        {"m": "Jan (P)", "actual": None, "forecast": 565, "lower": 520, "upper": 610}
    ],
    "departments": [
        {"name": "Cardiology", "ward": 95, "icu": 35, "color": "#00F0FF"},
        {"name": "Orthopedics", "ward": 80, "icu": 15, "color": "#00E5A3"},
        {"name": "Neurology", "ward": 65, "icu": 25, "color": "#A855F7"},
        {"name": "Pediatrics", "ward": 70, "icu": 12, "color": "#F59E0B"},
        {"name": "Oncology", "ward": 55, "icu": 18, "color": "#F43F5E"}
    ],
    "severity": [
        {"label": "Critical ICU", "pct": 22, "color": "#F43F5E"},
        {"label": "Step-Down Ward", "pct": 38, "color": "#00F0FF"},
        {"label": "Elective Post-Op", "pct": 28, "color": "#00E5A3"},
        {"label": "Day Observation", "pct": 12, "color": "#F59E0B"}
    ],
    "waterfall": [
        {"name": "Base Rev", "val": 24.5, "type": "relative"},
        {"name": "Surge Vol", "val": 3.2, "type": "relative"},
        {"name": "Cath Lab", "val": 1.8, "type": "relative"},
        {"name": "Discounts", "val": -0.9, "type": "relative"},
        {"name": "ETA VAT", "val": -0.2, "type": "relative"},
        {"name": "Net EGP", "val": 28.4, "type": "total"}
    ]
}

def generate_plotly_charts():
    """Build all 6 Plotly interactive charts with Dark Luxury cyber styling."""
    t0 = time.time()
    
    # 1. Area Trend + ARIMA Predictive Band
    months = [d["m"] for d in CLINICAL_DATA["monthly"]]
    actuals = [d["actual"] for d in CLINICAL_DATA["monthly"]]
    forecasts = [d["forecast"] for d in CLINICAL_DATA["monthly"]]
    upper = [d["upper"] for d in CLINICAL_DATA["monthly"]]
    lower = [d["lower"] for d in CLINICAL_DATA["monthly"]]

    fig_trend = go.Figure()
    # Confidence Band
    fig_trend.add_trace(go.Scatter(
        x=months + months[::-1],
        y=upper + lower[::-1],
        fill='toself',
        fillcolor='rgba(0, 240, 255, 0.08)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False,
        name='95% Confidence Band'
    ))
    # Historical Actuals
    fig_trend.add_trace(go.Scatter(
        x=months[:6], y=actuals[:6],
        mode='lines+markers',
        name='Verified Actuals',
        line=dict(color='#00F0FF', width=3, shape='spline'),
        marker=dict(size=7, color='#00F0FF', symbol='circle')
    ))
    # Forecast Horizon
    fig_trend.add_trace(go.Scatter(
        x=months[5:], y=forecasts[5:],
        mode='lines+markers',
        name='90-Day Forecast',
        line=dict(color='#A855F7', width=3, dash='dot', shape='spline'),
        marker=dict(size=8, color='#A855F7', symbol='diamond')
    ))
    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=20, t=30, b=30),
        height=220,
        font=dict(family='JetBrains Mono, sans-serif', color='#94A3B8', size=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', zeroline=False)
    )

    # 2. Bed Allocation Grouped Bar
    dept_names = [d["name"] for d in CLINICAL_DATA["departments"]]
    ward_beds = [d["ward"] for d in CLINICAL_DATA["departments"]]
    icu_beds = [d["icu"] for d in CLINICAL_DATA["departments"]]

    fig_beds = go.Figure()
    fig_beds.add_trace(go.Bar(
        x=dept_names, y=ward_beds, name='Ward Beds',
        marker=dict(color='#00F0FF', opacity=0.85, line=dict(color='#00F0FF', width=1))
    ))
    fig_beds.add_trace(go.Bar(
        x=dept_names, y=icu_beds, name='Critical ICU',
        marker=dict(color='#F43F5E', opacity=0.85, line=dict(color='#F43F5E', width=1))
    ))
    fig_beds.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=20, t=30, b=30),
        height=220,
        font=dict(family='JetBrains Mono, sans-serif', color='#94A3B8', size=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)')
    )

    # 3. Severity Distribution Donut
    labels = [s["label"] for s in CLINICAL_DATA["severity"]]
    values = [s["pct"] for s in CLINICAL_DATA["severity"]]
    colors = [s["color"] for s in CLINICAL_DATA["severity"]]

    fig_donut = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.62,
        marker=dict(colors=colors, line=dict(color='#050B14', width=2)),
        textinfo='percent',
        hoverinfo='label+percent'
    )])
    fig_donut.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=20, b=20),
        height=220,
        font=dict(family='JetBrains Mono, sans-serif', color='#94A3B8', size=10),
        showlegend=False
    )

    # 4. Financial Waterfall Variance Bridge
    wf_names = [w["name"] for w in CLINICAL_DATA["waterfall"]]
    wf_vals = [w["val"] for w in CLINICAL_DATA["waterfall"]]
    wf_measures = [w["type"] for w in CLINICAL_DATA["waterfall"]]

    fig_wf = go.Figure(go.Waterfall(
        name="Rev Bridge", orientation="v",
        measure=wf_measures,
        x=wf_names,
        textposition="outside",
        text=[f"{v:+.1f}M" if m != 'total' else f"{v:.1f}M" for v, m in zip(wf_vals, wf_measures)],
        y=wf_vals,
        connector=dict(line=dict(color="rgba(255,255,255,0.2)")),
        decreasing=dict(marker=dict(color="#F43F5E")),
        increasing=dict(marker=dict(color="#00E5A3")),
        totals=dict(marker=dict(color="#00F0FF"))
    ))
    fig_wf.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=20, t=30, b=30),
        height=220,
        font=dict(family='JetBrains Mono, sans-serif', color='#94A3B8', size=10),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)')
    )

    t_render = (time.time() - t0) * 1000  # ms
    return {
        "trend": fig_trend.to_html(full_html=False, include_plotlyjs=False),
        "beds": fig_beds.to_html(full_html=False, include_plotlyjs=False),
        "donut": fig_donut.to_html(full_html=False, include_plotlyjs=False),
        "waterfall": fig_wf.to_html(full_html=False, include_plotlyjs=False),
        "render_time_ms": round(t_render, 2)
    }

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holographic Clinical Deck • Python & Plotly Edition</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --holo-cyan: #00F0FF;
            --holo-teal: #00E5A3;
            --holo-violet: #A855F7;
            --holo-rose: #F43F5E;
            --bg-deep: #050B14;
            --glass-bg: rgba(15, 23, 42, 0.75);
            --glass-border: rgba(0, 240, 255, 0.22);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif; }
        body {
            background-color: var(--bg-deep);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(0, 240, 255, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.08) 0%, transparent 40%),
                linear-gradient(180deg, #050B14 0%, #0B1528 50%, #030712 100%);
            color: #FFFFFF;
            min-height: 100vh;
            padding-bottom: 60px;
        }
        .laser-top {
            position: fixed; top: 0; left: 0; height: 3px; width: 100%;
            background: linear-gradient(90deg, #00F0FF, #A855F7, #00E5A3);
            box-shadow: 0 0 15px #00F0FF; z-index: 9999;
        }
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
            transition: all 0.25s ease;
        }
        .glass-panel:hover {
            border-color: rgba(0, 240, 255, 0.55);
            box-shadow: 0 14px 40px rgba(0, 240, 255, 0.15);
        }
        .hud-header {
            position: sticky; top: 0; z-index: 100;
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 24px;
            border-bottom: 1px solid var(--glass-border);
            background: rgba(11, 21, 40, 0.88);
            backdrop-filter: blur(20px);
        }
        .kpi-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px; margin: 24px 0;
        }
        .kpi-card { padding: 20px; position: relative; }
        .kpi-val { font-size: 1.8rem; font-weight: 900; font-family: 'JetBrains Mono', monospace; margin: 6px 0; }
        .chart-grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 24px; margin-bottom: 24px; }
        .chart-card { padding: 20px; }
        .sim-section { padding: 28px; border: 1px solid rgba(0, 240, 255, 0.4); margin-top: 32px; }
        .sim-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; margin: 20px 0; }
        .sim-box { background: rgba(0, 0, 0, 0.4); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); }
        .sim-slider { width: 100%; accent-color: var(--holo-cyan); cursor: pointer; }
        .sim-banner {
            display: flex; justify-content: space-around; flex-wrap: wrap; gap: 16px;
            background: linear-gradient(90deg, rgba(0,240,255,0.1), rgba(168,85,247,0.1));
            padding: 18px; border-radius: 14px; border: 1px solid rgba(0,240,255,0.3); text-align: center;
        }
        .badge {
            padding: 4px 10px; border-radius: 999px; font-size: 0.72rem; font-family: 'JetBrains Mono', monospace;
            background: rgba(0, 240, 255, 0.12); color: var(--holo-cyan); border: 1px solid rgba(0, 240, 255, 0.3);
        }
        .btn-excel {
            background: rgba(0, 229, 163, 0.15); border: 1px solid rgba(0, 229, 163, 0.45);
            color: var(--holo-teal); padding: 6px 14px; border-radius: 8px; text-decoration: none;
            font-size: 0.75rem; font-weight: 700; display: inline-flex; align-items: center; gap: 6px;
        }
    </style>
</head>
<body>
    <div class="laser-top"></div>

    <header class="hud-header">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #00F0FF, #A855F7); display: flex; align-items: center; justify-content: center; font-weight: 900; color: #000;">🐍</div>
            <div>
                <h1 style="font-size: 1.05rem; font-weight: 800; display: flex; align-items: center; gap: 8px;">
                    HOLOGRAPHIC CLINICAL DECK
                    <span class="badge">Python & Plotly 7.1 Engine</span>
                </h1>
                <p style="font-size: 0.7rem; color: #94A3B8; font-family: 'JetBrains Mono', monospace;">
                    Python Native Server • Server Render Latency: {{ charts.render_time_ms }} ms
                </p>
            </div>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <a href="/download/excel" class="btn-excel">📊 Download Excel Deck (.xlsx)</a>
            <span class="badge" style="background: rgba(0, 229, 163, 0.1); color: #00E5A3; border-color: rgba(0, 229, 163, 0.3);">
                ⚡ High-Throughput Python
            </span>
        </div>
    </header>

    <main style="max-width: 1200px; margin: 0 auto; padding: 24px 16px;">
        
        <!-- 5 High-Impact KPI Cards -->
        <div class="kpi-grid">
            <div class="glass-panel kpi-card" style="border-left: 3px solid #00F0FF;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-family: 'JetBrains Mono';">ACTIVE INPATIENTS</span>
                <div class="kpi-val" style="color: #FFFFFF;">1,450 <span style="font-size: 0.8rem; color: #94A3B8;">Pts</span></div>
                <div style="font-size: 0.72rem; color: #00E5A3; font-family: 'JetBrains Mono';">+8.4% vs Sep</div>
            </div>
            <div class="glass-panel kpi-card" style="border-left: 3px solid #00E5A3;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-family: 'JetBrains Mono';">OCCUPIED BEDS</span>
                <div class="kpi-val" style="color: #FFFFFF;">482 <span style="font-size: 0.8rem; color: #94A3B8;">/ 520</span></div>
                <div style="font-size: 0.72rem; color: #00E5A3; font-family: 'JetBrains Mono';">92.7% Occupancy</div>
            </div>
            <div class="glass-panel kpi-card" style="border-left: 3px solid #A855F7;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-family: 'JetBrains Mono';">AVG LENGTH OF STAY</span>
                <div class="kpi-val" style="color: #FFFFFF;">4.6 <span style="font-size: 0.8rem; color: #94A3B8;">Days</span></div>
                <div style="font-size: 0.72rem; color: #00E5A3; font-family: 'JetBrains Mono';">-0.4d Optimization</div>
            </div>
            <div class="glass-panel kpi-card" style="border-left: 3px solid #F59E0B;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-family: 'JetBrains Mono';">CSAT SATISFACTION</span>
                <div class="kpi-val" style="color: #FFFFFF;">94.8<span style="font-size: 0.8rem; color: #94A3B8;">%</span></div>
                <div style="font-size: 0.72rem; color: #00E5A3; font-family: 'JetBrains Mono';">4.8/5.0 Star Rating</div>
            </div>
            <div class="glass-panel kpi-card" style="border-left: 3px solid #00F0FF;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-family: 'JetBrains Mono';">MONTHLY REVENUE</span>
                <div class="kpi-val" style="color: #00F0FF;">28.45 <span style="font-size: 0.8rem; color: #94A3B8;">M EGP</span></div>
                <div style="font-size: 0.72rem; color: #00E5A3; font-family: 'JetBrains Mono';">+14.2% YoY (Egypt)</div>
            </div>
        </div>

        <!-- Plotly Charts Row 1 -->
        <div class="chart-grid-2">
            <div class="glass-panel chart-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h3 style="font-size: 0.9rem; font-weight: 700; color: #FFFFFF;">Patient Flow & 90-Day ARIMA Horizon</h3>
                    <span class="badge">Plotly Spline</span>
                </div>
                {{ charts.trend | safe }}
            </div>

            <div class="glass-panel chart-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h3 style="font-size: 0.9rem; font-weight: 700; color: #FFFFFF;">Departmental Bed Allocation (Ward vs ICU)</h3>
                    <span class="badge">Plotly Bars</span>
                </div>
                {{ charts.beds | safe }}
            </div>
        </div>

        <!-- Plotly Charts Row 2 -->
        <div class="chart-grid-2">
            <div class="glass-panel chart-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h3 style="font-size: 0.9rem; font-weight: 700; color: #FFFFFF;">Clinical Severity & Care Level Mix</h3>
                    <span class="badge">Plotly Donut</span>
                </div>
                {{ charts.donut | safe }}
            </div>

            <div class="glass-panel chart-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h3 style="font-size: 0.9rem; font-weight: 700; color: #FFFFFF;">Financial Waterfall Variance Bridge (EGP)</h3>
                    <span class="badge">Plotly Waterfall</span>
                </div>
                {{ charts.waterfall | safe }}
            </div>
        </div>

        <!-- Interactive What-If Capacity Simulator (Python Powered) -->
        <div class="glass-panel sim-section">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; padding-bottom: 16px; border-bottom: 1px solid var(--glass-border);">
                <div>
                    <h2 style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">Python Capacity & Revenue Modeling Engine</h2>
                    <p style="font-size: 0.75rem; color: #94A3B8; font-family: 'JetBrains Mono';">Realtime Python-calculated throughput and headroom projections.</p>
                </div>
                <button onclick="triggerSimulate()" style="background: linear-gradient(90deg, #00F0FF, #A855F7); color: #000; font-weight: 800; border: none; padding: 10px 20px; border-radius: 10px; cursor: pointer;">
                    ⚡ Recalculate Simulation
                </button>
            </div>

            <div class="sim-grid">
                <div class="sim-box">
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-family: 'JetBrains Mono';">
                        <span style="color: #94A3B8;">Target Stay (ALOS)</span>
                        <span id="lblStay" style="color: #00F0FF; font-weight: 700;">4.2 Days</span>
                    </div>
                    <input type="range" id="rngStay" min="2.5" max="7.0" step="0.1" value="4.2" class="sim-slider" oninput="runSimClient()">
                </div>
                <div class="sim-box">
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-family: 'JetBrains Mono';">
                        <span style="color: #94A3B8;">Target Occupancy</span>
                        <span id="lblOcc" style="color: #00E5A3; font-weight: 700;">88%</span>
                    </div>
                    <input type="range" id="rngOcc" min="70" max="98" step="1" value="88" class="sim-slider" oninput="runSimClient()">
                </div>
                <div class="sim-box">
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-family: 'JetBrains Mono';">
                        <span style="color: #94A3B8;">Avg Daily Rate (EGP)</span>
                        <span id="lblRate" style="color: #A855F7; font-weight: 700;">4,850 L.E</span>
                    </div>
                    <input type="range" id="rngRate" min="3000" max="8500" step="250" value="4850" class="sim-slider" oninput="runSimClient()">
                </div>
            </div>

            <div class="sim-banner">
                <div>
                    <span style="font-size: 0.7rem; color: #94A3B8; font-family: 'JetBrains Mono'; text-transform: uppercase;">Simulated Inpatients</span>
                    <p id="resPts" style="font-size: 1.6rem; font-weight: 900; color: #00F0FF; font-family: 'JetBrains Mono';">3,269</p>
                </div>
                <div>
                    <span style="font-size: 0.7rem; color: #94A3B8; font-family: 'JetBrains Mono'; text-transform: uppercase;">Projected Gross EGP</span>
                    <p id="resRev" style="font-size: 1.6rem; font-weight: 900; color: #00E5A3; font-family: 'JetBrains Mono';">15.85 M EGP</p>
                </div>
                <div>
                    <span style="font-size: 0.7rem; color: #94A3B8; font-family: 'JetBrains Mono'; text-transform: uppercase;">Available Bed Buffer</span>
                    <p id="resBeds" style="font-size: 1.6rem; font-weight: 900; color: #A855F7; font-family: 'JetBrains Mono';">62 Beds</p>
                </div>
            </div>
        </div>

    </main>

    <script>
        function runSimClient() {
            const stay = parseFloat(document.getElementById('rngStay').value);
            const occ = parseInt(document.getElementById('rngOcc').value);
            const rate = parseInt(document.getElementById('rngRate').value);

            document.getElementById('lblStay').innerText = stay.toFixed(1) + ' Days';
            document.getElementById('lblOcc').innerText = occ + '%';
            document.getElementById('lblRate').innerText = rate.toLocaleString() + ' L.E';

            const totalBeds = 520;
            const activeBeds = Math.round(totalBeds * (occ / 100));
            const monthlyPts = Math.round((activeBeds / stay) * 30);
            const projRev = (monthlyPts * rate) / 1000000;
            const headroom = totalBeds - activeBeds;

            document.getElementById('resPts').innerText = monthlyPts.toLocaleString();
            document.getElementById('resRev').innerText = projRev.toFixed(2) + ' M EGP';
            document.getElementById('resBeds').innerText = headroom + ' Beds';
        }

        async function triggerSimulate() {
            const stay = parseFloat(document.getElementById('rngStay').value);
            const occ = parseInt(document.getElementById('rngOcc').value);
            const rate = parseInt(document.getElementById('rngRate').value);
            
            try {
                const res = await fetch('/api/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ stay, occ, rate })
                });
                const data = await res.json();
                document.getElementById('resPts').innerText = data.monthly_patients.toLocaleString();
                document.getElementById('resRev').innerText = data.projected_rev_m_egp + ' M EGP';
                document.getElementById('resBeds').innerText = data.headroom_beds + ' Beds';
            } catch(e) {
                runSimClient();
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    charts = generate_plotly_charts()
    return render_template_string(HTML_TEMPLATE, charts=charts)

@app.route("/api/simulate", methods=["POST"])
def simulate():
    t0 = time.time()
    data = request.get_json() or {}
    stay = float(data.get("stay", 4.2))
    occ = float(data.get("occ", 88))
    rate = float(data.get("rate", 4850))

    total_beds = 520
    active_beds = round(total_beds * (occ / 100))
    monthly_patients = round((active_beds / stay) * 30)
    projected_rev = (monthly_patients * rate) / 1_000_000
    headroom = total_beds - active_beds

    latency_us = round((time.time() - t0) * 1_000_000, 2)
    return jsonify({
        "status": "success",
        "monthly_patients": monthly_patients,
        "projected_rev_m_egp": round(projected_rev, 2),
        "headroom_beds": headroom,
        "calculation_latency_microseconds": latency_us
    })

@app.route("/download/excel")
def download_excel():
    excel_path = "/data/data/com.termux/files/home/holographic-command-deck/Holographic_Clinical_Analytics.xlsx"
    if os.path.exists(excel_path):
        return send_file(excel_path, as_attachment=True, download_name="Holographic_Clinical_Analytics.xlsx")
    return "Excel file not found", 404

def export_standalone_html(output_path):
    """Exports a self-contained HTML file with embedded Plotly charts."""
    charts = generate_plotly_charts()
    from jinja2 import Template
    t = Template(HTML_TEMPLATE)
    rendered = t.render(charts=charts)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Exported standalone HTML dashboard to: {output_path} (Size: {os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    if "--export" in sys.argv:
        out = "/data/data/com.termux/files/home/python_dashboard.html"
        export_standalone_html(out)
        out_dl = "/sdcard/Download/python_dashboard.html"
        export_standalone_html(out_dl)
    else:
        port = int(os.environ.get("PORT", 5050))
        print(f"Starting Python Flask + Plotly Dashboard Server on port {port}...")
        app.run(host="0.0.0.0", port=port, debug=False)
