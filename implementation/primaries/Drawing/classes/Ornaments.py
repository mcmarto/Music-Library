from implementation.primaries.Drawing.classes import BaseClass

# TODO: probably needs refactoring to 1 ornament class?
class InvertedMordent(BaseClass.Base):
    def toLily(self):
        return "\prall"

class Mordent(BaseClass.Base):

    def toLily(self):
        return "\mordent"

class Trill(BaseClass.Base):
    def toLily(self):
        return "\\trill"

class Turn(BaseClass.Base):
    def toLily(self):
        return "\\turn"

class InvertedTurn(BaseClass.Base):
    def toLily(self):
        return "\\reverseturn"

class Tremolo(BaseClass.Base):
    def __init__(self, **kwargs):
        self.preNote = True
        BaseClass.Base.__init__(self)
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]

        if "value" in kwargs:
            if kwargs["value"] is not None:
                self.value = kwargs["value"]
        else:
            self.value = 2

    def toLily(self):
        return_val = "\\repeat tremolo "
        num = ""
        if hasattr(self, "value"):
            options = {1:2,2:4,3:8}
            num = str(options[self.value])

        if num != "":
            return_val += num + " "
        if hasattr(self, "type"):
            if self.type == "start":
                return_val += "{"
            if self.type == "stop":
                return_val = "}"

        return return_val

