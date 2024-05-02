import subprocess
import re
import time

import flet as ft
import os



class Utils():
    def __init__(self) -> None:
        pass

    def get_modes_avalible():
        command = "powerprofilesctl list | grep -iE 'power-saver|balanced|performance'"

        # Ejecutar el comando y capturar la salida
        output = subprocess.check_output(command, shell=True)

        # Decodificar la salida a cadena de texto
        output = output.decode('utf-8')
        patron = r'[\w-]+(?=:|\n)'
        resultados = re.findall(patron, output)
        return resultados

    def change_power_mode(mode, modes=["power-saver", "balanced", "performance"]):

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

    def get_available_power_modes():
        try:
            result = subprocess.run(
                "powerprofilesctl list", shell=True, check=True, capture_output=True, text=True)
            available_modes = [mode.split(":")[0].strip(
            ) for mode in result.stdout.split("\n") if ":" in mode]
            print("Modos de energía disponibles:")
            for mode in available_modes:
                print(mode)
            return available_modes
        except subprocess.CalledProcessError as e:
            print(f"Error al obtener los modos de energía disponibles: {e}")
            return None

    def get_nvidia_gpu_use_temp():
        try:
            comando = "nvidia-smi --query-gpu=temperature.gpu,utilization.gpu --format=csv,noheader"
            resultado = subprocess.run(
                comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
            if resultado.returncode == 0:
                salida = resultado.stdout.strip().split(',')
                temperatura = int(salida[0])
                utilizacion = int(salida[1].split()[0])
                return utilizacion, temperatura
            else:
                print("Error al ejecutar el comando nvidia-smi:", resultado.stderr)
                return None, None
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando nvidia-smi: {e}")
            return None, None

    def get_intel_gpu_3d_use():
        proceso = None
        try:
            proceso = subprocess.Popen(
                ["sudo", "intel_gpu_top", "-l"], stdout=subprocess.PIPE)
            i = 0
            for linea in proceso.stdout:
                linea_decodificada = linea.decode("utf-8")
                if i == 2:
                    porcentaje = linea_decodificada.split()
                    cadena_sin_espacios = " ".join(porcentaje)
                    porcentajes = cadena_sin_espacios.split(' ')
                    return int(float(porcentajes[8]))
                if i == 2:
                    proceso.terminate()
                    break
                i = i+1
            return None
        except Exception as e:
            print("Error al obtener el porcentaje de uso de la GPU:", e)
            return None
        finally:
            if proceso:
                proceso.terminate()
    def validate_sudo_password(contrasena):
        comando = "echo '{}' | sudo -S echo 'Acceso concedido'".format(contrasena)
        try:
            resultado = subprocess.run(comando, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    


    

    
