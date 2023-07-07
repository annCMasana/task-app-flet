from flet import *
from components.TaskContainer import TodoContainer



def main(page: Page):
    page.title = "Task Application"
    page.window_height = 1000
    page.window_width = 600
    page.bgcolor = "#adf7b6"
    page.window_center()
    
    page.add(
        TodoContainer()
    )
    page.update()
    
app(target=main)