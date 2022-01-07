from .build import Build

def save(filename, target_type):
    build = Build(filename, target_type)
    code = build.build()
    savefile(filename, code)

def savefile(filename, script):
    if ".zpy" in filename:
        filename = filename.replace(".zpy", ".py")
    elif ".py" in filename:
        filename = filename.replace(".py", ".zpy")
    with open("./"+filename, "w") as newFile:
        newFile.write(script)