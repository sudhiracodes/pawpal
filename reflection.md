# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

 My initial design uses a simple object-oriented structure with four core classes: Owner, Pet, Task, Scheduler; to separate data from logic. 
 - The Owner class has the attributes name and a list of pets. It uses the methods add_pet() to link a new pet to the user, and get_all_tasks() to aggregate every task across all owned pets.

 - The Pet class represents an individual animal, with attributes like name, species, and a list of its specific Task objects. It has the method add_task() to assign a new chore directly to that pet.

- The Task class tracks a single chore's attributes (description, time, frequency) and an is_complete boolean flag. It uses the method mark_complete() to update the task's status to finished.

-The Scheduler Class holds attribute Owner and methods get_today_schedule(), sort_by_time() to order the aggregated tasks chronologically, and check_conflicts() to scan the schedule and flag any tasks occurring at the exact same time.

- What classes did you include, and what responsibilities did you assign to each?

The Owner class holds a list of Pet objects, and each Pet manages its own list of Task chores. I built a separate Scheduler class to act as the logic engine; instead of storing data, it takes the Owner object, aggregates all pet tasks, sorts them by time, and flags any scheduling conflicts.

**b. Design changes**

- Did your design change during implementation?
Yes
- If yes, describe at least one change and why you made it.

In my initial UML, I kept simpler tasks and a scheduler that only sorted and flagged conflicts. During implementation I expanded the Task class to include duration, priority, and an end_time helper, and I extended Scheduler.get_today_schedule to sort by time and priority and optionally respect an available‑minutes time budget. This shifts some responsibility into the domain classes while still keeping the main coordination inside Scheduler, and it makes it easier to evolve the scheduling rules later to handle more real‑world constraints without rewriting the whole design.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

The scheduler considers several primary constraints:

- **Chronological time** – Tasks are filtered by a specific date and sorted by their start time.
- **Priority** – An integer scale (1–5) is used as a secondary sort key so higher‑priority tasks at the same time are chosen first.
- **Time budget** – An optional `available_minutes` limit is compared against each task’s `duration_minutes`, and tasks are added greedily until the budget is exhausted.
- **Conflicts** – The scheduler performs lightweight conflict detection by checking for overlapping time windows (based on `time` and `end_time`), and surfaces warnings instead of crashing or auto‑rescheduling.
- **Recurrence** – For “Daily” and “Weekly” tasks, when a task is marked complete, a new instance is created for the next occurrence using `timedelta`, so recurring care continues automatically.
- **Filtering** – Tasks can be filtered by completion status or pet name in the scheduler, and the UI supports viewing all pets or a single pet’s schedule.

- How did you decide which constraints mattered most?

I decided to sort by time first because pet care follows a daily routine (e.g., morning walks before afternoon play). Priority is used as a tie‑breaker so that, when time slots collide, more important tasks are favored. The time budget is a practical constraint so the app doesn’t plan more than the owner can realistically do in a day. Conflict checks and recurrence are layered on top: conflicts are surfaced as warnings (so the user stays in control), and recurring tasks are regenerated so that daily and weekly care tasks don’t disappear after one completion.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The main tradeoff is that the scheduler uses a **greedy chronological time‑budget strategy** rather than an optimal packing algorithm (like knapsack). It processes tasks in sorted order (time, then priority) and includes each task as long as there is enough remaining time. It does not try to “rearrange” or skip an early, long task in order to squeeze in multiple shorter tasks later.

Another tradeoff is that **conflict handling is advisory**, not automatic. The system detects overlapping tasks and returns them as warnings, but it does not attempt to move or resolve them on its own.

- Why is that tradeoff reasonable for this scenario?

This is reasonable because pet care is inherently time‑sensitive. It’s usually not acceptable to skip or delay an 8:00 AM feeding just because that might yield a mathematically better time packing later in the day. Chronological realism and clarity are more important than theoretical optimality. Similarly, raising warnings instead of auto‑rescheduling keeps the owner in control of important commitments like vet visits or medication times, and keeps the logic simple and predictable for a busy user.


## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
