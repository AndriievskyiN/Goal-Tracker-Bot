import openpyxl as xl
from datetime import datetime
from scraper import Scraper

class FileWriter:
    def __init__(self):
        self.__index_to_str = {
            1: "Січень",
            2: "Лютий",
            3: "Березень",
            4: "Квітень",
            5: "Травень",
            6: "Червень",
            7: "Липень",
            8: "Серпень",
            9: "Вересень",
            10: "Жовтень",
            11: "Листопад",
            12: "Грудень"
        }

        self.__current_year = datetime.now().year
        self.__current_month = self.__index_to_str[datetime.now().month]
        self.__workbook = xl.Workbook()
        self.__worksheet = self.__workbook.active

        self.__worksheet.title = f"{self.__current_month} {self.__current_year}"
        self.__worksheet.append(["Ім'я", "Виконані цілі", "Заохочення",  "Не виконані цілі", "Всього цілей"])

    def write_data(self, data):
        self.__worksheet.append(data)
        self.__workbook.save("Report.xlsx")
