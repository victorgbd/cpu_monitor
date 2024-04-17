import flet as ft
from cpu_chart import CpuChart
from cpu_chart import HomePage


def main(page: ft.Page):
    # page.window_width = 350        
    # page.window_height = 350 
    # page.update()
    data_1 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(0, 3),
                ft.LineChartDataPoint(2.6, 2),
                ft.LineChartDataPoint(4.9, 5),
                ft.LineChartDataPoint(6.8, 100),
                ft.LineChartDataPoint(8, 4),
                ft.LineChartDataPoint(9.5, 50),
                ft.LineChartDataPoint(11, 4),
            ],
            stroke_width=1,
            color=ft.colors.CYAN,
            # curved=True,
            stroke_cap_round=True,
        )
    ]
    
    page.add(HomePage(cpu_chart=CpuChart()))
    
    # data_1[0].data_points[0].x


ft.app(main)
