def clearFileName(name):
    chars_to_remove = ["|", "<", ">", ":", "\"", "\\", "/", "?", "*"]
    for char in chars_to_remove:
        name  = name.replace(char, "")
    return name