from RPA.Robocorp.WorkItems import WorkItems


class WorkItemManager:
    def __init__(self):
        self.wi = WorkItems()

    def list_variables(self):
        self.wi.get_input_work_item()
        input = self.wi.get_work_item_variables()
        return input
