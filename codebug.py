import codebug_tether


class CodeBug():
    code_bug = None

    def __init__(self):
        self.code_bug = codebug_tether.CodeBug()

    def set_pixel(self, row, col, state):
        self.code_bug.set_pixel(col, row, state)

    def clear_screen(self):
        self.code_bug.clear()

    def set_col(self, col_index, col_data):
        self.code_bug.set_col(col_index, col_data)

    def set_screen(self, datas):
        for col_index, data in enumerate(datas):
            self.set_col(col_index, data)
