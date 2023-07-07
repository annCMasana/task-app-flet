from flet import *
from components.Task import Task

# Firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("./taskapp.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class TodoContainer(UserControl):
    
    def build(self):
        
        self.taskName = TextField(label="Task Name", width=200)
        self.description = TextField(label="Description", width=200)
        self.status = Dropdown(label="Status", width = 200, options = [
            dropdown.Option("Not Started"), # Red Border
            dropdown.Option("Started"), # Gray Border
            dropdown.Option("In Progress"), # Blue Border
            dropdown.Option("Done") # Green Border
        ])
        self.addBtn = ElevatedButton(text="+", on_click=self.addTask)
        
        inputs = Column(
            controls = [
                self.taskName,
                self.description,
                self.status
            ]
        )
        
        row = Row(
            controls=[
                inputs,
                self.addBtn
            ],
            alignment=MainAxisAlignment.CENTER
        )
        
        self.taskList = ListView(
            height = 500,
            spacing = 10
        )
        
        return Column(
            controls=[
                row,
                self.taskList
            ]
        )
        
    def did_mount(self):
        self.getTasks()
    
    
    def getTasks(self):
        tasks = db.collection(u'tasks').stream()
        self.taskList.controls.clear()
        for task in tasks :
            print(task.id)
            self.taskList.controls.append(Task(task.id, task.to_dict()['task_name'], task.to_dict()['description'], task.to_dict()['status'], self.getTasks, self.deleteTask, db))
            self.update()
        
        
    def addTask(self, e):
        # self.taskList.controls.append(Task(self.taskName.value, self.deleteTask))
        doc_ref = db.collection("tasks").document()
        doc_ref.set({
            u'task_name' : str(self.taskName.value),
            u'description' : str(self.description.value),
            u'status' : str(self.status.value)
        })
        self.taskName.value = ""
        # self.update()
        self.getTasks()
        
        
    def deleteTask(self, task):
        self.taskList.controls.remove(task)
        self.update()
        
        
        
        
        
        