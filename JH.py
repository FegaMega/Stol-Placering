import json

def JsonReader(folder):
    with open(folder, 'r') as f:
        filecontent = json.load(f)
        f.close
        return filecontent
def JsonWriter(folder, Content):
    with open(folder, "w") as f:
        Jsoninfo = json.dumps(Content, indent=4)
        f.write(Jsoninfo)
        f.close