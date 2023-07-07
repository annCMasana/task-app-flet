from flet import *


class Task(UserControl):
    def __init__(self, id, taskName, description, status, getTasks, deleteTodo, db):
        super().__init__()
        self.id = id
        self.taskName = taskName
        self.description = description
        self.status = status
        self.getTasks = getTasks
        self.delete = deleteTodo
        self.db = db
        
    def build(self):
        self.text1 = Text(value=str(self.taskName), size=20)
        self.text2 = Text(value=str(self.description), size=20)
        self.text3 = Text(value=str(self.status), size=20)
        self.editbtn = IconButton(icon=icons.EDIT, on_click=self.showEdit)
        self.deletebtn = IconButton(icon=icons.DELETE, on_click=self.deleteTodo)
        self.editTaskName = TextField(value=str(self.taskName))
        self.editDescription = TextField(value=str(self.description))
        self.editStatus = Dropdown(value=str(self.status), options = [
            dropdown.Option("Not Started"), # Red Border
            dropdown.Option("Started"), # Gray Border
            dropdown.Option("In Progress"), # Blue Border
            dropdown.Option("Done") # Green Border
        ])
        self.savebtn = IconButton(icon=icons.CHECK, on_click=self.updateTask)
        self.cancelbtn = IconButton(icon=icons.CANCEL, on_click=self.cancelEdit)
        
        # d1 = Row(
        #     controls=[
        #         self.chkbox
        #     ],
        #     alignment=MainAxisAlignment.END
        # )
        d2 = Column(
            controls=[
                self.text1,
                self.text2,
                self.text3
            ],
            alignment=MainAxisAlignment.START
        )
        d3 = Row(
            controls=[
                self.editbtn,
                self.deletebtn
            ],
            alignment=MainAxisAlignment.END
        )
        
        
        self.itemrow = Container(
            content = Row(
                controls=[
                    # d1,
                    d2,
                    d3
                ],
                width=500,
                alignment=MainAxisAlignment.SPACE_BETWEEN
            ),
            width=600,
            padding=5,
            border=border.all(2.0, colors.GREEN) #if self.description else border.all(1.0, colors.RED)
        )
        
        self.editInputs = Column(
            controls = [
                self.editTaskName,
                self.editDescription,
                self.editStatus
            ]
        )
        
        self.editrow = Row(
            controls = [
                self.editInputs,
                self.savebtn,
                self.cancelbtn
            ],
            width=600,
            alignment=MainAxisAlignment.CENTER,
            visible=False
        )
        
        if self.status == "Not Started":
            self.itemrow = Container(
                content = Row(
                    controls=[
                        # d1,
                        d2,
                        d3
                    ],
                    width=500,
                    alignment=MainAxisAlignment.SPACE_BETWEEN
                ),
                width=600,
                padding=5,
                border=border.all(2.0, colors.RED) #if self.status == "Not Started" else border.all(1.0, colors.RED)
            )
            
        elif self.status == "Started":
            self.itemrow = Container(
                content = Row(
                    controls=[
                        # d1,
                        d2,
                        d3
                    ],
                    width=500,
                    alignment=MainAxisAlignment.SPACE_BETWEEN
                ),
                width=600,
                padding=5,
                border=border.all(2.0, colors.YELLOW) #if self.status == "Not Started" else border.all(1.0, colors.RED)
            )
        
        elif self.status == "In Progress":
            self.itemrow = Container(
                content = Row(
                    controls=[
                        # d1,
                        d2,
                        d3
                    ],
                    width=500,
                    alignment=MainAxisAlignment.SPACE_BETWEEN
                ),
                width=600,
                padding=5,
                border=border.all(2.0, colors.BLUE_500) #if self.status == "Not Started" else border.all(1.0, colors.RED)
            )
            
        elif self.status == "Done":
            self.itemrow = Container(
                content = Row(
                    controls=[
                        # d1,
                        d2,
                        d3
                    ],
                    width=500,
                    alignment=MainAxisAlignment.SPACE_BETWEEN
                ),
                width=600,
                padding=5,
                border=border.all(2.0, colors.GREEN) 
            )
        
        
        # self.dlg = AlertDialog(
        #     title=Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
        # )
        
        return Column(
            controls = [
                self.itemrow,
                self.editrow
            ]
        )
    
    # def open_dlg_modal(e):
    #     page.dialog = dlg_modal
    #     dlg_modal.open = True
    #     page.update()
        
    # def close_dlg(e):
    #     dlg_modal.open = False
    #     page.update()
        
    
    # dlg_modal = AlertDialog(
    #     modal=True,
    #     title=Text("Please confirm"),
    #     content=Text("Do you really want to delete all those files?"),
    #     actions=[
    #         TextButton("Yes", on_click=close_dlg),
    #         TextButton("No", on_click=close_dlg),
    #     ],
    #     actions_alignment=ft.MainAxisAlignment.END,
    #     on_dismiss=lambda e: print("Modal dialog dismissed!"),
    # )
    
    
    # def open_dlg(e):
    #     page.dialog = dlg
    #     dlg.open = True
    #     page.update()
        
        
    def showEdit(self, e):
        self.itemrow.visible=False
        self.editrow.visible=True
        self.update()
        
    def cancelEdit(self, e):
        self.itemrow.visible=True
        self.editrow.visible=False
        self.update()
        
    def updateTask(self, e):
        newTaskName = str(self.editTaskName.value)
        newDescription = str(self.editDescription.value)
        newStatus = str(self.editStatus.value)
        # self.text.value = newtaskName
        task_ref = self.db.collection(u'tasks').document(self.id)
        task_ref.update({
                u'task_name' : newTaskName,
                u'description' : newDescription,
                u'status' : newStatus,
            })
        self.editrow.visible=False
        self.itemrow.visible=True
        self.getTasks()
        
    def deleteTodo(self, e):
        self.delete(self)
        task_ref = self.db.collection(u'tasks').document(self.id)
        task_ref.delete()
        self.getTasks()
        
    # def changeStatus(self, e):
    #     task_ref = self.db.collection(u'todos').document(self.id)
    #     if(self.chkbox.value == True):
    #         task_ref.update({
    #             u'description' : not self.description
    #         })
    #     #     self.itemrow.border = border.all(2.0, colors.GREEN)
    #     else:
    #         task_ref.update({
    #             u'description' : not self.description
    #         })
    #     #     self.itemrow.border = border.all(1.0, colors.RED)
    #     self.getTasks()
        
    # def open_dlg_modal(e):
    #     page.dialog = dlg_modal
    #     dlg_modal.open = True
    #     page.update()
        
    # def confirm(self, e):
    #     dlg_modal = AlertDialog(
    #         modal=True,
    #         title=Text("Please confirm"),
    #         content=Text("Do you really want to delete all those files?"),
    #         actions=[
    #             TextButton("Yes", on_click=self.deleteTodo),
    #             TextButton("No", on_click=close_dlg),
    #         ],
    #         actions_alignment=MainAxisAlignment.END,
    #         on_dismiss=lambda e: print("Modal dialog dismissed!"),
    #     )
        