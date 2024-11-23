import json

class JsonHandler:
    def JsonReader(self, folder):
        with open(folder, 'r') as f:
            filecontent = json.load(f)
            f.close
            return filecontent
    def JsonWriter(self, folder, info):
        with open(folder, "w") as f:
            Jsoninfo = json.dumps(info, indent=4)
            f.write(Jsoninfo)
            f.close