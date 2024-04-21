import sys
import flet as ft
from cpu_chart import HomePage
import subprocess
import fcntl
import os

from power_mode_utils import change_power_mode, get_current_power_mode, get_modes_avalible


def verificar_contrasena(contrasena):
    comando_verificación = f"echo {contrasena} | sudo -S echo autenticado"
    try:
        subprocess.run(comando_verificación, shell=True, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError:
        return False


def ejecutar_con_sudo(comando, contrasena):
    # Agregar 'sudo' al inicio del comando
    comando_con_sudo = f"sudo {comando}"

    # Verificar la contraseña
    if not verificar_contrasena(contrasena):
        print("Contraseña incorrecta. No se puede ejecutar el comando con permisos sudo.")
        return

    # Ejecutar el comando con permisos sudo
    try:
        salida = subprocess.run(comando_con_sudo, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Salida estándar:")
        print(salida.stdout)
        print("Salida de error:")
        print(salida.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")


def main(page: ft.Page):
    page.window_width = 750
    page.window_height = 500
    page.update()
    modes = get_modes_avalible()
    # radios=[]
    # for mode in modes:
    #     if mode == 'performance':
    #         radios.append(ft.Radio(value="performance", label="Performance"))
    #     elif mode == 'balanced':
    #         radios.append(ft.Radio(value="balanced", label="Balanced"))
    #     elif mode == 'power-saver':
    #         radios.append(ft.Radio(value="power-saver", label="Power Saver")) 

    mode_labels = {
        'performance': "Performance",
        'balanced': "Balanced",
        'power-saver': "Power Saver"
    }
    
    radios = [ft.Radio(value=mode, label=label)
              for mode, label in mode_labels.items() if mode in modes]

    page.add(HomePage())

    def radiogroup_changed(e):
        change_power_mode(e.control.value, modes)
        page.update()

    # Obtenemos el perfil de energía actual
    current_mode = get_current_power_mode()
    cg = ft.RadioGroup(value=current_mode, content=ft.Column(
        radios), on_change=radiogroup_changed)

    page.add(ft.Text("Power Mode:"), cg)


def check_lock():
    lock_file = '/tmp/my_app.lock'
    try:
        # Intentamos abrir el archivo de bloqueo en modo de lectura/escritura
        # y con la bandera de bloqueo exclusivo.
        fd = os.open(lock_file, os.O_CREAT | os.O_RDWR)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Si logramos bloquear el archivo, significa que somos la única instancia en ejecución.
        return False
    except (IOError, OSError):
        # Si no podemos bloquear el archivo, significa que otra instancia ya está en ejecución.
        sys.exit(1)


if __name__ == "__main__":
    if check_lock():
        pass
    else:
        print("La aplicación se está ejecutando por primera vez.")

        ft.app(main)
