from typing import Optional
import psutil
import asyncio
import flet as ft
from cpu_chart import CpuChart
from gpu_chart import GpuChart
from intel_gpu_chart import IntelGpuChart
from utils import Utils as ut



class HomePage(ft.Container):
    def __init__(self, x=0,):
        super().__init__()
        self.x = x
        self.cpu_temp = 0
        self.cpu_usage = 0
        self.cpu_chart = CpuChart()
        self.text_cpu = ft.Text('Uso de CPU:{}%'.format(self.cpu_usage))
        self.text_cpu_temp = ft.Text('Temp de CPU:{}°'.format(self.cpu_temp))
        self.gpu_temp = 0
        self.gpu_usage = 0
        self.gpu_chart = GpuChart()
        self.text_gpu = ft.Text('Uso de GPU:{}%'.format(self.gpu_usage))
        self.text_gpu_temp = ft.Text('Temp de GPU:{}°'.format(self.gpu_temp))
        self.igpu_usage = 0
        self.igpu_chart = IntelGpuChart()
        self.text_igpu = ft.Text('Uso de iGPU:{}%'.format(self.igpu_usage))
        self.content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.END,
                                 controls=[ft.Container(height=150, content=self.cpu_chart), 
                                           ft.Container(width=130,height=20, content=self.text_cpu),
                                           ft.Container(width=130,height=20, content=self.text_cpu_temp),
                                           ft.Container(height=150, content=self.gpu_chart), 
                                           ft.Container(width=130,height=20, content=self.text_gpu),
                                           ft.Container(width=130,height=20, content=self.text_gpu_temp),
                                           ft.Container(height=150, content=self.igpu_chart), 
                                           ft.Container(width=130,height=20, content=self.text_igpu),
                                           ])

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_usage)

    def will_unmount(self):
        self.running = False

    async def update_usage(self):
        while self.running:
            self.cpu_usage = psutil.cpu_percent(interval=1)
            sensors = psutil.sensors_temperatures()
            cpu_sensor = sensors['coretemp'][0]
            self.cpu_temp=cpu_sensor.current
            self.gpu_usage,self.gpu_temp = ut.get_nvidia_gpu_use_temp()
            self.igpu_usage=ut.get_intel_gpu_3d_use()
            self.cpu_chart.update_data(self.x, self.cpu_usage,self.cpu_temp)
            self.gpu_chart.update_data(self.x,self.gpu_usage,self.gpu_temp)
            self.igpu_chart.update_data(self.x,self.igpu_usage)
            self.text_cpu.value = 'Uso de CPU:{}%'.format(self.cpu_usage)
            self.text_cpu_temp.value ='Temp de CPU:{}°'.format(self.cpu_temp)
            self.text_gpu.value = 'Uso de GPU:{}%'.format(self.gpu_usage)
            self.text_gpu_temp.value ='Temp de GPU:{}°'.format(self.gpu_temp)
            self.text_igpu.value = 'Uso de iGPU:{}%'.format(self.igpu_usage)

            self.x += 1
            self.update()
            await asyncio.sleep(0.1)
