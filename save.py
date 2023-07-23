import json

class SaveHistory():
    def __init__(self):
        self._filename = 'equationHistory.json'
        self.dataSaved = []
    
    def saveData(self):
        # Open the file in write mode, setting the file pointer to the beginning
        with open(self._filename, "w+", encoding='utf8') as file:
            # Load any existing data (if any) from the file
            existing_data = []
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                pass  # If the file is empty or not in JSON format, ignore the error

            # Set the file pointer to the beginning: don't work
            file.seek(0,0)

            # Combine the existing data with the new data to save
            combined_data = self.dataSaved + existing_data

            # Write the combined data back to the file
            json.dump(combined_data, file, ensure_ascii=False, indent=2)

    def loadData(self):
        with open(self._filename, "r", encoding='utf8') as file:
            self.dataSaved = json.load(file)

    def getData(self):
        return self.dataSaved

    def setData(self,data:str):
        self.dataSaved.append(data)
    
        