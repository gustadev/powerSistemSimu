import string


class SimulatorState:
    def __init__(self):
        self.elementCount = dict()
        self.elements = dict()

    def addElement(self, class_name: string) -> tuple:
        if class_name not in self.elementCount:
            self.elementCount[class_name] = 0
        self.elementCount[class_name] += 1
        element = f"{class_name} {self.elementCount[class_name]}"

        if class_name not in self.elements:
            self.elements[class_name] = []
        self.elements[class_name].append(element)

        return (element, self.elementCount[class_name])
