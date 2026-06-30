#Il s'agit d’un programme python qui permet de transformer les coordonnées cartésiennes du dessins à faire en coordonnée moteur, cette solution est fonctionnelle
#mais manque quelque peu de confort. N’ayant que des bases en informatique j’ai fait appel à une intelligence artificielle générative (chat gpt), qui m’a permis
#de décrire les fonctions que je souhaitait en langage clair afin qu’il me les écrivent, bien que j’ai lu, et compris, le code fournie qui semble cohérent,
#j’invite quiconque s’en sert à ne pas s’y fier et à le relire. Une avancée majeure du projet serait de recoder ce programme, et de lui donner une interface
#graphique.
import re
import math


# =========================================================
# CONFIGURATION
# =========================================================

INPUT_FILE = "test_pole_Smart.gcode"
OUTPUT_FILE = "test_pole_Smart_transforme.gcode"

# Distance entre les moteurs (mm)
MACHINE_WIDTH = 1100

# Taille max des segments (mm)
SEGMENT_LENGTH = 1.0

# Délai après chaque commande M3 (ms)
DWELL_AFTER_M3_MS = 500

# ---------------------------------------------------------
# Longueurs des courroies quand le stylo est
# au coin haut-gauche du dessin
# ---------------------------------------------------------

ORIGIN_LEFT_LENGTH = 805
ORIGIN_RIGHT_LENGTH = 860

# ---------------------------------------------------------
# Position réelle du coin haut-gauche du dessin
# dans la machine (coordonnées XY machine)
# ---------------------------------------------------------

DRAWING_ORIGIN_X = ((ORIGIN_LEFT_LENGTH**2) - (ORIGIN_RIGHT_LENGTH**2) + (MACHINE_WIDTH**2))/(2* MACHINE_WIDTH) #reconversion en coordonnée cartésienne 
DRAWING_ORIGIN_Y = math.sqrt((ORIGIN_LEFT_LENGTH**2) - (DRAWING_ORIGIN_X**2))



# ---------------------------------------------------------
# Translation du GCODE
# remet le dessin à partir de (0,0)
# ---------------------------------------------------------

TARGET_MIN_X = 0.0
TARGET_MIN_Y = 0.0


# =========================================================
# PARSING GCODE
# =========================================================

def parse_gcode_line(line):

    # Suppression commentaires
    clean_line = re.sub(r'\(.*?\)', '', line)
    clean_line = clean_line.split(';')[0].strip()

    if not clean_line:
        return None

    # Extraction tokens
    tokens = re.findall(
        r'([A-Z])([-+]?[0-9]*\.?[0-9]+)',
        clean_line.upper()
    )

    if not tokens:
        return None

    result = {
        "command_type": None,
        "command_code": None,
        "params": {},
        "raw": line.strip()
    }

    for letter, value in tokens:

        # Conversion numérique
        if "." in value:
            value = float(value)
        else:
            value = int(value)

        # Commande principale
        if (
            letter in ["G", "M", "T"]
            and result["command_type"] is None
        ):

            result["command_type"] = letter
            result["command_code"] = value

        else:
            result["params"][letter] = value

    return result


# =========================================================
# LECTURE FICHIER
# =========================================================

def read_gcode_file(filepath):

    metadata = {}
    commands = []

    with open(filepath, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            stripped = line.strip()

            # Metadata
            if stripped.startswith(";"):

                match = re.match(
                    r";([A-Z0-9_]+):(.+)",
                    stripped
                )

                if match:

                    key = match.group(1)
                    value = match.group(2).strip()

                    try:
                        if "." in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except:
                        pass

                    metadata[key] = value

                continue

            parsed = parse_gcode_line(line)

            if parsed:
                parsed["line_number"] = line_number
                commands.append(parsed)

    return {
        "metadata": metadata,
        "commands": commands
    }


# =========================================================
# SEGMENTATION
# =========================================================

def segment_line(
    x1,
    y1,
    x2,
    y2,
    segment_length
):

    dx = x2 - x1
    dy = y2 - y1

    distance = math.sqrt(dx**2 + dy**2)

    if distance == 0:
        return [(x1, y1)]

    steps = max(
        1,
        int(distance / segment_length)
    )

    points = []

    for i in range(1, steps + 1):

        t = i / steps

        x = x1 + dx * t
        y = y1 + dy * t

        points.append((x, y))

    return points


# =========================================================
# GEOMETRIE POLARGRAPH
# =========================================================

def belt_lengths_from_xy(
    x,
    y,
    machine_width
):

    left = math.sqrt(
        x**2 +
        y**2
    )

    right = math.sqrt(
        (machine_width - x)**2 +
        y**2
    )

    return left, right


# =========================================================
# XY DESSIN -> LONGUEURS COURROIES
# =========================================================

def drawing_xy_to_belts(
    drawing_x,
    drawing_y,
    machine_width,
    drawing_origin_x,
    drawing_origin_y,
    origin_left_length,
    origin_right_length
):

    # -----------------------------------------------------
    # Position absolue dans la machine
    # -----------------------------------------------------

    machine_x = drawing_origin_x + drawing_x
    machine_y = drawing_origin_y + drawing_y

    # -----------------------------------------------------
    # Longueurs géométriques du point courant
    # -----------------------------------------------------

    current_left_geom, current_right_geom = (
        belt_lengths_from_xy(
            machine_x,
            machine_y,
            machine_width
        )
    )

    # -----------------------------------------------------
    # Longueurs géométriques du point origine dessin
    # -----------------------------------------------------

    origin_left_geom, origin_right_geom = (
        belt_lengths_from_xy(
            drawing_origin_x,
            drawing_origin_y,
            machine_width
        )
    )

    # -----------------------------------------------------
    # Delta géométrique
    # -----------------------------------------------------

    delta_left = (
        current_left_geom -
        origin_left_geom
    )

    delta_right = (
        current_right_geom -
        origin_right_geom
    )

    # -----------------------------------------------------
    # Longueurs finales
    # -----------------------------------------------------

    final_left = (
        origin_left_length +
        delta_left
    )

    final_right = (
        origin_right_length +
        delta_right
    )

    return final_left, final_right


# =========================================================
# CONVERSION COMPLETE
# =========================================================

def convert_to_polargraph(
    commands,
    machine_width,
    segment_length
):

    converted = []

    current_x = 0
    current_y = 0

    for cmd in commands:

        cmd_type = cmd["command_type"]
        cmd_code = cmd["command_code"]

        # -------------------------------------------------
        # G0 / G1
        # -------------------------------------------------

        if (
            cmd_type == "G"
            and cmd_code in [0, 1]
        ):

            target_x = cmd["params"].get(
                "X",
                current_x
            )

            target_y = cmd["params"].get(
                "Y",
                current_y
            )

            feedrate = cmd["params"].get(
                "F",
                None
            )

            # ---------------------------------------------
            # Découpage segments
            # ---------------------------------------------

            points = segment_line(
                current_x,
                current_y,
                target_x,
                target_y,
                segment_length
            )

            # ---------------------------------------------
            # Conversion segments
            # ---------------------------------------------

            for x, y in points:

                left, right = (
                    drawing_xy_to_belts(
                        x,
                        y,
                        machine_width,
                        DRAWING_ORIGIN_X,
                        DRAWING_ORIGIN_Y,
                        ORIGIN_LEFT_LENGTH,
                        ORIGIN_RIGHT_LENGTH
                    )
                )

                new_cmd = {
                    "command_type": "G",
                    "command_code": 1,
                    "params": {
                        "X": round(left, 3),
                        "Y": round(right, 3)
                    }
                }

                # Feedrate à la fin
                if feedrate is not None:
                    new_cmd["params"]["F"] = feedrate

                converted.append(new_cmd)

            current_x = target_x
            current_y = target_y

        else:

            # Copie autres commandes
            converted.append(cmd)

            # Ajoute un délai juste APRES chaque M3 S...
            if (
                cmd["command_type"] == "M"
                and cmd["command_code"] == 3
                and "S" in cmd["params"]
            ):
                converted.append({
                    "command_type": "G",
                    "command_code": 4,
                    "params": {
                        "P": DWELL_AFTER_M3_MS
                    }
                })

    return converted


# =========================================================
# GENERATION GCODE
# =========================================================

def write_gcode(
    output_path,
    metadata,
    commands
):

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            ";Converted to Polargraph\n"
        )

        # Metadata
        for key, value in metadata.items():

            file.write(
                f";{key}:{value}\n"
            )

        file.write("\n")

        # Commandes
        for cmd in commands:

            line = (
                f"{cmd['command_type']}"
                f"{cmd['command_code']}"
            )

            params = cmd["params"]

            # Paramètres sauf F
            for key, value in params.items():

                if key == "F":
                    continue

                if isinstance(value, float):
                    value = round(value, 3)

                line += f" {key}{value}"

            # Feedrate à la fin
            if "F" in params:

                value = params["F"]

                if isinstance(value, float):
                    value = round(value, 3)

                line += f" F{value}"

            file.write(line + "\n")


# =========================================================
# MAIN
# =========================================================

def main():

    print("Lecture GCODE...")
    data = read_gcode_file(INPUT_FILE)

    print("Conversion Polargraph...")
    polar_commands = convert_to_polargraph(
        data["commands"],
        MACHINE_WIDTH,
        SEGMENT_LENGTH
    )

    print("Ecriture fichier...")
    write_gcode(
        OUTPUT_FILE,
        data["metadata"],
        polar_commands
    )

    print("Terminé.")
    print(f"Fichier généré : {OUTPUT_FILE}")


# =========================================================

if __name__ == "__main__":
    main()
