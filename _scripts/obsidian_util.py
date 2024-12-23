import os
import re
import sys

LINK_REGEX = "\[\[([\w\s'`\-\+\.&!?,;]+)\]\]"

def list_files_in_directory(dir):
    """
    Reads all files in the directory and returns a list of the file paths
    """
    file_paths = []
    for f in os.listdir(dir):
        if f.endswith(".md"):
            file_paths.append(f)
    return file_paths


def list_files_in_directory_recursive(dir):
    """
    Reads all files in the directory and returns a list of the file paths recursively
    """
    file_paths = []
    for root, dirs, files in os.walk(dir):
        for f in files:
            if f.endswith(".md"):
                file_paths.append(os.path.join(root, f))
    return file_paths


def read_file(file_path):
    """
    Reads a file and returns the contents as a string
    """
    with open(file_path, "r") as f:
        file_contents = f.read()
    return file_contents


def read_file_lines(file_path):
    """
    Reads a file and returns the contents as a list of lines
    """
    with open(file_path, "r") as f:
        file_contents = f.readlines()
    return file_contents


def move_selector_to_folder(selector, folder, vault_path):
    # e.g selector = "Type: #topic"
    files = list_files_in_directory(vault_path)
    for f in files:
        file_contents = read_file(os.path.join(vault_path, f))
        if selector in file_contents:
            print(f"{f.replace('.md', '')} --> {folder}")
            os.rename(os.path.join(vault_path, f), os.path.join(vault_path, folder, f))


def create_authors(vault_path):
    dirname = os.path.join(vault_path, "Sources")
    files = list_files_in_directory(dirname)
    for f in files:
        lines = read_file_lines(os.path.join(dirname, f))
        for line in lines:
            if "Author:" in line:
                author_string = line.split(":")[1].strip()
                for author_tag in re.findall(LINK_REGEX, author_string):
                    # check if author_tag is in Authors/ or in the main folder
                    # if not, create a new file in Authors/ containing the string "Type: #author"
                    if (
                        f"{author_tag}.md"
                        in list_files_in_directory(os.path.join(vault_path, "Authors"))
                        or f"{author_tag}.md" in list_files_in_directory(vault_path)
                    ):
                        continue
                    else:
                        print(f"Creating new author: {author_tag}")
                        with open(
                            os.path.join(vault_path, "Authors", author_tag, ".md"),
                            "w"
                        ) as f:
                            f.write(f"Type: #author")


def create_topics(dirname):
    files = list_files_in_directory(dirname)
    for f in files:
        lines = read_file_lines(os.path.join(dirname, f))
        for line in lines:
            if "Topics:" in line:
                cat_string = line.split(":")[1].strip()
                for cat_tag in re.findall(LINK_REGEX, cat_string):
                    # check if cat_tag is in Authors/ or in the main folder
                    # if not, create a new file in Authors/ containing the string "Type: #author"
                    if (
                        f"{cat_tag}.md"
                        in list_files_in_directory(os.path.join(vault_path, "Topics"))
                        or f"{cat_tag}.md" in list_files_in_directory(vault_path)
                    ):
                        continue
                    else:
                        print(f"Creating new topic: {cat_tag}")
                        with open(
                        os.path.join(vault_path, "Topics", cat_tag, ".md"),
                        "w") as f:
                            f.write(f"Type: #topic")


def notes_to_review(vault_path):
    """
    Find all files in the main directory that need attention (non atoms, orphans, todos).
    """
    print("\nPlease review the following files")
    print("=================================")
    files = list_files_in_directory(vault_path)
    for f in files:
        file_contents = read_file(os.path.join(vault_path, f))
        if (
            "#atom" not in file_contents
            and "#todo" not in file_contents
            and f != "__OBSIDIAN_META__.md"
        ):
            print(f.replace(".md", ""))

    todos = []
    mentioned = set()
    not_linked_to = []
    not_linking = []

    all_files = list_files_in_directory_recursive(vault_path)

    for f in all_files:
        file_contents = read_file(os.path.join(vault_path, f))
        if "#todo" in file_contents:
            todos.append(f.replace(".md", "").replace(vault_path, "").strip("/"))
        # Find words in [[...]] and add to mentioned
        links = re.findall(LINK_REGEX, file_contents)
        if len(links) == 0:
            # These notes don't link to anything
            not_linking.append(f.split("/")[-1].replace(".md", ""))
        else:
            for word in links:
                mentioned.add(word)

    # Find notes that are not mentioned in any other file
    for f in all_files:
        note = f.split("/")[-1].replace(".md", "")
        if note not in mentioned:
            not_linked_to.append(note)

    orphans = [
        note
        for note in set(not_linked_to).intersection(set(not_linking))
        if note + ".md" not in os.listdir(os.path.join(vault_path, "_templates")) and "__" not in note
    ]

    if len(todos) > 0:
        print("\nTodos")
        print("=====")
        for note in todos:
            print(note)

    if len(orphans) > 0:
        print("\nOrphans")
        print("=======")
        for note in orphans:
            print(note)


if __name__ == "__main__":
    # Allow you to pass in a vault_path from anywhere, otherwise it defaults to the current directory you call the Python script from
    
    vault_path = "./" if len(sys.argv) == 1 else sys.argv[1]
    print("\nCleaning up Obsidian")
    print("=====================")
    move_selector_to_folder("Type: #topic", "Topics", vault_path)
    move_selector_to_folder("Type: #author", "Authors", vault_path)
    move_selector_to_folder("Type: #molecule", "Molecules", vault_path)
    move_selector_to_folder(f"Type: #source", "Sources", vault_path)

    create_authors(vault_path)
    create_topics(vault_path)
    notes_to_review(vault_path)
