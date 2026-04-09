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

logging.info("Program started.")

g = -9.81  # gravitational acceleration


# --- Input ---
def get_initial_conditions():
    def ask_float(prompt, default=None):
        val = input(prompt).strip()
        if val == "":
            return default
        try:
            return float(val)
        except ValueError:
            print("[WARN] Invalid input, using default.")
            return default

    h0 = ask_float("Initial height h0 (m): ", 10)
    v0 = ask_float("Initial vertical velocity v0 (m/s) [default 0]: ", 0)
    a = ask_float("Acceleration (m/s²) [default -9.81]: ", g)

    return h0, v0, a


# --- Simulation ---
def simulate_fall(h0, v0, a, dt=0.01):
    t = 0
    data = []

    while True:
        h = h0 + v0 * t + 0.5 * a * t**2
        v = v0 + a * t

        data.append((t, h, v))

        if h < 0:
            break

        t += dt

    logging.info(f"Simulation complete. Steps: {len(data)}")
    return data


# --- Interactive probe ---
def interactive_probe(sim_data):
    if not sim_data:
        print("[ERROR] No data.")
        return

    t_max = sim_data[-1][0]

    print(f"\nEnter time (0 to {round(t_max, 2)} s). Press Enter to exit.\n")

    while True:
        val = input("t = ").strip()
        if val == "":
            print("Exiting probe.")
            break

        try:
            t_query = float(val)
            if t_query < 0 or t_query > t_max:
                print("[WARN] Out of range.")
                continue

            times = [row[0] for row in sim_data]
            idx = min(range(len(times)), key=lambda i: abs(times[i] - t_query))

            t, h, v = sim_data[idx]

            print(f"\nt = {round(t,2)} s")
            print(f"  height = {round(h,2)} m")
            print(f"  velocity = {round(v,2)} m/s")
            print(f"  acceleration = constant ({round(g,2)} m/s²)\n")

        except ValueError:
            print("[WARN] Enter a number.")


# --- Plot ---
def plot_height(sim_data):
    ts = [row[0] for row in sim_data]
    hs = [row[1] for row in sim_data]

    plt.figure()
    plt.plot(ts, hs)
    plt.xlabel("Time (s)")
    plt.ylabel("Height (m)")
    plt.title("Free fall motion h(t)")
    plt.grid(True)
    plt.show()


# --- Main ---
def main():
    h0, v0, a = get_initial_conditions()
    sim_data = simulate_fall(h0, v0, a)

    plot_height(sim_data)
    interactive_probe(sim_data)

    logging.info("Program finished.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[FATAL ERROR]", e)
        logging.critical(f"Unhandled error: {e}")

# Koda izveidošana un optimizēšana atvieglināta, lietojot ChatGPT 5.
