import re

def get_value(line):
    line = re.sub("[,]", ".", line.split("-")[1].strip())
    index = line.find("(")
    value = float(line[:index]) if index != -1 else float(line)
    
    return value

class Scraper:
    @staticmethod
    def scrape_goals(message: str):
        for line in message.split("\n"):
            if line.lower().startswith("ім'я") or line.lower().startswith("имя"):
                name = line.split("-")[1].strip()

            elif line.lower().startswith("виконані цілі"):
                completed_goals = int(line.split("-")[1].strip())
            
            elif line.lower().startswith("заохочення"):
                rewards = int(line.split("-")[1].strip())

            elif line.lower().startswith("не виконані цілі"):
                uncompleted_goals = int(line.split("-")[1].strip())

            # elif line.split(".")[1].strip().lower().startswith("вага"):
            #     weight = float(line.split("-")[1].strip())

        total_goals = completed_goals + uncompleted_goals

        return name, completed_goals, rewards, uncompleted_goals, total_goals

    @staticmethod
    def scrape_measurements(message: str):
        keys = ["вага", "плечі", "груди", "рука права", "рука ліва", "рука ліва", "талія", "стегна", "стегна праве", "стегна ліве"]
        data = {}

        for line in message.split("\n"):
            if line.lower().startswith("ім'я"):
                name = line.split("-")[1].strip()
                data["Ім'я"] = name

            elif re.match("^\d*[.]", line):
                line = ".".join(re.sub("[–]", "-", line).split(".")[1:]).strip().lower() # replace the weird-long dash symbol with a regular one and apply some preprocessing

                for i in keys:
                    if i == "стегна":
                        if line.startswith("стегна") and not (line.startswith("стегна праве") or line.startswith("стегна ліве")):
                            data["Стегна"] = get_value(line)
                    else:
                        if line.startswith(i):
                            data[i.capitalize()] = get_value(line)

        return data



    # def get_data(self):
    #     return "---name---", self.__completed_goals, self.__rewards, self.__uncompleted_goals, self.__total_goals


    # def print_info(self):
    #     print(f"Name: {self.__full_name}")
    #     print(f"Total goals: {self.__total_goals}")
    #     print(f"Completed goals: {self.__completed_goals}")
    #     print(f"Rewards: {self.__rewards}")
    #     print(f"Uncompleted goals: {self.__uncompleted_goals}")

# with open("test_message3.txt", "r") as f:
#     lines = f.read()

# scraper = Scraper()
# data = scraper.scrape_measurements(lines)
# print(data)
# # scraper.print_info()