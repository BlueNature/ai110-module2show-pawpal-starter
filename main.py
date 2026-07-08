from pawpal_system import Priority, Frequency, Task, Pet, Scheduler, Owner

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

    dot.add_task(title="walkies!", duration=60, priority=Priority.HIGH, frequency=Frequency.DAILY)
    dot.add_task(title="fetch", duration=20, priority=Priority.LOW, frequency=Frequency.DAILY)
    spot.add_task(title="Bath Time", duration=45, priority=Priority.MEDIUM, frequency=Frequency.WEEKLY)
    spot.add_task(title="Vet visit", duration=200, priority=Priority.VERY_HIGH, frequency=Frequency.ONE_TIME)
    spot.add_task(title="Hay Refill", duration=10, priority=Priority.HIGH, frequency=Frequency.DAILY)
    pip.add_task(title="brushing", duration=15, priority=Priority.MEDIUM, frequency=Frequency.WEEKLY)
    pip.add_task(title="Vet visit", duration=200, priority=Priority.VERY_HIGH, frequency=Frequency.ONE_TIME)
    # gremlin.add_task(title="ESCAPE ATTEMPT #47", duration=1, priority=Priority.VERY_HIGH, frequency="hourly")
    # gremlin.add_task(title="steal dad's socks", duration=9999, priority=Priority.LOW, frequency="constantly")
    # gremlin.add_task(title="Nap (do not disturb or else)", duration=0, priority=Priority.VERY_LOW, frequency="never")
    # gremlin.add_task(title="??????????", duration=30, priority=Priority.MEDIUM, frequency="??????")

    print("Today's Schedule")
    print('~'*30)
    for task in claude.get_all_tasks():
        print(task)
    '''
    (schedule, reasoning) = s.generate_schedule(claude)
    for item in schedule:
        print(item)
    '''

if __name__ == "__main__":
    main()


'''
Imports your classes from pawpal_system.py.
Creates an Owner and at least two Pets .
Adds at least three Tasks with different times to those pets.
Prints a "Today's Schedule" to the terminal.
'''