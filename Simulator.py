from Generator import PowerGenerator
from FrequencySensor import FrequencySensor
from Breaker import CircuitBreaker
import time
import matplotlib.pyplot as plt
import random

def plot_frequency_wave(frequency_history):
    plt.plot(range(len(frequency_history)), frequency_history, label="FS101 frequency")
    plt.axhline(50.5, color="red", linestyle="--", label="Upper limit 50.50 Hz")
    plt.axhline(49.5, color="red", linestyle="--", label="Lower limit 49.50 Hz")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.legend()
    plt.grid(True)
    plt.savefig("frequency_wave.png")
    plt.close()

def generator_to_binary(generator_history):
    # generator.is_on -> 1 = ON, 0 = OFF
    return [1 if is_on else 0 for is_on in generator_history]

def breaker_to_binary(breaker_history):
    # breaker.is_open -> 1 = CLOSED, 0 = OPEN (inverted, because we store is_open)
    return [0 if is_open else 1 for is_open in breaker_history]

def plot_state_steps(generator_history, breaker_history):
    generator_binary = generator_to_binary(generator_history)
    breaker_binary = breaker_to_binary(breaker_history)
    time_axis = range(len(generator_binary))

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    ax1.step(time_axis, generator_binary, where="post")
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(["OFF", "ON"])
    ax1.set_ylabel("G101")
    ax1.grid(True)

    ax2.step(time_axis, breaker_binary, where="post")
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["OPEN", "CLOSED"])
    ax2.set_ylabel("CB101")
    ax2.set_xlabel("Time (s)")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("state_steps.png")
    plt.close()

generator = PowerGenerator()
frequency_sensor = FrequencySensor()
circuit_breaker = CircuitBreaker()

generator.on()
circuit_breaker.close()
count = 0
frequency_history = []
generator_state =[]
breaker_state =[]

#initial state
frequency_history.append(frequency_sensor.get_frequency())
generator_state.append(generator.is_on)
breaker_state.append(circuit_breaker.is_open)


RESTART_DELAY = 3                 # controller: seconds before it restarts G101
MIN_TRIP_GAP = RESTART_DELAY + 1  # scenario: min seconds between trips, so each trip hits a running G101
generator_off_timer = 0

simulation_period = int(input("Enter the simulation period in seconds: "))
if simulation_period <= 0:
    print("Simulation period must be greater than 0")
    exit()

generator_trip_times = [] 
no_of_trips = int(input("Enter the number of trips: "))
# scenario: pick unique trip times, at least MIN_TRIP_GAP seconds apart, and
# never in the last second (a trip there would not show up in the graphs)
attempts = 0
while len(generator_trip_times) < no_of_trips and simulation_period > 1 and attempts < 1000:
    trip_time = random.randint(1, simulation_period - 1)
    if all(abs(trip_time - other) >= MIN_TRIP_GAP for other in generator_trip_times):
        generator_trip_times.append(trip_time)
    attempts += 1
generator_trip_times.sort()

if len(generator_trip_times) < no_of_trips:
    print(f"Only {len(generator_trip_times)} of {no_of_trips} trips fit in {simulation_period}s "
          f"(trips must be at least {MIN_TRIP_GAP}s apart)")
print("Trip times:", generator_trip_times)

while True:
    if generator.is_on and circuit_breaker.is_open == False:
        frequency_sensor.generator_providing_load()
    if generator.is_on and circuit_breaker.is_open == True:
        frequency_sensor.generator_not_providing_load_running()
    if generator.is_on == False and circuit_breaker.is_open == False:
        frequency_sensor.generator_off_and_load_running()
    frequency_history.append(frequency_sensor.get_frequency())
    generator_state.append(generator.is_on)
    breaker_state.append(circuit_breaker.is_open)
    if frequency_sensor.get_frequency() <= 49.65:
        circuit_breaker.open()
    if frequency_sensor.get_frequency() >= 50.35 and generator.is_on:
        circuit_breaker.close()
    # controller: restart the generator after RESTART_DELAY seconds off
    if generator.is_on == False:
        generator_off_timer += 1
        if generator_off_timer >= RESTART_DELAY:
            generator.on()
            generator_off_timer = 0
    else:
        generator_off_timer = 0
    time.sleep(1)
    count += 1
    # scenario: trip the generator at the scripted times
    if count in generator_trip_times:
        if generator.is_on:
            generator.off()
            print(f"t={count}s: G101 tripped")
        else:
            print(f"t={count}s: trip ignored, G101 already OFF")
    if count == simulation_period:
        break
print(frequency_history)
plot_frequency_wave(frequency_history)
plot_state_steps(generator_state, breaker_state)

