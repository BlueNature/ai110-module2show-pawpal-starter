from pawpal_system import Priority, Task, Pet, Scheduler, Owner

def main():
    s = Scheduler()
    claude = Owner("Claude", s, [], [], [])

    dot = Pet("Dot", "cute doggy", [])
    claude.add(dot)
    spot = Pet("Spot", "silly bunny", [])
    claude.add(spot)
    pip = Pet("Pip", "grumpy cat", [])
    claude.add(pip)
    gremlin = Pet("Lord Biscuit Mc-Stinkypaws III", "chaotic feral ferret of unknown origin", [])
    claude.add(gremlin)

    dot.add_task("walkies!", 60, Priority.HIGH, "daily")
    dot.add_task("fetch", 20, Priority.LOW, "daily")
    spot.add_task("Bath Time", 45, Priority.MEDIUM, "weekly")
    spot.add_task("Vet visit", 200, Priority.VERY_HIGH, "one-time")
    spot.add_task("Hay Refill", 10, Priority.HIGH, "daily")
    pip.add_task("brushing", 15, Priority.MEDIUM, "weekly")
    pip.add_task("Vet visit", 200, Priority.VERY_HIGH, "one-time")
    gremlin.add_task("ESCAPE ATTEMPT #47", 1, Priority.VERY_HIGH, "hourly")
    gremlin.add_task("steal dad's socks", 9999, Priority.LOW, "constantly")
    gremlin.add_task("Nap (do not disturb or else)", 0, Priority.VERY_LOW, "never")
    gremlin.add_task("??????????", 30, Priority.MEDIUM, "??????")

    print("Today's Schedule")
    print('~'*30)

if __name__ == "__main__":
    main()


'''
Imports your classes from pawpal_system.py.
Creates an Owner and at least two Pets .
Adds at least three Tasks with different times to those pets.
Prints a "Today's Schedule" to the terminal.
'''