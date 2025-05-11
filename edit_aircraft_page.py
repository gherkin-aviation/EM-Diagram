import dash
from dash import dcc, html
import json
import os
from dash.exceptions import PreventUpdate

def load_aircraft_data_from_folder():
    folder_path = os.path.join(os.path.dirname(__file__), "aircraft_data")
    aircraft_data = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r") as f:
                try:
                    data = json.load(f)
                    name = os.path.splitext(filename)[0].replace("_", " ")
                    aircraft_data[name] = data
                except Exception as e:
                    print(f"[ERROR] Failed to load {filename}: {e}")
    return aircraft_data

# ✅ Load it once for this page
aircraft_data = load_aircraft_data_from_folder()

# --- Full Edit Aircraft Page Layout ---
def edit_aircraft_layout():
    return html.Div([
        dcc.Store(id="stored-flap-configs", data=[]),
        dcc.Store(id="stored-g-limits", data=[]),
        dcc.Store(id="stored-stall-speeds", data=[]),
        dcc.Store(id="stored-single-engine-limits", data=[]),
        dcc.Store(id="stored-engine-options", data=[]),
        dcc.Store(id="stored-other-limits", data={}),
        dcc.Store(id="stored-oei-performance", data=[]),

        html.Button("⬅️ Back to EM Diagram", id="back-button", n_clicks=0, style={"marginBottom": "20px"}),
        html.H1("Edit / Create Aircraft", style={"marginBottom": "20px"}),

        html.Div([
            html.Label("Search Aircraft"),
            dcc.Dropdown(
                id="aircraft-search",
                options=[{"label": name, "value": name} for name in aircraft_data.keys()],
                placeholder="Start typing...",
                searchable=True,
                style={"width": "300px", "marginBottom": "10px"}
            ),
            html.Button("New Aircraft", id="new-aircraft-button", n_clicks=0, style={"marginLeft": "10px"}),
            html.Button("💾 Save Aircraft", id="save-aircraft-button", n_clicks=0, style={"marginLeft": "10px", "backgroundColor": "#007bff", "color": "white", "fontWeight": "bold"}),
            html.Div(id="search-result", style={"marginTop": "10px", "color": "green"})
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "20px"}),
        
        
        html.Div([
            html.Label("Apply Default Performance Values:", style={"fontWeight": "bold", "marginBottom": "5px"}),

            html.Div([
                html.Button("Single Engine", id="default-single", n_clicks=0, style={"marginRight": "10px"}),
                html.Button("Multi Engine", id="default-multi", n_clicks=0, style={"marginRight": "10px"}),
                html.Button("Aerobatic", id="default-aerobatic", n_clicks=0, style={"marginRight": "10px"}),
                html.Button("Trainer", id="default-trainer", n_clicks=0, style={"marginRight": "10px"}),
                html.Button("Military Trainer", id="default-mil-trainer", n_clicks=0, style={"marginRight": "10px"}),
                html.Button("Experimental", id="default-experimental", n_clicks=0)
            ], style={"marginBottom": "20px", "display": "flex", "flexWrap": "wrap"})
        ]),

        html.Div([
            html.Label("Units:"),
            dcc.RadioItems(
                id="units-toggle",
                options=[
                    {"label": "KIAS", "value": "KIAS"},
                    {"label": "MPH", "value": "MPH"}
                ],
                value="KIAS",
                labelStyle={"display": "inline-block", "marginRight": "15px"}
            )
        ], style={"marginBottom": "20px"}),

        html.Div([
            html.Label("Aircraft Name"),
            dcc.Input(id="aircraft-name", type="text", style={"width": "300px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Aircraft Type"),
            dcc.Dropdown(
                id="aircraft-type",
                options=[
                    {"label": "Single Engine", "value": "single_engine"},
                    {"label": "Multi Engine", "value": "multi_engine"}
                ],
                placeholder="Select type",
                style={"width": "200px"}
            )
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Engine Count"),
            dcc.Input(id="engine-count", type="number", min=1, step=1, style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Wing Area (ft²)"),
            dcc.Input(id="wing-area", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Aspect Ratio"),
            dcc.Input(id="aspect-ratio", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("CD0 (Parasite Drag Coefficient)"),
            dcc.Input(id="cd0", type="number", step=0.001, style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Oswald Efficiency Factor (e)"),
            dcc.Input(id="oswald-efficiency", type="number", step=0.01, style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Empty Weight (lbs)"),
            dcc.Input(id="empty-weight", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Max Gross Weight (lbs)"),
            dcc.Input(id="max-weight", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Number of Seats"),
            dcc.Input(id="seats", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("CG Range (inches)"),
            html.Div([
                html.Label("FWD", style={"marginRight": "10px"}),
                dcc.Input(id="cg-fwd", type="number", style={"width": "80px", "marginRight": "20px"}),
                html.Label("AFT", style={"marginRight": "10px"}),
                dcc.Input(id="cg-aft", type="number", style={"width": "80px"})
            ], style={"display": "flex", "alignItems": "center"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Fuel Capacity (gal)"),
            dcc.Input(id="fuel-capacity-gal", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Fuel Weight per Gallon (lbs)"),
            dcc.Input(id="fuel-weight-per-gal", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Vne (Never Exceed Speed)"),
            dcc.Input(id="vne", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Vno (Max Structural Cruising Speed)"),
            dcc.Input(id="vno", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Best Glide Speed (KIAS)"),
            dcc.Input(id="best-glide", type="number", style={"width": "100px"})
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Best Glide Ratio"),
            dcc.Input(id="best-glide-ratio", type="number", step=0.1, style={"width": "100px"})
        ], style={"marginBottom": "15px"}),
        
        html.Div([
            html.Label("Service Ceiling (ft)"),
            dcc.Input(
                id="max-altitude",
                type="number",
                placeholder="e.g. 18000",
                style={"width": "120px"}
            )
        ], style={"marginBottom": "15px"}),

        html.Div([
            html.Label("Airspeed Arcs", style={"fontWeight": "bold"}),

            html.Div([
                html.Label("White Arc:"),
                dcc.Input(id="arc-white-bottom", type="number", placeholder="Bottom", style={"width": "80px", "marginRight": "10px"}),
                dcc.Input(id="arc-white-top", type="number", placeholder="Top", style={"width": "80px"})
            ], style={"marginBottom": "10px"}),

            html.Div([
                html.Label("Green Arc:"),
                dcc.Input(id="arc-green-bottom", type="number", placeholder="Bottom", style={"width": "80px", "marginRight": "10px"}),
                dcc.Input(id="arc-green-top", type="number", placeholder="Top", style={"width": "80px"})
            ], style={"marginBottom": "10px"}),

            html.Div([
                html.Label("Yellow Arc:"),
                dcc.Input(id="arc-yellow-bottom", type="number", placeholder="Bottom", style={"width": "80px", "marginRight": "10px"}),
                dcc.Input(id="arc-yellow-top", type="number", placeholder="Top", style={"width": "80px"})
            ], style={"marginBottom": "10px"}),

            html.Div([
                html.Label("Red Line:"),
                dcc.Input(id="arc-red", type="number", placeholder="Red", style={"width": "80px"})
            ])
        ], style={"marginBottom": "20px"}),

        html.Div([
            html.Label("Prop Thrust Decay", style={"fontWeight": "bold"}),
            html.Div([
                html.Label("T_static Factor"),
                dcc.Input(id="prop-static-factor", type="number", step=0.1, style={"width": "100px", "marginRight": "15px"}),
                html.Label("V_max"),
                dcc.Input(id="prop-vmax-kts", type="number", style={"width": "100px"})
            ])
        ], style={"marginBottom": "20px"}),

        html.Div([
            html.Label("Flap Configurations (Standardized)", style={"fontWeight": "bold", "marginBottom": "10px"}),
            html.Div(id="flap-configs-container", children=[
                html.Div([
                    html.Label("Clean / Up", style={"width": "100px", "display": "inline-block"}),
                    html.Div(style={"width": "100px", "marginRight": "10px", "display": "inline-block"}),
                    dcc.Input(
                        id={"type": "clmax-input", "config": "clean"},
                        type="number",
                        placeholder="CLmax",
                        step=0.01,
                        style={"width": "100px"}
                    )
                ], style={"marginBottom": "10px"}),

                html.Div([
                    html.Label("Takeoff / Approach / 10-20°", style={"width": "100px", "display": "inline-block"}),
                    dcc.Input(
                        id={"type": "vfe-input", "config": "takeoff"},
                        type="number",
                        placeholder="Vfe",
                        style={"width": "100px", "marginRight": "10px"}
                    ),
                    dcc.Input(
                        id={"type": "clmax-input", "config": "takeoff"},
                        type="number",
                        placeholder="CLmax",
                        step=0.01,
                        style={"width": "100px"}
                    )
                ], style={"marginBottom": "10px"}),

                html.Div([
                    html.Label("Landing / Full / 30-40°", style={"width": "100px", "display": "inline-block"}),
                    dcc.Input(
                        id={"type": "vfe-input", "config": "landing"},
                        type="number",
                        placeholder="Vfe",
                        style={"width": "100px", "marginRight": "10px"}
                    ),
                    dcc.Input(
                        id={"type": "clmax-input", "config": "landing"},
                        type="number",
                        placeholder="CLmax",
                        step=0.01,
                        style={"width": "100px"}
                    )
                ], style={"marginBottom": "10px"})
            ])
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.H3("G Limits"),
            html.Div(id="g-limits-container", children=[]),
            html.Button("➕ Add G Limit", id="add-g-limit", n_clicks=0, style={"marginTop": "10px"})
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.H3("Stall Speeds"),
            html.Div(id="stall-speeds-container", children=[]),
            html.Button("➕ Add Stall Speed", id="add-stall-speed", n_clicks=0, style={"marginTop": "10px"})
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.H3("Single Engine Limits (Vmca / Vyse / Vxse)"),
            html.Div(id="single-engine-limits-container"),
            html.Button("➕ Add Single Engine Limit", id="add-single-engine-limit", n_clicks=0, style={"marginTop": "10px"})
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.H3("OEI (One Engine Inoperative) Performance"),
            html.Div(id="oei-performance-container"),
            html.Button("➕ Add OEI Performance", id="add-oei-performance", n_clicks=0, style={"marginTop": "10px"})
        ], style={"marginBottom": "30px"}),
        
        html.Div([
            html.H3("Engine / Prop Options"),
            html.Div(id="engine-options-container"),
            html.Button("➕ Add Engine Option", id="add-engine-option", n_clicks=0, style={"marginTop": "10px"})
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.Label("Power Curve", style={"fontWeight": "bold", "marginBottom": "5px"}),

            html.Div([
                html.Label("Sea Level Max HP", style={"width": "150px", "display": "inline-block"}),
                dcc.Input(
                    id="power-curve-sea-level",
                    type="number",
                    placeholder="e.g. 180",
                    style={"width": "120px", "marginRight": "20px"}
                ),

                html.Label("Max Altitude (ft)", style={"width": "150px", "display": "inline-block"}),
                dcc.Input(
                    id="power-curve-max-alt",
                    type="number",
                    placeholder="e.g. 12000",
                    style={"width": "120px", "marginRight": "20px"}
                ),

                html.Label("Derate per 1000 ft", style={"width": "180px", "display": "inline-block"}),
                dcc.Input(
                    id="power-curve-derate",
                    type="number",
                    placeholder="e.g. 0.03",
                    step=0.001,
                    style={"width": "100px"}
                )
            ], style={"display": "flex", "alignItems": "center", "flexWrap": "wrap"})
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.Label("Prop Condition Profiles", style={"fontWeight": "bold", "marginBottom": "5px"}),

            html.Div([
                html.Label("Normal", style={"width": "80px", "display": "inline-block"}),
                dcc.Input(
                    id="prop-normal-drag",
                    type="number",
                    placeholder="Drag Factor",
                    step=0.01,
                    style={"width": "120px", "marginRight": "10px"}
                ),
                dcc.Input(
                    id="prop-normal-eff",
                    type="number",
                    placeholder="Prop Eff.",
                    step=0.01,
                    style={"width": "120px"}
                )
            ], style={"marginBottom": "10px"}),

            html.Div([
                html.Label("Windmilling", style={"width": "80px", "display": "inline-block"}),
                dcc.Input(
                    id="prop-wind-drag",
                    type="number",
                    placeholder="Drag Factor",
                    step=0.01,
                    style={"width": "120px", "marginRight": "10px"}
                ),
                dcc.Input(
                    id="prop-wind-eff",
                    type="number",
                    placeholder="Prop Eff.",
                    step=0.01,
                    style={"width": "120px"}
                )
            ], style={"marginBottom": "10px"}),

            html.Div([
                html.Label("Stationary", style={"width": "80px", "display": "inline-block"}),
                dcc.Input(
                    id="prop-stop-drag",
                    type="number",
                    placeholder="Drag Factor",
                    step=0.01,
                    style={"width": "120px", "marginRight": "10px"}
                ),
                dcc.Input(
                    id="prop-stop-eff",
                    type="number",
                    placeholder="Prop Eff.",
                    step=0.01,
                    style={"width": "120px"}
                )
            ])
        ], style={"marginBottom": "30px"}),

        html.Div([
            html.H3("Other Limits"),
            html.Div(id="other-limits-container"),
            html.Button("➕ Add Other Limit", id="add-other-limit", n_clicks=0, style={"marginTop": "10px"})
        ], style={"marginBottom": "30px"}),

        html.Button("💾 Save Aircraft", id="save-aircraft-button", n_clicks=0, style={"marginTop": "20px"}),
        html.Div(id="save-status", style={"marginTop": "10px", "color": "green"})
    ])
