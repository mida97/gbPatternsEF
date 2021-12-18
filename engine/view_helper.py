
class Tab:
    def __init__(self, id, href, name):
        self.id = id
        self.href = href
        self.name = name


class TabSet:

    @classmethod
    def __init__(self, tabs_desc):
        self.tabs = []
        for item in tabs_desc:
            self.tabs.append(Tab(id=item[0], href=item[1], name=item[2]))

    @classmethod
    def get_tabs(self):
        return self.tabs

    @classmethod
    def get_tab(self, id):

        for tab in self.tabs:
            if tab.id == str(id):
                return tab
        raise Exception(f'Нет вкладки с id = {id}')