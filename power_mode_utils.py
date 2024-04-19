import subprocess


def change_power_mode(mode):
    modes = ["power-saver", "balanced", "performance"]
    if mode not in modes:
        print("Modo de energía no válido.")
        return

    command = f"powerprofilesctl set {mode}"
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Modo de energía cambiado a: {mode}")
    except subprocess.CalledProcessError as e:
        print(f"Error al cambiar el modo de energía: {e}")


def get_current_power_mode():
    try:
        result = subprocess.run(
            "powerprofilesctl get", shell=True, check=True, capture_output=True, text=True)
        current_mode = result.stdout.strip()
        print(f"El perfil de energía actual es: {current_mode}")
        return current_mode
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener el perfil de energía actual: {e}")
        return None
