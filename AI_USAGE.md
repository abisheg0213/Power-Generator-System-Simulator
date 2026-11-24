# AI Usage

This file records how I used an AI coding assistant while building the Power Grid Simulator. It covers the tool and how I accessed it, the prompts I gave, what the assistant returned, and what I changed and why.

The prompts below are copied from my chat messages. The responses are summaries of the key points, because the full replies were long. The full text is in the chat history.

---

## 1. Tool and model

- **Tool:** Cursor, the AI code editor, using its **agent mode**. In agent mode the assistant can read and edit files in the project, run commands in the terminal, and view the graphs the program produces.
- **How I accessed it:** through the Cursor chat panel, in the project folder `Power System Simulator`.
- **Model:** the assistant identifies itself as "Auto" inside Cursor, and it could not see which underlying model it was running. `[Model name from Cursor's model selector: fill in]`
- **Period:** 23 to 24 November 2026.

---

## 2. How I worked with it

I wrote the code and made the decisions. I used the assistant to explain the physics, to review my code and graphs, and to suggest fixes. The assistant also ran checks, and I reviewed the results before keeping a change. Most checks ran in a temporary copy of the project, so my own files and graphs were only changed when I decided to.

---

## 3. Prompts, responses and what I did with them

### Stage 1: Understanding the brief and the design

**My prompt:**
> Power_Grid_Simulator_Task.docx Hey I have to simulate the power station grid using python and provide graphical representations of the frequency of the components can you detaily explain the physical process the components the interconnection to implement the breifing that would help me to build it completly. I am PLANNING TO IMPLEnting the components as clases and the interconnection and communication using main_process.py file

**Response (summary):** The assistant read the brief and worked out the physics as four states (generator ON or OFF, breaker CLOSED or OPEN) with the rate of frequency change for each. It ran a throwaway simulation outside the project to compare control strategies, and suggested opening the breaker at 49.65 Hz and reclosing at about 50.30 Hz. It also proposed a design with one class per component, a fixed order of steps each second, and a set of tests.

**What I did:** I used the four-state physics and the opening threshold of 49.65 Hz as the basis of the design. I kept the separate classes for each component.

### Stage 2: A build plan

**My prompt:**
> lets build it from basics and lets build a simple mental model baisc components flow control logic lets have that idea build it up and build over it (plan it only dont build)

**Response (summary):** A nine-stage plan. Each stage was small, produced something I could see, and had a clear test for when it was done.

**What I did:** I followed the stages in order.

### Stage 3: Reviewing my first code

**My prompt:**
> hey I have developed a small mental model of it am I going in the right direction? how the physical process spans out over all can U explain the physical process mental model in simple terms (do not code)

**Response (summary):** The assistant said my structure was right, but pointed out that my sensor changed the frequency itself, which a sensor should not do. It also found missing `self` arguments, file names that did not match the imports, and a generator that started OFF, which is the worst starting case.

**What I did:** I fixed the file names and the missing `self` arguments myself. I kept the sensor for now, and I planned to separate the true frequency from it later.

### Stage 4: When the generator should trip

**My prompt:**
> at what stage then the generator off should it be offed at random time period

**Response (summary):** The generator should not be turned off by the normal control logic. It should be a scripted fault at a chosen time, added after the basic controller works. A random time is better as a seeded option, so a test can be repeated. The assistant also said that a trip while the breaker is closed is the hardest case.

**What I did:** I used scripted trips first, and added random trips later with a seed option.

### Stage 5: A wave-curve function (rejected)

**My prompt:**
> can you define a function that generates the wave curve of the sensor frequency value in @Simulator.py

**Response (summary):** The assistant wrote a function that runs the whole simulation for 120 seconds and returns the history. It also wrote a plot function.

**What I did:** I rejected this. My next message asked for an undo, and that is covered in Stage 6.

### Stage 6: Undo, and a plot function only

**My prompt:**
> undo the chnages I just need a function to generate the wave graph thats it

**Response (summary):** The assistant rebuilt `Simulator.py` from its memory of my original loop, and added one plot function.

**What I did:** I kept the plot function and removed the rest. The assistant rebuilt the file from memory rather than restoring a saved copy, so I checked it myself.

### Stage 7: Binary state graphs

**My prompt:**
> can you add a helper method to convert the generator and breaker state into binary values and represent as a step fun graph

**Response (summary):** Three functions: one to convert the generator state to 1 for ON and 0 for OFF, one to convert the breaker state to 1 for CLOSED and 0 for OPEN, and one to draw both as step plots. The assistant ran it and noted that the breaker graph showed the breaker never closing again.

**What I did:** I kept the functions. The breaker's stored value is `is_open`, so the conversion inverts it. I kept that conversion and labelled it in a comment.

### Stage 8: Checking whether the fix worked

**My prompt:**
> is it now fine

**Response (summary):** No. The code had a syntax error, `!circuit_breaker.is_open`, which Python does not accept. With that fixed, the frequency froze at about 49.57 Hz, because the +0.12 Hz rise only ran inside the under-frequency branch. The assistant explained that each second should apply exactly one rate, chosen from the generator and breaker states.

**What I did:** I changed the rate logic so that each second applies one rate.

### Stage 9: Completing the mental model

**My prompt:**
> lets discuss in detail the physical process the gaps and yes I have not completed the mental model completly can you help me to complete it out

**Response (summary):** A four-state model with transitions between the states, the sawtooth explained with numbers (about 14 seconds closed and 6 seconds open, which gives 70.6% uptime), eight gaps in my understanding, and five questions to test it.

**What I did:** I used the gaps as a checklist. I answered the questions myself to check my understanding before moving on.

### Stage 10: Next steps

**My prompt:**
> see now we will go step by step what are the next steps of simulations that are pending show we will do it out

**Response (summary):** A table of nine remaining steps, each with a way to tell it was finished.

**What I did:** I worked through them in order, starting with the control rules.

### Stage 11: Floating-point rounding

**My prompt:**
> now see the modeling

**Response (summary):** Seven steps of -0.05 Hz from 50 gives `49.65000000000002`, which is not `<= 49.65`. So the breaker opened one second late, at 49.60 Hz. The assistant recommended rounding the frequency after each update.

**What I did:** I noted this as a known issue. I did not apply the rounding fix in this project, and the README describes the issue.

### Stage 12: Reading the simulation output

**My prompt:**
> now see the simulation

**Response (summary):** The assistant read my trace and found that the restart was being done by the scenario list, not by the controller. It also said that a random-looking trip list made the scenario hard to trust.

**What I did:** I moved the restart into the controller in the next stage.

### Stage 13: Controller restarts the generator

**My prompt:**
> how to make the controller itself to restart the generator

followed by:

> can you add it outy

**Response (summary):** The scenario should only trip the generator. The controller should count the seconds the generator is OFF and turn it back on after three seconds. The breaker should only reclose while the generator is ON. The assistant gave the code for this.

**What I did:** I added the code myself, and I renamed the scenario list to `generator_trip_times`. I then ran the change in a temporary copy and checked the trace.

### Stage 14: Is the "generator ON" check important?

**My prompt:**
> if frequency_sensor.get_frequency() >= 50.35 and generator.is_on: is this condition higly imp

**Response (summary):** It is a safety rule, because the load should never be reconnected to a stopped generator. The assistant said it had no effect on the scripted run, and the reason is that the breaker closes at 50.35 Hz before a trip can happen. It said the check matters once sensor faults are added. The assistant also corrected an earlier statement it had made, that the check was needed in that run.

**What I did:** I kept the check, and I kept the explanation in the README.

### Stage 15: Reviewing the results

**My prompt:**
> now see the results

**Response (summary):** A timeline of the run, with no limit violations and a closest approach of 49.55 Hz. It listed the remaining gaps: unseeded random trips, a rounding problem, the sensor holding the true frequency, and a short run.

**What I did:** I used the list as my next steps.

### Stage 16: Reviewing against the brief

**My prompt:**
> (off the track) not to be added in agent.md Review my simulation accordinhg to the assesment describtion given and if you were the one who examines this how much you arte it out and will you select for next round

**Response (summary):** An estimated score of about 55 out of 100, then about 58 after later fixes. The assistant said it would not be selected yet, because the README, the `AI_USAGE.md` and the repository were missing, and it listed the fixes in order.

**What I did:** I used the score as a rough guide. The brief has no published marking scheme, so the number is an estimate, not an official result.

### Stage 17: Trips that could be lost

**My prompt:**
> Trips that land on an already-OFF generator are silently ignored. Two trips in the same outage, or duplicate trip times, would drop events without any message. Log these or prevent them.

followed by:

> can U resolve that out

**Response (summary):** Three cases where a trip could disappear: a trip during an outage, duplicate times, and a trip in the last second. The assistant suggested unique times at least four seconds apart, no trips in the last second, a message if the requested number does not fit, and a log line for each trip.

**What I did:** I used the scheduling approach and the messages, and kept the spacing constant named `MIN_TRIP_GAP`. The assistant then tested 300 random runs of 60 seconds with five trips each, and every trip fired.

### Stage 18: Docker

**My prompt:**
> now I have added end to end deployment using dockering the project and note docker run -it --rm -v "$PWD":/app sim-test as the cmd to run and replace pwd with the directory where oputput must be placed (need to add this in redme.md

**Response (summary):** I did not have a README at that point, so I created one. The assistant tested the command and found that the mount replaces `/app`. The output therefore lands in the mounted folder, and the folder must contain the code. Running from an empty folder fails.

**What I did:** I kept the command you specified and documented this behaviour in the README. I did not change the design to allow a separate output folder.

### Stage 19: A detailed README

**My prompt:**
> hey make a detailed readme.md file where the project structure the components developed the way in whcih it is developed the physical process it depics how it is implemented the normal steps to run the script tthe outputs delivered the entire detailing of the project with addon of docker based containerisation as a add on feature to run it up in my envi

**Response (summary):** A long README covering the project, the physics, the components, the control logic, the scenario, the outputs, the local steps and the Docker add-on. The assistant also ran a seeded example, so the README could show a real run.

**What I did:** I used the README as the project documentation. Later I found that it described features that do not exist, which led to the next stage.

### Stage 20: Removing unimplemented content

**My prompt:**
> remove the unwanted content from @README.md which are not implemented in this project

**Response (summary):** The assistant removed the controller comparison, the limitations section with suggested fixes, the Windows and Linux notes I had not tested, and references to a `.dockerignore` file that does not exist. It replaced the limitations section with plain notes on how the program behaves, and it checked all the internal links.

**What I did:** I kept the change. Writing the first README had included content I had not verified, and I wanted the file to describe only what is in the project.

### Stage 21: A short AI usage note

**My prompt:**
> Hey I want a short and crisp AI_USAGE.md highlighting that I used cursor in agent mode which was helpful in developing the graphical plots that were displayed, helping to understand the physical process in a better manner fix the minor logic and syntatic bugs and made the development process much faster and efficient make it in 1st person narative (Like I am telling these things out)

**Response (summary):** A short first-person file covering the graphs, understanding the physics, fixing bugs, speed, and checking the output.

**What I did:** I used it as a starting point. Your next request asked for the full version, which is this file.

---

## 4. Changes I made to the AI's output, and why

| Output from the assistant | What I changed | Why |
|---|---|---|
| A 120-second wave function (Stage 5) | Rejected, then removed | I only needed a plotting function, and the extra code was not what I asked for. |
| The rebuilt `Simulator.py` after the undo (Stage 6) | Checked it against my own version | The assistant rebuilt it from memory, so I could not rely on it without a check. |
| A reclose threshold of 50.30 Hz (Stage 1) | Used 50.35 Hz | The reclose threshold has to stay below the 50.38 Hz ceiling so the peak remains under 50.50 Hz. 50.35 Hz meets that, and it means the breaker stays open a little longer. |
| Restart and trip logic in the scenario (Stage 12) | Moved the restart into the controller | Only the controller should restart the generator. The scenario should only trip it. |
| Random trip times with no limits (Stage 17) | Added the spacing rule, unique times, and log messages | Without them, trips could be lost without any message. |
| Output that goes to the mounted folder (Stage 18) | Kept, and documented | You asked for this command, and the README now explains the constraint. |
| A README that included untested platform notes and suggested features (Stage 19) | Removed them (Stage 20) | The README should only describe the project as it is. |
| The rounding fix (Stage 11) | Not applied yet | It is a known issue, and the README describes it. |
| An estimated score (Stage 16) | Used as a guide only | The brief does not publish a scoring system. |

---

## 5. Checks

- **Temporary copies.** Most tests ran in temporary copies of the project, with the real-time wait removed.
- **Scenario traces.** The assistant read the trace for each change, and compared it with the graphs. I checked the graphs myself.
- **Stress test.** 300 random runs of 60 seconds with five trips.
- **Docker.** I ran the container from the project folder, and from an empty folder to confirm the failure.
- **Link check.** I checked that every internal link in the README resolves.

---

## 6. Where the assistant was wrong, or needed correcting

1. **The undo was a rewrite from memory** (Stage 6). I checked the file afterwards.
2. **An overstated claim about the reclose check** (Stage 14). It was corrected after I tested it.
3. **My first Docker test was inconclusive.** Docker Desktop did not share `/tmp`, so the mounted folder looked empty. I repeated the test in a folder under my home directory.
4. **The first README included untested and planned content** (Stage 19). I removed it in Stage 20.
5. **Some numbers in the summaries were read from the graphs**, so they are approximate, and the README labels them that way.
6. **The score was an estimate** (Stage 16), not an official result.
