import sys
import flet as ft
from cpu_chart import HomePage
import subprocess
import fcntl
import os

from power_mode_utils import change_power_mode, get_current_power_mode


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
    page.window_height = 550
    # page.update()

    def ejecutar_con_sudo(e):
        # Agregar 'sudo' al inicio del comando
        comando_con_sudo = f"sudo echo hola"

        # Verificar la contraseña
        if not verificar_contrasena(textfield.value):
            print(
                "Contraseña incorrecta. No se puede ejecutar el comando con permisos sudo.")
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

    page.add(HomePage())

    def close_dlg(e):
        dlg_modal.open = False
        textfield.value = ''
        page.update()

    def on_dismiss_dlg(e):
        textfield.value = ''

    textfield = ft.TextField(label="Password", hint_text="Please enter the password",
                             password=True,  on_submit=ejecutar_con_sudo)

    dlg_modal = ft.AlertDialog(

        title=ft.Text("Please confirm"),
        content=ft.Container(height=100.0, content=ft.Column(

            controls=[ft.Text("Do you really want to delete all those files?"), textfield
                      ])),
        actions=[
            ft.TextButton("Yes", on_click=ejecutar_con_sudo),
            ft.TextButton("No", on_click=close_dlg),
        ],
        on_dismiss=on_dismiss_dlg
    )

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    page.add(
        ft.ElevatedButton("Open dialog", on_click=open_dlg_modal),
    )

    def radiogroup_changed(e):
        change_power_mode(e.control.value)
        page.update()

    # Obtenemos el perfil de energía actual
    current_mode = get_current_power_mode()
    cg = ft.RadioGroup(value=current_mode, content=ft.Column([
        ft.Radio(value="performance", label="Performance"),
        ft.Radio(value="balanced", label="Balanced"),
        ft.Radio(value="power-saver", label="Power Saver")]), on_change=radiogroup_changed)

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
