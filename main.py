
import flet as ft
from cpu_chart import CpuChart


def main(page: ft.Page):
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

    ch = CpuChart()
    
    page.add(ch)
    
    # data_1[0].data_points[0].x


ft.app(main)
