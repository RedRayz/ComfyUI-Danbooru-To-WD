import os
import requests
import re

class DanbooruToWD:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "booru_tags": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "booru_url": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
                "remove_meta_artist": ("BOOLEAN",{
                    "default": False
                }),
                "to_animagine_style": ("BOOLEAN",{
                    "default": False
                }),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "convert_to_wd"

    #OUTPUT_NODE = False

    CATEGORY = "utils"

    def convert_to_wd(
            self,
            booru_tags: str, 
            booru_url: str,
            remove_meta_artist: bool,
            to_animagine_style: bool,
            ):
        source = ""
        dest = ""
        if booru_url:
            try:
                burl = booru_url + ".json"
                with requests.get(
                    url=burl,
                    headers={'user-agent': 'my-app/1.0.0'}
                ) as r:
                    raw_json = r.json()
                    if not to_animagine_style:
                        if remove_meta_artist:
                            txt = raw_json["tag_string_character"]
                            if txt:
                                source += f"{txt} "
                            txt = raw_json["tag_string_copyright"]
                            if txt:
                                source += f"{txt} "
                            txt = raw_json["tag_string_general"]
                            if txt:
                                source += f"{txt} "
                        else:
                            source = raw_json["tag_string"]
                    else:
                        pattern = "[1-6]\\+?(girl|boy)s?"
                        repatter = re.compile(pattern)
                        rawtag_general = raw_json["tag_string_general"]
                        general_tags_list = rawtag_general.split(' ')
                        # girl/boyを先に追加
                        for i, tag in enumerate(general_tags_list):
                            is_match = repatter.match(tag)
                            if is_match:
                                source += f"{tag} "
                        # character
                        rawtag_character = raw_json["tag_string_character"]
                        if rawtag_character:
                            source += f"{rawtag_character} "
                        # copyright
                        rawtag_copyright = raw_json["tag_string_copyright"]
                    if rawtag_copyright:
                        source += f"{rawtag_copyright} "
                        # girl/boy以外のgeneralタグ
                        for i, tag in enumerate(general_tags_list):
                            is_match = repatter.match(tag)
                            if not is_match:
                                source += f"{tag} "
                        if not remove_meta_artist:
                            txt = raw_json["tag_string_artist"]
                            if txt:
                                source += f"{txt} "
                            txt = raw_json["tag_string_meta"]
                            if txt:
                                source += f"{txt} "
            except:
                print("Failed to fetch danbooru tags.")
                raise RuntimeError("Bad URL, missing post or request refused(cloudflare wall?)")
        else:
            source = booru_tags

        if not source:
            print("Warning: booru_tag is empty")
            return ("",)

        source = source.strip()


        if os.path.exists("custom_nodes/ComfyUI-Danbooru-To-WD/removal-list.txt") and remove_meta_artist and not booru_url:
            f = open("custom_nodes/ComfyUI-Danbooru-To-WD/removal-list.txt", 'r', encoding='UTF-8') 
            removal = f.read()
            f.close()
            removal = removal.replace('\r\n', '\n')
            tags = removal.split('\n')
            sourceTags = source.split(' ')
            for i, tag in enumerate(tags):
                for j, src in enumerate(sourceTags):
                    if(tag == src and tag) or ("user_" in src):
                        sourceTags[j] = ''

            for i, tag in enumerate(sourceTags):
                if i < (len(sourceTags) - 1) and tag:
                    sourceTags[i] += ", "

            dest = ''.join(sourceTags)
        else:
            dest = source.replace(' ', ", ")

    
        dest = dest.replace('_', ' ')
        # 制御文字のエスケープ(1111用だがComfyでも同じだとは思う)
        dest = dest.replace('\\', "\\\\")
        dest = dest.replace('(', "\(")
        dest = dest.replace(')', "\)")

        dest = dest.replace('<', "\<")
        dest = dest.replace('>', "\>")

        dest = dest.replace('|', "\|")

        dest = dest.replace('[', "\[")
        dest = dest.replace(']', "\]")
    

        return (dest,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "DanbooruToWD": DanbooruToWD
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "DanbooruToWD": "Danbooru to WD"
}
