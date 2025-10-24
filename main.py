import math
import logging
import matplotlib.pyplot as plt

# --- Logging setup ---
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="w"
)
logging.info("[INFO] Programma startēta.")
# --- Input sākotnējo parametru iegūšana ---
def get_initial_conditions():
    def ask_float(prompt, default=None):
        val = input(prompt).strip()
        if val == "":
            return default
        try:
            return float(val)
        except ValueError:
            print("[WARN] Nederīga vērtība, izmantošu noklusējumu.")
            return default

    x0 = ask_float("Ierakstiet sākuma x koordinātu [m] (noklusējums 0): ", 0)
    y0 = ask_float("Ierakstiet sākuma y koordinātu [m] (noklusējums 0): ", 0)
    v0 = ask_float("Ierakstiet sākuma ātrumu [m/s]: ", None)
    alpha = ask_float("Ierakstiet leņķi pret horizontu (grādos): ", None)
    ax = ask_float("Ierakstiet x paātrinājumu [m/s²] (noklusējums 0): ", 0)
    ay = ask_float("Ierakstiet y paātrinājumu [m/s²] (noklusējums -9.81): ", -9.81)

    if v0 is None or alpha is None:
        print("[ERROR] Nepieciešams ievadīt gan v0, gan alpha!")
        logging.error("[ERROR] Missing v0 or alpha — cannot simulate.")
        return None

    return {"x0": x0, "y0": y0, "v0": v0, "alpha": alpha, "ax": ax, "ay": ay}


# --- Simulācija ---
def simulate_projectile(variables, dt=0.01):
    """
    Veic kustības simulāciju ar laika soli dt.
    Saglabā laiku, koordinātas, ātrumu un paātrinājumu katrā solī.
    Kad y < 0, interpolē precīzu trieciena brīdi (y = 0).
    """
    logging.info("Sāku simulāciju...")

    x0 = variables["x0"]["value"]
    y0 = variables["y0"]["value"]
    v0 = variables["v0"]["value"]
    alpha = math.radians(variables["alpha"]["value"])
    ax = variables["ax"]["value"]
    ay = variables["ay"]["value"]

    v0x = v0 * math.cos(alpha)
    v0y = v0 * math.sin(alpha)

    t = 0
    data = []

    while True:
        # Position update
        x = x0 + v0x * t + 0.5 * ax * t**2
        y = y0 + v0y * t + 0.5 * ay * t**2

        # Velocity update
        vx = v0x + ax * t
        vy = v0y + ay * t

        data.append((t, x, y, vx, vy))

        # Stop condition: projectile hits the ground
        if y < 0:
            # Linear interpolation for a clean impact at y = 0
            if len(data) >= 2:
                t1, x1, y1, _, _ = data[-2]
                t2, x2, y2, _, _ = data[-1]

                # Compute the exact impact time when y == 0
                if y2 != y1:
                    t_impact = t1 - y1 * (t2 - t1) / (y2 - y1)
                    x_impact = x0 + v0x * t_impact + 0.5 * ax * t_impact**2
                    vx_impact = v0x + ax * t_impact
                    vy_impact = v0y + ay * t_impact

                    # Replace the last entry with interpolated data
                    data[-1] = (t_impact, x_impact, 0.0, vx_impact, vy_impact)
                    logging.info(f"[INFO] Interpolēts trieciena punkts pie t={t_impact:.3f}s, x={x_impact:.3f}m")
            break

        t += dt

    logging.info(f"Simulācija pabeigta. Kopā soļu: {len(data)}")
    return data

# --- Interaktīvā analīze ---
def interactive_probe(sim_data):
    if not sim_data:
        print("[ERROR] Nav simulācijas datu.")
        return

    t_max = sim_data[-1][0]
    print(f"Ievadiet laiku (0 līdz {round(t_max, 2)} s), lai redzētu stāvokli.")
    print("Atstājiet tukšu, lai izietu.\n")

    while True:
        val = input("t = ").strip()
        if val == "":
            print("[INFO] Iziet no simulācijas apskates.")
            break
        try:
            t_query = float(val)
            if t_query < 0 or t_query > t_max:
                print(f"[WARN] Laiks ārpus diapazona (0 - {round(t_max,2)} s).")
                continue

            times = [row[0] for row in sim_data]
            idx = min(range(len(times)), key=lambda i: abs(times[i] - t_query))
            t, x, y, vx, vy = sim_data[idx]
            v = math.hypot(vx, vy)

            print(f"\nt={round(t,2)} s:")
            print(f"  x = {round(x,2)} m, y = {round(y,2)} m")
            print(f"  vx = {round(vx,2)} m/s, vy = {round(vy,2)} m/s")
            print(f"  Momentānais ātrums = {round(v,2)} m/s")
            print("  Paātrinājums ir konstants\n")

        except ValueError:
            print("[WARN] Ievadiet skaitlisku vērtību.")


# --- Grafiskā vizualizācija ---
def plot_trajectory(sim_data):
    xs = [row[1] for row in sim_data]
    ys = [row[2] for row in sim_data]

    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label="Trajektorija", color="royalblue")
    plt.scatter(xs[0], ys[0], color="green", label="Sākums")
    plt.scatter(xs[-1], ys[-1], color="red", label="Trieciena punkts")

    # Find peak (max height)
    peak_idx = ys.index(max(ys))
    plt.scatter(xs[peak_idx], ys[peak_idx], color="orange", label="Maksimālais augstums")

    plt.title("Masas punkta kustības trajektorija")
    plt.xlabel("Horizontālā distance (m)")
    plt.ylabel("Augstums (m)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


# --- Galvenā funkcija ---
def main():
    params = get_initial_conditions()
    if params is None:
        return

    sim_data = simulate_projectile(params)
    plot_trajectory(sim_data)
    interactive_probe(sim_data)
    logging.info("[INFO] Programma pabeidza izpildi.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        msg = f"Neapstrādāta kļūda: {e}"
        print(f"[FATAL] {msg}")
        logging.critical(msg)

# Koda izveidošana un optimizēšana atvieglināta, lietojot ChatGPT 5.