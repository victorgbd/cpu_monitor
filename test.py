
import tkinter as tk
import subprocess
from utils import Utils as ut
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

# La opción show="*" muestra asteriscos en lugar del texto
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Botón para enviar la contraseña
submit_button = tk.Button(root, text="Ingresar", command=submit_password)
submit_button.pack()

root.mainloop()

# Comando sudo que quieres ejecutar
sudo_command = f"echo {password} | sudo -S su"

try:
    
    process = subprocess.Popen(sudo_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
except Exception as e:
    print("Error:", e)
