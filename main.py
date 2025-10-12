import math
# Pirmā versija - programma, kas spēj izrēķināt pāris nezināmos, lietojot formulas


# input

def get_properties():
    variable_prompts = {
        "x0": "Ierakstiet sākuma x koordinātu",
        "y0": "Ierakstiet sākuma y koordinātu",
        "x": "Ierakstiet momentāno x koordinātu",
        "y": "Ierakstiet momentāno y koordinātu",
        "v0x": "Ierakstiet sākuma x ātrumu",
        "v0y": "Ierakstiet sākuma y ātrumu",
        "vx": "Ierakstiet momentāno x ātrumu",
        "vy": "Ierakstiet momentāno y ātrumu",
        "t": "Ierakstiet laiku, kopš kustības sākuma",
        "ax": "Ierakstiet x paātrinājumu",
        "ay": "Ierakstiet y paātrinājumu",
        "alpha": "Ierakstiet leņķi pret horizontu (grādos)",
        "v0": "Ierakstiet sākuma ātrumu (v0)",
    }

    variables = {}

    for var, prompt in variable_prompts.items():
        val = input(f"{prompt} (Atstāt tukšu, ja nezināms): ").strip()
        if val == "":
            variables[var] = {"value": None, "known": False}
        else:
            try:
                num = float(val)
                variables[var] = {"value": num, "known": True}
            except ValueError:
                print(f"[INFO]'{val}' nav skaitlis. Tiek pieņemts par nezināmu.")
                variables[var] = {"value": None, "known": False}

    return variables

# check

def try_solve(formula_name, required_vars, solve_fn, variables):
    known_vars = [v for v in required_vars if variables[v]["known"]]
    unknown_vars = [v for v in required_vars if not variables[v]["known"]]

    if len(unknown_vars) == 0:
        # Tāpat pārbaudīšu.
        try:
            result = solve_fn(variables)
            print(f"Pārbaude: {formula_name} → {result}")
        except Exception as e:
            print(f"[ERROR] Pārbaude neizdevās! {formula_name}: {e}")
    elif len(unknown_vars) == 1:
        # One unknown — solve it
        target = unknown_vars[0]
        try:
            result = solve_fn(variables, solve_for=target)
            if result is not None:
                variables[target]["value"] = result
                variables[target]["known"] = True
                print(f"[INFO] {target} = {result}")
        except Exception as e:
            print(f"[ERROR] Solving {formula_name} for {target}: {e}")
    else:
        print(f"[WARN] {formula_name} — pārāk daudz nezināmo: {unknown_vars}")
# formulas
# sāku ar v0 formulām, jo tajās ir mazāk mainīgo

def formula_v0x(v, solve_for=None):
    v0 = v["v0"]["value"]
    alpha = math.radians(v["alpha"]["value"])
    if solve_for is None or solve_for == "v0x":
        return v0 * math.cos(alpha)
    elif solve_for == "v0":
        return v["v0x"]["value"] / math.cos(alpha)
    elif solve_for == "alpha":
        return math.degrees(math.acos(v["v0x"]["value"] / v0))
    return None

def formula_v0y(v, solve_for=None):
    v0 = v["v0"]["value"]
    alpha = math.radians(v["alpha"]["value"])
    if solve_for is None or solve_for == "v0y":
        return v0 * math.sin(alpha)
    elif solve_for == "v0":
        return v["v0y"]["value"] / math.sin(alpha)
    elif solve_for == "alpha":
        return math.degrees(math.asin(v["v0y"]["value"] / v0))
    return None

def formula_x(v, solve_for=None):
    x0 = v["x0"]["value"]
    v0x = v["v0x"]["value"]
    t = v["t"]["value"]
    ax = v["ax"]["value"]
    if solve_for is None or solve_for == "x":
        return x0 + v0x * t + 0.5 * ax * t**2
    return None

def formula_y(v, solve_for=None):
    y0 = v["y0"]["value"]
    v0y = v["v0y"]["value"]
    t = v["t"]["value"]
    ay = v["ay"]["value"]
    if solve_for is None or solve_for == "y":
        return y0 + v0y * t + 0.5 * ay * t**2
    return None

# ja viss ir, tad mēģinam izrēķināt

def run_all_formulas(variables):
    try_solve("v0x = v0 * cos(alpha)", ["v0x", "v0", "alpha"], formula_v0x, variables)
    try_solve("v0y = v0 * sin(alpha)", ["v0y", "v0", "alpha"], formula_v0y, variables)
    try_solve("x = x0 + v0x*t + 0.5*ax*t²", ["x", "x0", "v0x", "t", "ax"], formula_x, variables)
    try_solve("y = y0 + v0y*t + 0.5*ay*t²", ["y", "y0", "v0y", "t", "ay"], formula_y, variables)

# Galvenā funkcija

def main():
    print("Brīvā kritienā esoša masas punkta kustības simulācija divās dimensijās")
    variables = get_properties()
    print("\nMēģinu atrisināt zināmās formulas...\n")
    run_all_formulas(variables)

    print("\nGala rezultāti:")
    for name, data in variables.items():
        val = data["value"]
        status = "zināms" if data["known"] else "nezināms"
        print(f"{name}: {val if data['known'] else '---'} ({status})")

if __name__ == "__main__":
    main()

# Kods izveidots, prasot palīdzību ChatGPT optimizācijas jautājumos. Struktūra un funkcijas izdomāju pats.

