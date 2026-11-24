# AI Usage

This file records the technical help I got from an AI coding assistant while building the Power Grid Simulator. For each technical request it gives my prompt, a summary of the response, and what I did with it. It also records the changes I made to the AI's output and why.

The prompts are copied from my chat messages. The responses are summaries, because the full replies were long. The full text is in the chat history.

---

## 1. Tool and model

- **Tool:** Cursor, the AI code editor, using its **agent mode**. In agent mode the assistant can read and edit files in the project, run commands, and view the graphs the program produces.
- **How I accessed it:** through the Cursor chat panel, in the project folder `Power System Simulator`.
- **Model:** the assistant identifies itself as "Auto" inside Cursor, and it could not see which underlying model it was running. `[Model name from Cursor's model selector: fill in]`
- **Period:** 23 to 24 November 2026.

---

## 2. Technical requests and responses

### Request 1: Physics, components and design

**My prompt:**
> Power_Grid_Simulator_Task.docx Hey I have to simulate the power station grid using python and provide graphical representations of the frequency of the components can you detaily explain the physical process the components the interconnection to implement the breifing that would help me to build it completly. I am PLANNING TO IMPLEnting the components as clases and the interconnection and communication using main_process.py file

**Response (summary):** The assistant read the brief and explained the physics as four states, set by two switches: the generator (ON or OFF) and the breaker (CLOSED or OPEN). Each state has a rate of frequency change. It ran a throwaway simulation outside the project to compare control strategies. It suggested opening the breaker at 49.65 Hz and reclosing at about 50.30 Hz, and it proposed one class per component, a fixed order of steps each second, and a set of tests.

**What I did:** I used the four-state physics and the 49.65 Hz opening threshold as the basis of the design. I kept one class per component.

### Request 2: A build plan

**My prompt:**
> lets build it from basics and lets build a simple mental model baisc components flow control logic lets have that idea build it up and build over it (plan it only dont build)

**Response (summary):** A nine-stage plan. Each stage was small, produced something I could see, and had a clear test for when it was finished.

**What I did:** I followed the stages in order.

### Request 3: When the generator should trip

**My prompt:**
> at what stage then the generator off should it be offed at random time period

**Response (summary):** The normal control logic should not turn the generator off. A trip should be a scripted fault at a chosen time, added once the basic controller works. A random time is better as a seeded option, so a test can be repeated. A trip while the breaker is closed is the hardest case.

**What I did:** I used scripted trips first, and added random trips later with a seed option.

### Request 4: A wave-curve function

**My prompt:**
> can you define a function that generates the wave curve of the sensor frequency value in @Simulator.py

**Response (summary):** The assistant wrote a function that runs the whole simulation for 120 seconds and returns the history, and a plot function.

**What I did:** I rejected the simulation function and asked for an undo.

### Request 5: Plot function only

**My prompt:**
> undo the chnages I just need a function to generate the wave graph thats it

**Response (summary):** The assistant rebuilt `Simulator.py` from its memory of my original loop, and kept only one plot function.

**What I did:** I kept the plot function. The assistant rebuilt the file from memory rather than restoring a saved copy, so I checked the result myself.

### Request 6: Binary state graphs

**My prompt:**
> can you add a helper method to convert the generator and breaker state into binary values and represent as a step fun graph

**Response (summary):** Three functions. One converts the generator state to 1 for ON and 0 for OFF. One converts the breaker state to 1 for CLOSED and 0 for OPEN. One draws both as step plots. The breaker's stored value is `is_open`, so the conversion inverts it.

**What I did:** I kept the functions, and kept the inverted conversion with a comment explaining it.

### Request 7: Physical process and gaps

**My prompt:**
> lets discuss in detail the physical process the gaps and yes I have not completed the mental model completly can you help me to complete it out

**Response (summary):** A four-state model with the transitions between the states, and the sawtooth explained with numbers: about 14 seconds closed and 6 seconds open, which gives 70.6% uptime. It listed eight gaps in the model and five questions to test it.

**What I did:** I used the gaps as a checklist for the next steps, and worked through the questions to check my understanding.

### Request 8: Next steps

**My prompt:**
> see now we will go step by step what are the next steps of simulations that are pending show we will do it out

**Response (summary):** A table of nine remaining steps, each with a way to tell it was complete.

**What I did:** I worked through the steps in order, starting with the control rules.

### Request 9: Restarting the generator from the controller

**My prompt:**
> how to make the controller itself to restart the generator

followed by:

> can you add it outy

**Response (summary):** The scenario should only trip the generator. The controller should count the seconds the generator is OFF and turn it back on after three seconds. The breaker should only reclose while the generator is ON. The assistant gave the code.

**What I did:** I added the code myself, with the trip times kept in a list named `generator_trip_times`. I then tested the change in a temporary copy and checked the trace.

### Request 10: Is the "generator ON" reclose check important?

**My prompt:**
> if frequency_sensor.get_frequency() >= 50.35 and generator.is_on: is this condition higly imp

**Response (summary):** It is a safety interlock, because the load should never be reconnected to a stopped generator. In the scripted trips it had no effect, because the breaker closes at 50.35 Hz before a trip can happen. It matters once sensor faults are added. The assistant also corrected an earlier statement it had made, that the check was needed in that run.

**What I did:** I kept the check and its explanation.

### Request 11: Trips that could be lost

**My prompt:**
> Trips that land on an already-OFF generator are silently ignored. Two trips in the same outage, or duplicate trip times, would drop events without any message. Log these or prevent them.

followed by:

> can U resolve that out

**Response (summary):** Three cases where a trip could disappear: a trip during an outage, duplicate times, and a trip in the last second. The assistant suggested unique times at least four seconds apart, no trips in the last second, a message when the requested number does not fit, and a log line for each trip.

**What I did:** I used this approach and kept the spacing constant named `MIN_TRIP_GAP`. The assistant tested 300 random runs of 60 seconds with five trips each, and every trip fired.

### Request 12: Docker

**My prompt:**
> now I have added end to end deployment using dockering the project and note docker run -it --rm -v "$PWD":/app sim-test as the cmd to run and replace pwd with the directory where oputput must be placed (need to add this in redme.md

**Response (summary):** The assistant tested the command. The `-v` mount replaces `/app`, so the output lands in the mounted folder, and that folder must contain the code. Running from an empty folder fails.

**What I did:** I kept the command you specified and documented this behaviour in the README. I did not change the design to allow a separate output folder.

---

## 3. Changes I made to the AI's output, and why

| Output from the assistant | What I changed | Why |
|---|---|---|
| A 120-second simulation function (Request 4) | Rejected, then removed | I only needed a plotting function. |
| The rebuilt `Simulator.py` after the undo (Request 5) | Checked it | The assistant rebuilt the file from memory, so I could not rely on it without checking. |
| A reclose threshold of 50.30 Hz (Request 1) | Used 50.35 Hz | The reclose threshold has to stay below the 50.38 Hz ceiling, so the peak stays under 50.50 Hz. 50.35 Hz meets that, and it keeps the breaker open a little longer. |
| Restart and trip logic in the scenario (Request 9) | Moved the restart into the controller | Only the controller should restart the generator. The scenario should only trip it. |
| Output that goes to the mounted folder (Request 12) | Kept, and documented | You asked for this command, and the README explains the constraint. |
| Rounding of the frequency | Not applied yet | Seven steps of -0.05 Hz from 50 gives `49.65000000000002`, which is not `<= 49.65`, so the breaker opened one second late at 49.60 Hz. The README describes this. |
| The first README, which included untested platform notes | Edited in later versions | The README should only describe the project as it is. |

---

## 4. Checks

- **Temporary copies.** Most tests ran in temporary copies of the project, with the real-time wait removed, so the project's own files and graphs were not changed during testing.
- **Scenario traces.** The assistant read a trace of each change and compared it with the graphs.
- **Stress test.** 300 random runs of 60 seconds with five trips.
- **Docker.** The container was run from the project folder, and from an empty folder to confirm the failure.
- **Link check.** Every internal link in the README resolves.
