import subprocess
import sys
import flet as ft
from charts import HomePage
import fcntl
import os
import tkinter as tk


from utils import Utils as ut

def main(page: ft.Page):
    page.window_width = 750
    page.window_height = 800
    page.update()
    
    modes = ut.get_modes_avalible()
    mode_labels = {
        'performance': "Performance",
        'balanced': "Balanced",
        'power-saver': "Power Saver"
    }
    radios = [ft.Radio(value=mode, label=label)
                for mode, label in mode_labels.items() if mode in modes]
    page.add(HomePage())
    def radiogroup_changed(e):
        ut.change_power_mode(e.control.value, modes)
        page.update()

    # Obtenemos el perfil de energía actual
    current_mode = ut.get_current_power_mode()
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



def ejecutar_comando():
    password = ""

    def submit_password():
        password = password_entry.get()  # Obtén la contraseña ingresada
        # Aquí podrías realizar alguna validación o acción con la contraseña
        print("Contraseña ingresada:", password)
        if ut.validate_sudo_password(password):
            root.destroy()
        

    root = tk.Tk()

    # Etiqueta y campo de entrada para la contraseña
    password_label = tk.Label(root, text="Contraseña:")
    password_label.pack()

    password_entry = tk.Entry(root, show="*")  # La opción show="*" muestra asteriscos en lugar del texto
    password_entry.pack()

    # Botón para enviar la contraseña
    submit_button = tk.Button(root, text="Ingresar", command=submit_password)
    submit_button.pack()

    root.mainloop()

    # Comando sudo que quieres ejecutar
    sudo_command = f"echo {password} | sudo -S echo hola"

    try:
        subprocess.run(
                sudo_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        # process = subprocess.Popen(sudo_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # stdout, stderr = process.communicate()
    except Exception as e:
        print("Error:", e)

   

if __name__ == "__main__":
    if check_lock():
        pass
    else:
        ejecutar_comando()
        print("La aplicación se está ejecutando por primera vez.")
        ft.app(main)
        
                
