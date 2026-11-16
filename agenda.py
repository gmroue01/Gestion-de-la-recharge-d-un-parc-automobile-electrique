import random 
from datetime import datetime,timedelta
TYPES_SLOT = ("available","meeting","do not disturb","break")

START_OF_A_DAY = "8:00"
END_OF_A_DAY = "17:00"
SLOT_TIME_MIN = 15





def _schedule(start : str = START_OF_A_DAY, end : str = END_OF_A_DAY, step : int = SLOT_TIME_MIN) -> list[str]:
    """
    Generate the label of each slot of the schedule.
    
    """




    start_time = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end,"%H:%M")
    duration_min = ((end_time - start_time).total_seconds() / 3600)*60
    number_slot = int(duration_min /step)

    time_slot_labels = []

    for t in range(number_slot):
        time_slot = start_time + timedelta(minutes=t*step)
        time_slot_labels.append(f"{time_slot.hour}:{time_slot.minute:02d}")
    
    
    return time_slot_labels






def generate_agendas(seed : int):

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


    w = 5
    # Pick a slot type randomly amoung the set of slot type avec remise
    rng_type_slot_list = list(random.choices(TYPES_SLOT, k = w ))
    # Pick a number of slot randomly amoung two slots (=30 min) and 8 slots (=2 hours)
    rng_size_slot_list = [random.randint(2,8) for _ in range(w)]
    # Pick a start time of the slot 
    rng_start_time_list = list(random.sample(hours,k=w))

    return agenda






if __name__=="__main__":
   print(generate_agendas(42))



