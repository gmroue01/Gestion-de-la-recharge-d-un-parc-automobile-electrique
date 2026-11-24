import json
from pathlib import Path
def save_instance_json(save_path : Path, 
                       instance_id : int,
                       E : int, 
                       V : int,
                       p : list[int],
                       B : int,
                       slot_time_labels : list[str],
                       agendas : list[str]):
    instance = {
        "id" : instance_id,
        "nb_employees" : E,
        "nb_vehicules" : V,
        "Charging_time" : p,
        "nb_charging_station" : B,
        "slot_time_labels" : slot_time_labels,
        "agendas_per_employee" : agendas
    }

    with open(save_path,"w",encoding='utf-8') as f:
        json.dump(instance,f,ensure_ascii=False,indent=2)

    return instance