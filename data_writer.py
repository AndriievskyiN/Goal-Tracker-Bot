import openpyxl as xl
import psycopg2
from datetime import datetime
from scraper import Scraper
from typing import Dict, Union, List, Any

class DataWriter:
    def __init__(self):
        self.__index_to_month = {
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


        hostname = "localhost"
        database = "coach-bot"
        username = "andriievskyi"
        pwd = "Kakady33dyno"
        port_id = 5432

        self.__conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )

        self.__cur = self.__conn.cursor()

        self.__cur.execute(
            """
            DROP TABLE goals
            """
        )

        self.__cur.execute(
            """
            DROP TABLE measurements
            """
        )

        self.__conn.commit()



        create_goals_table = """
            CREATE TABLE IF NOT EXISTS goals (
                id SERIAL PRIMARY KEY,
                year SMALLINT,
                month SMALLINT,
                week_num SMALLINT,
                name VARCHAR(100) NOT NULL,
                completed_goals SMALLINT,
                rewards SMALLINT, 
                uncompleted_goals SMALLINT,
                total_goals SMALLINT,
                UNIQUE (year, month, week_num, name)
            )    
        """

        create_measurements_table = """
            CREATE TABLE IF NOT EXISTS measurements (
                id SERIAL PRIMARY KEY,
                year SMALLINT,
                month SMALLINT,
                week_num SMALLINT,
                name VARCHAR(100) NOT NULL,
                weight REAL,
                shoulders REAL,
                chest REAL,
                right_arm REAL, 
                left_arm REAL,
                waist REAL,
                hips REAL, 
                right_hip REAL,
                left_hip REAL
            )
        """

        self.__cur.execute(create_goals_table)
        self.__cur.execute(create_measurements_table)
        self.__conn.commit()

        self.__current_year = datetime.now().year
        self.__current_month = self.__index_to_month[datetime.now().month]

        self.__meas_workbook = xl.Workbook()
        self.__meas_worksheet = self.__meas_workbook.active
        self.__meas_worksheet.title = f"{self.__current_month} {self.__current_year}"
        self.__meas_worksheet.append(["Ім'я", "Вага", "Плечі",  "Груди", "Рука права", "Рука ліва", "Талія", "Стегна", "Стегна праве", "Стегна ліве"])
        

    def write_goals_xl(self, data):
        self.__goal_worksheet.append(data)
        self.__goal_workbook.save("Report.xlsx")


    def write_measurements_xl(self, data: Dict[str, Union[str, float]]):
        last_row = len(self.__meas_worksheet["A"])
        for k, v in data.items():
            for col in range(1, 11):
                if self.__meas_worksheet.cell(row=1, column=col).value == k:
                    self.__meas_worksheet.cell(row=last_row+1, column=col).value = v
                    
        self.__meas_workbook.save("Measurements.xlsx")


    
    def write_goal_data_db(self, data: List[Union[str, int]]) -> str:
        today = datetime.today().date()
        year = int(today.strftime("%Y"))
        month = int(today.strftime("%m"))
        week_num = int(week_number_of_month(today))

        self.__cur.execute(
        """
        INSERT INTO goals (year, month, week_num, name, completed_goals, rewards, uncompleted_goals, total_goals)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        
        ON CONFLICT (year, month, week_num, name)
            DO UPDATE
                SET 
                    completed_goals = excluded.completed_goals, 
                    rewards = excluded.rewards,
                    uncompleted_goals = excluded.uncompleted_goals,
                    total_goals = excluded.total_goals

        RETURNING 1
        """, 
        ((year, month, week_num) + tuple(data)))

        self.__conn.commit()
        
    
    # def TEST_write_measurement_data(self, data):
    #     # WILL NOT WORK (DATA IS SUPPOSED TO BE A DICTIONARY, BUT IN THIS FUNCTION IT IS TREATED AS A LIST)
    #     query = """
    #         INSERT INTO measurements (date, name, weight, shoulders, chest, right_arm, left_arm, waist, hips, right_hip, left_hip)
    #             VALUES (
    #                 %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    #             )
    #     """

    #     insert_values = tuple(data)
        
    #     self.__cur.execute(query, insert_values)
    #     self.__conn.commit()


    def get_goals_xl(self, mode: str, sort_by: str):
        sort_by_options = ["completed", "rewards", "uncompleted", "total"]

        if mode == "week":
            today = datetime.today().date()
            month = int(datetime.now().strftime("%m"))
            week_num = week_number_of_month(today)

            query = """
                SELECT 
                    name, completed_goals, rewards, uncompleted_goals, total_goals
                FROM
                    goals
                WHERE month = %s and week_num = %s
            """

            insert_values = (month, week_num)

            self.__cur.execute(query, insert_values)
            data = self.__cur.fetchall()

            # Get index to sort by
            sort_by_index = sort_by_options.index(sort_by) + 1 # because we exclude name 

            if sort_by == "uncompleted":
                data = sorted(data, key=lambda x: x[sort_by_index]) # sort in ascending order
            
            else:
                data = sorted(data, key=lambda x: -x[sort_by_index]) # sort in descending order

            # Create an excel sheet
            today = datetime.today().date()

            goal_workbook = xl.Workbook()
            goal_worksheet = goal_workbook.active
            goal_worksheet.title = str(today)
            goal_worksheet.append(["Ім'я", "Виконані цілі", "Заохочення",  "Не виконані цілі", "Всього цілей"])

            # Add data to the excel sheet
            for i in data:
                goal_worksheet.append(list(i))
                goal_workbook.save("Report.xlsx")
    
        elif mode == "month":
            query = """
                SELECT  
                    year, month, week_num, name, completed_goals, rewards, uncompleted_goals, total_goals
                FROM 
                    goals
                WHERE
                    month = %s
            """

            print("month")


        elif mode == "year":
            print("year")


def week_number_of_month(date_value):
     return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)