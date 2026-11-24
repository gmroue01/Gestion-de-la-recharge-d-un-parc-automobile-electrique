import random
from datetime import datetime, timedelta
import csv
from display import display_agendas
from instances import save_instance_json
from pathlib import Path
TYPES_SLOT = ("available", "meeting", "do not disturb")

START_OF_A_DAY = "8:00"
END_OF_A_DAY = "17:00"
SLOT_TIME_MIN = 15
BREAK_SLOTS = range(16, 20)

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


def generate_agenda(seed: int):
    """"
    generate_agendas generates random agenda of lenght n for one employee.
    Each employee has one vehicule.
    Each employee has a single agenda.
    Params:

    """
    rng = random.Random(seed)
    hours = _schedule()
    n = len(hours)


    agenda = ["available"]*n
    
    # w is the number of new type of slot that will be generated randomly



    #Pause à midi : 12h00 à 13h00

    for i in BREAK_SLOTS:
        agenda[i] = "break"

    w = 5

    remain = set(range(n)) - set(BREAK_SLOTS)
    for i in range(w):
        type_slot_variable = random.choice(TYPES_SLOT)



        duration_slot_variable = random.randint(2, 8)



        starts = [h for h in sorted(remain) if all(
            h+k in remain for k in range(duration_slot_variable))]

        if not starts:
            continue

        start_time_variable = random.choice(starts)

   
        for h in range(start_time_variable, start_time_variable + duration_slot_variable):
            remain.remove(h)
            agenda[h] = type_slot_variable

    return agenda


def generate_charge_duration(seed : int):
    return random.randint(4,16)


def generate_all_agendas(seed : int, n_employee : int):

    return [generate_agenda(seed*1000  + e) for e in range(n_employee)]


def save_agendas_csv(agendas, path="agendas.csv"):
    labels = _schedule()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["employee", *labels])
        for i, agenda in enumerate(agendas):
            writer.writerow([i, *agenda])
if __name__ == "__main__":
    E = 3
    V = 3
    p = [8 for _ in range(V)]
    B = 1
    out_dir = Path(__file__).parent / "agendas"
    out_dir.mkdir(exist_ok=True)
    
    for i in range(10):
        ag = generate_all_agendas(i, E)
        save_instance_json(out_dir / f"instance_{i}.json",i,E,V,p,B,_schedule(),ag)
        csv_path = out_dir / f"agendas_{i}.csv"
        save_agendas_csv(ag, csv_path)
        display_agendas(source=str(csv_path), index_col=0,
                        save_path=str(out_dir / f"agendas_{i}.png"))
