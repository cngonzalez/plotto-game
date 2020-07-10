import json
import random

NAMESTORE = [
            "Cason Jyothi",
            "Tamar Emilia",
            "Vencel Blanche",
            "Vesela Girish",
            "Wibawa Atefeh",
            "Huệ Laelius",
            "Ana Erland",
            "Okeke Beathan",
            "Estiñe Hlíf",
            "Bianca Facundo",
            "Vester Sundara",
            "Shripati Mikaela",
            "Diogenes Amaranta",
            "Leocadio Kleon"
        ]

ITEMSTORE = [
            "Mystic Scroll",
            "Vial of Exotic Perfume",
            "Vein of Aquamarine",
            "Tooled Leather-bound Book",
            "Bolt of Gold Cloth",
            "Marble Miniature of a Temple set with Blue Quartz",
            "Painting by a Legendary Master",
            "Rare Bird with Jeweled Feathers",
            "Fine Tapestry Trimmed in Ermine",
            "Extinct Creature Encased in Amber"
        ]

class PlottoGen():
    def __init__(self):
        with open("./story.json") as f:
            story_map = json.load(f)
            self.story = story_map["plotPoints"]
            characters = story_map["characters"]
            objects = story_map["objects"]

        item = random.choice(ITEMSTORE)
        for character in characters:
            new_name = self.generate_name()
            for step in self.story:
                step["text"] = step["text"].replace(f'_{character}_', new_name)
                step["text"] = step["text"].replace('_X_', item)

        self.step = 0
        self.achieved = set()
        self.feelings = []

    def generate_name(self):
        name_index = random.randrange(len(NAMESTORE))
        name = NAMESTORE[name_index]
        del NAMESTORE[name_index]
        return name

    def get_next_feelings(self):
        next_steps = self.find_valid_steps()
        next_feelings = [step[1]["feelings"] for step in next_steps]
        self.feelings = list(set([feeling for feeling_list in next_feelings for feeling in feeling_list]))
        return self.feelings

    def find_valid_steps(self, feeling=None):
        steps = []

        for idx, step in enumerate(self.story):
            if idx == self.step:
                continue
            #if my preconditions are a subset of what i've achieved or what i will achieve this step
            achieved = self.achieved.union(set(self.story[self.step]["achieves"]))
            remaining_preconditions = set(step["preconditions"]).difference(achieved)
            if len(remaining_preconditions) == 0:
                if not feeling:
                    steps.append((idx,step))
                elif feeling in step["feelings"]:
                    steps.append((idx, step))

        return steps


    def get_current_state(self):
        return self.story[self.step]["text"]


    def advance_with_feeling(self, feeling):
        self.achieved = self.achieved.union(set(self.story[self.step]["achieves"]))
        chosen_feeling = self.feelings[feeling]
        valid_steps = self.find_valid_steps(chosen_feeling)
        if len(valid_steps) > 1:
            self.step = random.choice(valid_steps)[0]
        else:
            self.step = valid_steps[0][0]

        self.achieved = self.achieved.difference(
            self.story[self.step]["removes"])

    def determine_terminal(self):
        return self.story[self.step]["achieves"][0] == "TERMINAL"


