import psutil
import asyncio
import flet as ft


class CpuChart(ft.LineChart):
    def __init__(self):
        super().__init__()
        self.interactive = False
        self.data_series = [
            ft.LineChartData(
                data_points=[
                ],
                stroke_width=1,
                color=ft.colors.CYAN,
                stroke_cap_round=True,
                curved=True,
                below_line_bgcolor=ft.colors.CYAN,
                prevent_curve_over_shooting=True
            )

        ]
        self.animate = 0
        self.border = ft.border.all(
            3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE))
        self.horizontal_grid_lines = ft.ChartGridLines(
            interval=50, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
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

        # self.tooltip_bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY)
        self.min_y = 0
        self.max_y = 100
        self.max_x = 20

        self.expand = True

    def update_data(self, x, cpu_utilization):
        if len(self.data_series[0].data_points) > 20:
            self.data_series[0].data_points.pop(0)
            self.max_x = x
        self.data_series[0].data_points.append(
            ft.LineChartDataPoint(x, cpu_utilization))
        self.min_x = self.data_series[0].data_points[0].x


class HomePage(ft.Container):
    def __init__(self, x=0):
        super().__init__()
        self.x = x
        self.cpu_chart = CpuChart()
        self.cpu_usage = 0
        self.text_cpu = ft.Text('Uso de CPU:{}%'.format(self.cpu_usage))
        self.content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.END,controls=[ft.Container(height=200, content=self.cpu_chart), ft.Container(width=120,
                                                                                                          height=50, content=self.text_cpu)])

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_usage)

    def will_unmount(self):
        self.running = False

    async def update_usage(self):
        while self.running:
            self.cpu_usage = psutil.cpu_percent(interval=1)
            self.cpu_chart.update_data(self.x, self.cpu_usage)
            self.text_cpu.value = 'Uso de CPU:{}%'.format(self.cpu_usage)
            self.x += 1
            self.update()
            await asyncio.sleep(0.01)
