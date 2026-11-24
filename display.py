import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle


def display_agendas(source, s=15, heure_debut=8.0,
                     slot_type=("available", "do not disturb", "break", "meeting"),
                     noms=None, index_col=None, save_path=None):
    """
    Affiche les agendas en diagramme de Gantt.

    source      : chemin vers un CSV, DataFrame ou array (lignes = employés, colonnes = créneaux).
                  Les valeurs peuvent être des codes (0..3) ou des libellés ("meeting", ...).
    s           : durée d'un créneau (min)
    heure_debut : heure de début de journée (ex : 8.0 = 8h00, 8.5 = 8h30)
    slot_type   : libellés des types de créneaux, dans l'ordre des codes
    noms        : noms des lignes (par défaut "Employé 0", "Employé 1", ...)
    index_col   : colonne d'index du CSV, si le fichier en a une
    save_path   : chemin de sauvegarde de la figure (ex : ".../agendas.png").
                  None = pas de sauvegarde.
    """
    # --- Lecture et conversion en matrice d'entiers ---
    if isinstance(source, str):
        df = pd.read_csv(source, index_col=index_col)
    elif isinstance(source, pd.DataFrame):
        df = source.copy()
    else:
        df = pd.DataFrame(np.asarray(source))
    codes = {nom: i for i, nom in enumerate(slot_type)}
    A = df.replace(codes).to_numpy().astype(int)

    E, nT = A.shape
    d = s / 60                                   # durée d'un créneau (h)
    h = lambda t: heure_debut + t * d            # créneau -> heure
    noms = noms or [f"Employé {e}" for e in range(E)]
    palette = ["#e8e8e8", "#f4b183", "#a9d18e", "#ff7c7c", "#b4a7d6", "#ffe699"]

    # --- Tracé ---
    fig, ax = plt.subplots(figsize=(max(12, 0.4 * nT), 1.8 + 0.8 * E))
    for e in range(E):
        for t in range(nT):
            ax.add_patch(Rectangle((h(t), e - 0.4), d, 0.8,
                                   facecolor=palette[A[e, t] % len(palette)],
                                   edgecolor="white", lw=1.5))

    ax.set_xlim(h(0), h(nT))
    ax.set_ylim(E - 0.5, -0.5)
    ax.set_yticks(range(E))
    ax.set_yticklabels(noms)

    heures = np.arange(heure_debut, h(nT) + 1e-9, 1)
    ax.set_xticks(heures)
    ax.set_xticklabels([f"{int(x)}h{int(round((x % 1) * 60)):02d}" for x in heures])
    ax.set_xticks([h(t) for t in range(nT + 1)], minor=True)
    ax.grid(which="major", axis="x", color="black", alpha=0.35)

    sec = ax.secondary_xaxis("top", functions=(lambda x: (x - heure_debut) / d,
                                               lambda t: heure_debut + t * d))
    sec.set_xticks([t + 0.5 for t in range(nT)])
    sec.set_xticklabels([str(t) for t in range(nT)], fontsize=7)
    sec.set_xlabel(f"créneau t ({s} min)")

    ax.legend(handles=[mpatches.Patch(color=palette[i], label=nom)
                       for i, nom in enumerate(slot_type)],
              loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=len(slot_type))
    ax.set_title("Agendas des employés", pad=30)
    plt.tight_layout()

    # --- Sauvegarde (avant plt.show, sinon l'image est blanche) ---
    if save_path is not None:
        dossier = os.path.dirname(save_path)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        fig.savefig(save_path, dpi=200, bbox_inches="tight")
        print(f"Agendas sauvegardés : {save_path}")

    plt.show()