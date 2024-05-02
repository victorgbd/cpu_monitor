import flet as ft

class IntelGpuChart(ft.LineChart):
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
                below_line_bgcolor=ft.colors.with_opacity(0.2,'cyan'),
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
                ),
                ft.ChartAxisLabel(
                    value=100,
                    label=ft.Text("100%", size=10, weight=ft.FontWeight.BOLD),
                ),
            ],
            labels_size=40,
        )

        self.min_y = 0
        self.max_y = 100
        self.max_x = 20

        self.expand = True

    def update_data(self, x, gpu_utilization):
        if len(self.data_series[0].data_points) > 20:
            self.data_series[0].data_points.pop(0)
            self.max_x = x
        self.data_series[0].data_points.append(
            ft.LineChartDataPoint(x, gpu_utilization))
        self.min_x = self.data_series[0].data_points[0].x
        