class Scraper:
    @staticmethod
    def scrape_report(message: str):
        for line in message.split("\n"):
            if line.lower().startswith("ім'я") or line.lower().startswith("имя"):
                name = line.split("-")[1].strip()

            elif line.lower().startswith("виконані цілі"):
                completed_goals = int(line.split("-")[1].strip())
            
            elif line.lower().startswith("заохочення"):
                rewards = int(line.split("-")[1].strip())

            elif line.lower().startswith("не виконані цілі"):
                uncompleted_goals = int(line.split("-")[1].strip())

        total_goals = completed_goals + uncompleted_goals

        return name, completed_goals, rewards, uncompleted_goals, total_goals

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