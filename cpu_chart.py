import psutil
import asyncio
import flet as ft


class CpuChart(ft.LineChart):
    def __init__(self, x=0):
        super().__init__()
        self.x = x
        self.data_series = [
            ft.LineChartData(
                data_points=[
                ],
                stroke_width=1,
                color=ft.colors.CYAN,
                stroke_cap_round=True,
                curved=True,
                prevent_curve_over_shooting=True
            )

        ]
        self.border = ft.border.all(
            3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE))
        self.horizontal_grid_lines = ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
        )
        self.vertical_grid_lines = ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
        )
        self.left_axis = ft.ChartAxis(
            labels=[

                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Text("0%", size=10, weight=ft.FontWeight.BOLD),
                ), ft.ChartAxisLabel(
                    value=50,
                    label=ft.Text("50%", size=10, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=100,
                    label=ft.Text("100%", size=10, weight=ft.FontWeight.BOLD),
                ),
            ],
            labels_size=40,
        )

        self.tooltip_bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY)
        self.min_y = 0
        self.max_y = 100
        self.max_x = 10

        self.expand = True

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_usage)

    def will_unmount(self):
        self.running = False

    async def update_usage(self):
        while self.running:
            cpu_usage = psutil.cpu_percent(interval=1)
            self.update_data(self.x, cpu_usage)
            self.update()
            await asyncio.sleep(0.2)

    def update_data(self, x, cpu_utilization):
        if len(self.data_series[0].data_points) > 10:
            self.data_series[0].data_points.pop(0)
            self.max_x = x
        self.data_series[0].data_points.append(
            ft.LineChartDataPoint(self.x, cpu_utilization))
        
        self.min_x = self.data_series[0].data_points[0].x
        self.x += 1
