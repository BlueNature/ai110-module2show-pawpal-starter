# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Example actions:
- Enter owner/pet info
- Enter tasks including duration + priority
- Generate schedule that satisfies constraints


- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I first thought about the classes and their interactions with my group, and we came up with some potential class attributes and methods. Then, I iterated on the whole thing with Claude Code. First, I had it generate its own UML diagram from scratch, which did not work well as expected since it did not have knowledge of the scope of my project. (i.e. only wanting four different classes, whereas it came up with additional classes including ScheduledTask and Conflict) After that, I gave it the class interactions we came up with and had it critique them. The full iteration has been put into `class_outline_iteration.md` for my own ease of access. The first and last drafts before beginning implementation are also available below. All significant UML diagrams are in the diagrams directory.

**First Draft Classes:**
Owner:
- owner of pets
- attributes: name, has list of all pets, schedule
- methods: add(Pet) -> list[Pet], remove(Pet) -> list[Pet], add_task(Pet, title, duration, priority), get_tasks -> list[Task], generate_schedule -> Schedule

Pet:
- represents one individual pet
- attributes: name, species, has list of tasks
- methods: create_pet

Task:
- represents a single task
- attributes: title, duration, priority, time needed
- methods: create_task

Scheduler:
- schedule for a given day
- attributes: (not sure yet)
- methods: get_tasks -> list[Task], generate_schedule

**Revised Draft Classes:**
Owner:
attributes: name, pets: list[Pet], scheduler: Scheduler, schedule: list[(str, time, Task)], reasoning: list[str]
methods: add(Pet) -> Pet, remove(Pet) -> None, find_pet(name: str) -> Pet, get_tasks() -> list[Task], generate_schedule(), display_schedule(), display_reasoning()

Pet:
attributes: name, species, tasks: list[Task]
methods: add_task(title, duration, priority, frequency) -> Task, remove_task(Task) -> None, find_task(title: str) -> Task

Task:
attributes: title, duration, priority, frequency
methods: edit(title=None, duration=None, priority=None, frequency=None) -> Task

Scheduler:
attributes: (none — stateless)
methods: generate_schedule(owner: Owner) -> tuple[list[(str, time, Task)], list[str]]

Priority:
(enumeration)
values: VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW



**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

The design changed quite a bit from the original plans. For example, I had to figure out how the Owner class would access the reasoning from the Scheduler; Claude Code suggested representing it as a list of strings where each one represents a decision made rather than a whole string. Another decision was whether the Owner or the Scheduler would be in control of getting all the tasks from all the pets. This settled on the Owner, for which the Scheduler could call its method when generating the schedule. I also decided to create an Enum for the task priority.
A significant change was how to represent the tasks in the final schedule. I was stuck between having it be a simple list of tasks or a list of tuples containing the time and the task. (in other words, whether the day and time should be attributes of the task or appear separately) When working with Claude Code, it suggested that the time attributes should be separate from the Task definition because these attributes only get filled once the Scheduler generates a schedule, otherwise the Task may have these attributes blank sometimes and filled other times.
However, later in the project I realized that this might go against what the instructions want; rather than the Scheduler figuring out what times work best for the tasks, the user can be expected to put in the starting time and duration (as rigid values) and the Scheduler will arrange them all. This means the Task would have the time attribute and the schedule could be represented as just a list of tasks sorted by time. I also settled on adding a date attribute in order to fit the requirement of managing recurring tasks using `timedelta`.
Finally, there were a few small changes made in some of the accessor functions so that they could be used by app.py in the Streamlit UI instead of plain print statements. (The skeleton code originally contained only print statements but was added to later on)


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

I took a greedy approach when designing the scheduler. First, it only considers tasks that are not marked as completed, which seems reasonable. It values priority as the most important attribute, followed by time. It does not consider other things like what pet the task belongs to. I think priority is more important than time because a higher priority naturally implies the task itself is more important, which is a very pragmatic stance to take.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler strictly values priority over time to the point where it essentially places all higher-priority tasks before moving on to lower-priority ones. This can result in a long high-priority task taking up the space that could otherwise fit many lower-priority tasks. However, I think this is reasonable and that higher-priority tasks should be appropriately given higher priority. (it feels obvious when you write it out like this)
At the same time, I recognize that other strategies could be reasonable, such as aiming to maximize the number of tasks that get scheduled for a given day. A possible heuristic for this could be to schedule smaller durations first, or focus on boundaries to minimize empty time.
The scheduler also only generates schedules for one day at a time rather than the entire week. I did this because it worked best with my method of managing recurring tasks: there is only one on-deck instance of the task at all times, and the next instance is only created when the existing one is marked as completed.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI for a variety of cases throughout the process. I mostly used it to help me take on large portions of the work such as building tables to house enums and adding tasks (which require lots of parameters though their arguments are obvious). I also used it to confirm various part of the Streamlit UI.
I often tried to build parts of the logic or UI myself before asking the AI to revise my design so that I could have a hand in building the code myself and subsequently receive feedback on what does and doesn't work. In many cases, the AI will have greater knowledge of libraries and coding in general than me, which makes it important that I harness that knowledge to increase my own knowledge.
I used plan mode for the first time during this project with the intention of consolidating prompts into larger batches, and planning beforehand to make sure they would all be implemented properly. This tended to work well as I could see all the proposed changes, and I frequently iterated with Claude Code as well as looked through all the changes before manually approving them.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

When generating the test file, the AI added import statements for sys and os. I did not approve these changes without asking further because I am wary about including import statements for packages I do not know the purpose of. After asking, it decided that these imports were unnecessary and did not include them.
When determining duration-based time conflicts, I created my own logic before having the AI look it over. It correctly identified an edge case where my logic wouldn't work before replacing it with a different piece of logic for calculating overlap between intervals. I had never seen this code before despite Claude Code calling it the "standard" two-interval test, so I asked it about the code both to verify that it was correct and also internalize why it works so I could use it myself in later situations.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I made sure the tests covered all the functions as well as a full workflow through a typical user session. This means simple tests that covered individual function calls from `pawpal_system.py` as well as entire scenarios from creating an owner to creating pets and tasks, sorting them, and generating a schedule and confirming that it fit all the necessary criteria. I especially think the full workflow tests are important because they mimic how the user will interact with the app in practice rather than arbitrary scenarios that may or may not happen (see next section).

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

__Confidence level: 5/5 stars__
All of the test cases I had (total 43) passed. One case was previously included that verified a potential type error, but I confirmed that this case doesn't happen in practice when adding tasks through the UI. (The only way it can occur is when explicitly creating a task with arbitrary values, which cannot happen.) But while the tests seem to comprehensively cover all the backend functions and logic, I would still take some time to look deeper into the code myself if I had more time. For example, I would try creating more complex and conflicting tasks between pets to see how the scheduler prioritizes tasks if forced to decide. I would also stress-test deleting various objects to look for any potential key errors that arise.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the logic I used for the app. I chose this because it is the thing I spent the most time learning about, compared to Streamlit which I already had a bit of experience with from the previous project. Specifically, I am satisfied with the way my UML diagram worked out and the process of designing it.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had more time, I would inspect the code even deeper to make sure everything is not only readable but understandable. As for features, the biggest improvement would be to allow generating a weekly schedule and not just a daily one.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

This project gave me perspective on how valuable it is to design a program before implementing it. In contrast, in my DSA class, I would first draft the main functionality for each file and how to implement the functions, but here I had to look at the big picture. Admittedly, I am not a huge fan of the UML diagram structure as it didn't fit my preferences. I think I was naturally trying to code in terms of functionality (seeing what I need to do, and what I need to have in order to accomplish it) rather than class interactions (starting by breaking down the problem into encapsulated units that only interact with each other in certain ways). Still, I recognize the benefits of a class-based structure like what UML encourages, and I will most likely continue to consider it in future projects.
