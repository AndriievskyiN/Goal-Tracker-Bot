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
        for line in message.split("\n"):
            if line.lower().startswith("ім'я") or line.lower().startswith("имя"):
                name = line.split("-")[1].strip()

            elif line.lower().startswith("вага"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                weight = float(line[:index])
            
            elif line.lower().startswith("плечі"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                shoulders = float(line[:index])

            elif line.lower().startswith("груди"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                chest = float(line[:index])

            elif line.split(".")[1].strip().lower().startswith("рука права"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                right_hand = float(line[:index])

            elif line.split(".")[1].strip().lower().startswith("рука ліва"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                left_hand = float(line[:index])

            elif line.split(".")[1].strip().lower().startswith("талія"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                waist = float(line[:index])

            elif line.split(".")[1].strip().lower().startswith("стегна"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                hips = float(line[:index])  

            elif line.split(".")[1].strip().lower().startswith("стегна праве"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                right_hip = float(line[:index])

            elif line.split(".")[1].strip().lower().startswith("стегна ліве"):
                line = line.split("-")[1].strip()
                index = line.find("(")
                left_hip = float(line[:index])

        return name, weight, shoulders, chest, right_hand, left_hand, waist, hips, right_hip, left_hip

    # def get_data(self):
    #     return "---name---", self.__completed_goals, self.__rewards, self.__uncompleted_goals, self.__total_goals


    # def print_info(self):
    #     print(f"Name: {self.__full_name}")
    #     print(f"Total goals: {self.__total_goals}")
    #     print(f"Completed goals: {self.__completed_goals}")
    #     print(f"Rewards: {self.__rewards}")
    #     print(f"Uncompleted goals: {self.__uncompleted_goals}")

# with open("test_message.txt", "r") as f:
#     lines = f.read()

# scraper = Scraper()
# data = scraper.scrape_report(lines)
# # scraper.print_info()