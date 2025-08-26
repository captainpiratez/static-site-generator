from textnode import TextNode, TextType
import os
import shutil


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)
    print(copy_static_to_public(True))


def copy_static_to_public(first, files=[], static = "./static", public = "./public"):
    if not os.path.exists(public):
        os.mkdir(public)
    if first:
        files = os.listdir(static)
        if len(os.listdir(public)) != 0:
            shutil.rmtree(public)
            os.mkdir(public)
        first = False
    if not first and files == []:
        return True
    file = files[0]
    del files[0]
    if os.path.isfile(os.path.join(static, file)):
        shutil.copy(os.path.join(static, file), os.path.join(public, file))
        print(f"copying {file} from {static} to {public}")
    else:
        new_static = os.path.join(static, file)
        new_list = os.listdir(os.path.join(static, file))
        new_public = os.path.join(public, file)
        copy_static_to_public(first, new_list, static = new_static, public = new_public)

    return copy_static_to_public(first, files)
    
    



main()
