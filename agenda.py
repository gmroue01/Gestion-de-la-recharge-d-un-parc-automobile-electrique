import random
from datetime import datetime, timedelta
TYPES_SLOT = ("available", "meeting", "do not disturb", "break")

START_OF_A_DAY = "8:00"
END_OF_A_DAY = "17:00"
SLOT_TIME_MIN = 15


def _schedule(start: str = START_OF_A_DAY, end: str = END_OF_A_DAY, step: int = SLOT_TIME_MIN) -> list[str]:
    """
    Generate the label of each slot of the schedule.

    """

    start_time = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")
    duration_min = ((end_time - start_time).total_seconds() / 3600)*60
    number_slot = int(duration_min / step)

    time_slot_labels = []

    for t in range(number_slot):
        time_slot = start_time + timedelta(minutes=t*step)
        time_slot_labels.append(f"{time_slot.hour}:{time_slot.minute:02d}")

    return time_slot_labels


def generate_agendas(seed: int):
    """"
    generate_agendas generates random agenda of lenght n for one employee.
    Each employee has one vehicule.
    Each employee has a single agenda.
    Params:

    """
    rng = random.Random(seed)
    hours = _schedule()
    n = len(hours)
    hours_index = list(range(n))

    agenda = ["available"]*n

    # w is the number of new type of slot that will be generated randomly

    type_slot_picked = []
    duration_slot_picked = []
    start_time_picked = []

    w = 5

    remain = set(hours_index)
    for i in range(w):
        type_slot_variable = random.choice(TYPES_SLOT)

        type_slot_picked.append(type_slot_variable)

        duration_slot_variable = random.randint(2, 8)

        duration_slot_picked.append(duration_slot_variable)

        starts = [h for h in sorted(remain) if all(
            h+k in remain for k in range(duration_slot_variable))]

        if not starts:
            continue

        start_time_variable = random.choice(starts)

        start_time_picked.append(start_time_variable)
        for h in range(start_time_variable, start_time_variable + duration_slot_variable):
            remain.remove(h)

    for start, duration, type_slot in zip(start_time_picked, duration_slot_picked, type_slot_picked):

        agenda[start:start + duration] = [type_slot] * duration

    return agenda


if __name__ == "__main__":
    print(generate_agendas(42))
