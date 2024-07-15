def write_to_file(filepath, content):
    try:
        with open(filepath, "w") as file:
            file.write(content)
    except Exception as e:
        print(f"Failed to write to {filepath}: {e}")
