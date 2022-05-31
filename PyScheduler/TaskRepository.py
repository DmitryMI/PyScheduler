import os.path
import xml
from xml.etree.ElementTree import Element, ElementTree, SubElement

TASK_REPOSITORY_DEFAULT_PATH = "task_repository.xml"

class TaskRepository:
    def __init__(self, xml_path=None):
        self.xml_path = xml_path
        if self.xml_path is None:
            self.xml_path = TaskRepository.get_repository_absolute_location()

        self._ensure_repository_exists()

    def _ensure_repository_exists(self):
        if os.path.exists(self.xml_path):
            return

        top = Element('root')
        element_tree = ElementTree(top)  
        element_tree.write(self.xml_path, encoding="utf-8")

    def add_task(self, name, command):

        if self.has_name(name):
            return False

        element_tree = ElementTree()
        element_tree.parse(self.xml_path)
        root = element_tree.getroot()

        task_element = SubElement(root, 'Task', {'name': name, 'command': command})

        element_tree.write(self.xml_path, encoding="utf-8")
        return True

    def remove_task(self, name):
        element_tree = ElementTree()
        element_tree.parse(self.xml_path)
        root = element_tree.getroot()

        tasks = root.findall("Task")
        for task in tasks:
            if task.get("name") == name:
                root.remove(task)

        element_tree.write(self.xml_path, encoding="utf-8")

    def get_task_command(self, name):
        element_tree = ElementTree()
        element_tree.parse(self.xml_path)
        root = element_tree.getroot()

        tasks = root.findall("Task")
        for task in tasks:
            if task.get("name") == name:
                return task.get("command")

        return None

    def _get_all_tasks(self):
        element_tree = ElementTree()
        element_tree.parse(self.xml_path)
        root = element_tree.getroot()

        tasks = root.findall("Task")
        return tasks

    def has_name(self, name):
        element_tree = ElementTree()
        element_tree.parse(self.xml_path)
        root = element_tree.getroot()

        tasks = root.findall("Task")

        for task in tasks:
            if task.get("name") == name:
                return True
        return False

    def generate_name(self, prefix):
        tasks = self._get_all_tasks()

        counter = 1 
        name = prefix + str(counter)
        while True:
            collision_found = False
            for task in tasks:
                if task.get("name") == name:
                    counter += 1
                    collision_found = True
                    break

            name = prefix + str(counter)

            if not collision_found:
                break

        return name

    @staticmethod
    def get_repository_absolute_location():
        path_abs = os.path.realpath(__file__)
        folder_abs = os.path.dirname(path_abs)
        return os.path.join(folder_abs, TASK_REPOSITORY_DEFAULT_PATH) 
    

