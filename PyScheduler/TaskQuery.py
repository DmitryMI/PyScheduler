import subprocess

TASK_QUERY_OK = 0
TASK_QUERY_FAIL = -1

class TaskDescription():
    def __init__(self, path, time, status):
        self.path = path
        self.time = time
        self.status = status

    def __str__(self):
        return f"Name: {self.path}; Time: {self.time}; Status: {self.status}"

class TaskQuery:
    def __init__(self):
        self.csv_text = None

    @staticmethod
    def strip_csv(text):
        text = text.strip()        
        return text

    def read_csv(self):
        # SCHTASKS /QUERY /FO CSV /NH
        process = subprocess.Popen(['SCHTASKS', '/QUERY', '/FO', 'CSV', '/NH'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
        lines = []
        while True:
            output = process.stdout.readline()

            line = TaskQuery.strip_csv(output)            
            if not line.isspace() and len(line) > 0:
                lines.append(line)

            return_code = process.poll()
            if return_code is not None:
                print('QUERY RETURN CODE', return_code)
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    line = TaskQuery.strip_csv(output)            
                    if not line.isspace() and len(line) > 0:
                        lines.append(line)
                break

        if(return_code != 0):
            return return_code
        
        self.csv_text = lines
        return 0

    def get_tasks(self):
        tasks = []
        for line in self.csv_text:
            values = line.split(',')            
            task = TaskDescription(values[0].strip(' "'), values[1].strip(' "'), values[2].strip(' "'))
            tasks.append(task)

        return tasks

    def get_tasks_from_dir(self, path):
        tasks = []

        if path is None or path.isspace() or len(path) == 0:
            return self.get_tasks()

        folder_mask = path
        if folder_mask[0] != '\\':
            folder_mask = '\\' + folder_mask
        
        if folder_mask[len(folder_mask) - 1] != '\\':
            folder_mask = folder_mask + '\\'

        for line in self.csv_text:
            values = line.split(',')
            name = values[0].strip(' "')
            if name.startswith(folder_mask):
                task = TaskDescription(name, values[1].strip(' "'), values[2].strip(' "'))
                tasks.append(task)

        return tasks