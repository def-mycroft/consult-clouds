# 05 Devplan - Current

#process-notes
capable-push
34aa005b-cc44-4778-99c1-c915875bd517
2025-06-10T16:57:30.568761-06:00


***

note: this is currently a template. 

\# TODO - this needs to be updated to a generalized template or at least a description of waht is needed here. the below is for another project and is retained as an example. 

---

### PHASE 1: Scaffold Execution Loop + Baseline Functionality

#### Objective

Implement a functional, minimal simulation that can:

- Schedule and execute events
    
- Track agent arrival, lift boarding, and lift return
    
- Print or store key metrics: agent wait time, number of riders, etc.
    

#### Strategy

1. **Start with class-by-class prompting**, keeping the full module in Codex's context window.
    
    - Copy-paste the current module
        
    - Then prompt with:  
        “Implement the `Simulation` class. It should manage a priority queue of events and execute them in time order.”
        
    - Follow up with:  
        “Now implement the `Lift` class. It should store a FIFO queue of agents, track state (‘idle’/‘moving’), and expose methods to load riders.”
        
2. **For each `Event` subclass**, provide the context and prompt tightly:
    
    - “Given the class `ArrivalEvent`, implement the `execute(sim)` method. It should add the agent to the lift’s queue and schedule a `BoardingEvent` if the lift is idle.”
        
3. **Once the structure runs**, create a function like `generate_agents(n, distribution)` and ask Codex to write it:
    
    - Give the format (e.g. list of agents with random arrival times)
        
    - Pass agents into the simulation and let it run until a cutoff time
        
4. **Log basic results**:
    
    - Total agents
        
    - Average wait time
        
    - Lift utilization
        
    - Number of completed rides
        

#### Codex Prompting Tip

Keep your prompts **imperative and explicit**, e.g.

> “Implement the `run()` method for the `Simulation` class to pop events from the heap and execute them until the event queue is empty or the clock exceeds the sim duration.”

Avoid:

> “What should go in the run method?” ← this leads to vague or general outputs.

---

### PHASE 2: Expand Behavior and State Tracking

#### Objective

Introduce skiing down and looping back into queue, agent histories, and more diverse metrics.

#### Steps

1. Add `ski_time` parameter to agent traits, and schedule a `ReturnToQueueEvent` or just reschedule another `ArrivalEvent` with `arrival_time = current_time + ski_time`.
    
2. Track per-agent:
    
    - Time entered queue
        
    - Time boarded lift
        
    - Time completed ride
        
    - Number of rides completed
        
3. Track lift metrics:
    
    - Total cycles
        
    - Idle time vs moving time
        
    - Utilization rate (Codex can help you compute this post-run)
        
4. Ask Codex to implement these by prompting:
    

> “Track `agent.wait_start` and compute per-agent wait time when boarding.”  
> “Add a field `lift.cycles_completed`, increment in `ReturnEvent.execute()`.”

---

### PHASE 3: Visualization and Analysis

#### Objective

Produce basic visual output (e.g. matplotlib plots) and log files for agent-level or lift-level time series.

#### Tactics

1. Prompt Codex to build visualizations:
    
    > “Using matplotlib, plot queue length over time from a list of (time, queue_size) tuples.”
    
2. Ask it to collect data during the run (e.g. queue snapshots every event):
    
    > “Log the queue length at every event execution.”
    
3. Extend:
    
    - Heatmap of queue times
        
    - Histogram of per-agent wait time
        
    - Time series: lift moving vs idle
        

---

### PHASE 4: Refactor + Persist

#### Objective

Refactor the kernel into a package, persist results, and build interfaces for experiment control.

#### Next Steps

1. Ask Codex to split simulation components into `core/`, `events/`, `agents/`, etc.
    
    > “Refactor the module into a package with submodules: `core.py`, `events.py`, `agents.py`, `lift.py`.”
    
2. Add JSON or SQLite logging:
    
    > “After the simulation run, write agent data to a SQLite table with schema (agent_id, rides, avg_wait_time, total_time).”
    
3. Allow experiment configuration via CLI or YAML:
    
    > “Write a CLI that accepts sim params like lift capacity, cycle time, n_agents, and logs results.”
    

---

### PHASE 5: Variant Scenarios and Agent Logic

#### Objective

Add parameterizable experiments, scenario variants, and agent-specific heuristics.

1. Introduce agent traits:
    
    - Patience threshold (leave if wait too long)
        
    - Preferred ski duration (limit total runs)
        
    - Random decision-making
        
2. Inject scenario config into the event loop:
    
    > “Add a flag to simulate a ‘Free Lift Day’ that doubles arrival rate.”
    
3. Codex can help with:
    
    - Creating variants from templates
        
    - Writing test scaffolds
        
    - Configuring batch runs
        

---

### General Codex Usage Principles

- **Use short, imperative prompts** grounded in code context.
    
- **Don’t ask abstractly**—always frame with “implement,” “add,” or “track.”
    
- **Copy-paste key class definitions** as context to avoid hallucination.
    
- **After each class**, test immediately and fix bugs before expanding.
    
- **Be explicit about outputs** (e.g. “return a list of events with timestamps and queue sizes”).
    
- **Name things consistently** across sessions.
    

---

Let me know when you’re ready to prompt Codex and want help crafting the first focused implementation prompt (e.g. `Simulation.run()` or `Lift.load()`), or when you're ready to design the sim entry point and test harness.

