from datetime import date as Date, time as Time
from pawpal_system import Priority, Frequency, Task, Pet, Scheduler, Owner

TODAY    = Date(2026, 7, 7)
TOMORROW = Date(2026, 7, 8)

def main():
    s = Scheduler()
    claude = Owner("Claude", s, [], [], [])

    dot = Pet("Dot", "cute doggy", [])
    claude.add_pet(dot)
    spot = Pet("Spot", "silly bunny", [])
    claude.add_pet(spot)
    pip = Pet("Pip", "grumpy cat", [])
    claude.add_pet(pip)
    gremlin = Pet("Lord Biscuit Mc-Stinkypaws III", "chaotic feral ferret of unknown origin", [])
    claude.add_pet(gremlin)

    dot.add_task(title="walkies!", date=TODAY, time=Time(8, 0),  duration=60, priority=Priority.HIGH,      frequency=Frequency.DAILY)
    dot.add_task(title="fetch",    date=TODAY, time=Time(8, 0),  duration=20, priority=Priority.LOW,       frequency=Frequency.DAILY)
    spot.add_task(title="Bath Time",       date=TODAY, time=Time(10, 30), duration=45, priority=Priority.MEDIUM,    frequency=Frequency.WEEKLY)
    spot.add_task(title="Vet visit",       date=TODAY, time=Time(10, 30), duration=200, priority=Priority.VERY_HIGH, frequency=Frequency.ONE_TIME)
    spot.add_task(title="Hay Refill",      date=TODAY, time=Time(7, 0),  duration=10, priority=Priority.HIGH,      frequency=Frequency.DAILY)
    pip.add_task(title="brushing",         date=TODAY, time=Time(14, 0), duration=15, priority=Priority.MEDIUM,    frequency=Frequency.WEEKLY)
    pip.add_task(title="Vet visit",        date=TOMORROW, time=Time(9, 15), duration=200, priority=Priority.VERY_HIGH, frequency=Frequency.ONE_TIME)
    gremlin.add_task(title="ESCAPE ATTEMPT #47",                date=TOMORROW, time=Time(6, 0),  duration=1,    priority=Priority.VERY_HIGH, frequency=Frequency.DAILY)
    gremlin.add_task(title="steal dad's socks",                 date=TODAY, time=Time(8, 0),  duration=9999, priority=Priority.LOW,       frequency=Frequency.DAILY)
    gremlin.add_task(title="Nap (do not disturb or else)",      date=TODAY, time=Time(13, 0), duration=0,    priority=Priority.VERY_LOW,  frequency=Frequency.ONE_TIME)
    gremlin.add_task(title="??????????",                        date=TODAY, time=Time(20, 0), duration=30,   priority=Priority.MEDIUM,    frequency=Frequency.ONE_TIME)

    claude.find_task("fetch").mark_complete()
    claude.find_task("Hay Refill").mark_complete()
    claude.find_task("ESCAPE ATTEMPT #47").mark_complete()

    all_tasks = claude.get_all_tasks()

    print("Today's Schedule")
    print('~'*30)
    for task in all_tasks:
        print(task)
    print("\nSorted by Time (priority tiebreaker)")
    print('~'*30)
    for task in Scheduler.sort_by_time_with_priority(all_tasks):
        print(task)
    print("\nPending Tasks")
    print('~'*30)
    for task in Scheduler.filter_by_completed(all_tasks, completed=False):
        print(task)
    print("\nCompleted Tasks")
    print('~'*30)
    for task in Scheduler.filter_by_completed(all_tasks, completed=True):
        print(task)


    print("\n\nToday's Generated Schedule")
    print('~'*30)
    schedule, reasoning = s.generate_schedule(claude, TODAY)
    for item in schedule:
        print(item)
    print("\nScheduling Reasoning")
    print('~'*30)
    for reason in reasoning:
        print(reason)

    print("\n\nTomorrow's Generated Schedule")
    print('~'*30)
    schedule, reasoning = s.generate_schedule(claude, TOMORROW)
    for item in schedule:
        print(item)
    print("\nScheduling Reasoning")
    print('~'*30)
    for reason in reasoning:
        print(reason)

if __name__ == "__main__":
    main()


'''
Imports your classes from pawpal_system.py.
Creates an Owner and at least two Pets .
Adds at least three Tasks with different times to those pets.
Prints a "Today's Schedule" to the terminal.
'''