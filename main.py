import math
import logging
import matplotlib.pyplot as plt

# --- Logging setup ---
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="a"
)

logging.info("Program started.")

g = -9.81  # gravitational acceleration


# --- Input ---
def get_initial_conditions():
    def ask_float(prompt):
        val = input(prompt).strip()
        if val == "":
            logging.warning("Blank string passed as input: " + val)
            return ask_float("Lūdzu, ievadiet datus: ")
        try:
            return float(val)
        except ValueError:
            logging.warning("Invalid user input: " + val)
            return ask_float("Ievadi neizdevās pārveidot par skaitli. Lūdzu, mēģiniet vēlreiz: ")

    h0 = ask_float("Lūdzu, ievadiet sākotnējo augstumu h0 (m): ")
    v0 = ask_float("Lūdzu, ievadiet sākotnējo ātrumu v0 (m/s): ")

    return h0, v0


# --- Simulation ---
def simulate_fall(h0, v0, dt=0.01):
    t = 0
    data = []

    while True:
        h = h0 + v0 * t + 0.5 * g * t**2
        v = v0 + g * t

        data.append((t, h, v))

        if h < 0:
            break

        t += dt

    logging.info(f"Simulation complete. Steps: {len(data)}")
    return data


# --- Interactive probe ---
def interactive_probe(h0, v0):
    if not sim_data:
        logging.error("Simulation data not found!")
        print("Simulācijas datu ielāde nav izdevusies.")
        return

    t_max = sim_data[-1][0]

    print(f"\n Lūdzu, ievadiet laika daudzumu, kas pagājis kopš kustības sākuma vai nospiediet \"Enter\", lai izietu. (No 0s līdz {round(t_max, 2)}s): ")

    while True:
        val = input("t = ").strip()
        if val == "":
            logging.info("Exiting probe.")
            break

        try:
            t = float(val)
            if t_query < 0 or t_query > t_max:
                logging.warning("Out of range t requested:" + string(t))
                continue

            h = h0 + v0 * t + 0.5 * g * t**2
            v = v0 + g * t

            print(f"\nt = {round(t,2)} s")
            print(f"  Momentānais augstums = {round(h,2)} m")
            print(f"  Momentānais ātrums = {round(v,2)} m/s")
            print(f"  Paātrinājums = constant ({round(g,2)} m/s²)\n")

        except ValueError:
            print("Ievade nevar tikt pārveidota par skaitli.")


# --- Plot ---
def plot_height(sim_data):
    ts = [row[0] for row in sim_data]
    hs = [row[1] for row in sim_data]

    plt.figure()
    plt.plot(ts, hs)
    plt.xlabel("Laiks (s)")
    plt.ylabel("Augstums (m)")
    plt.title("Ķermeņa augstums h(t)")
    plt.grid(True)
    plt.show()


# --- Main ---
def main():
    h0, v0= get_initial_conditions()
    sim_data = simulate_fall(h0, v0)
    plot_height(sim_data)
    interactive_probe(h0, v0)

    logging.info("Program finished.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Critical error: {e}")

# Koda izveidošana un optimizēšana atvieglināta, lietojot ChatGPT 5.
