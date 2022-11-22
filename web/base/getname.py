import re

class getname:
    def getLabel(shop , link):
        label = None
        mask = f"""{shop}([^/]+)"""
        m = re.match(mask , link )
        if m:
            label = m.group(1).strip()
        text = label.split("-")
        return text
