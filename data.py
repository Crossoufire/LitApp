import os.path
import sqlite3
import pandas as pd


class USData:
    DATABASE_URL = os.path.join(os.path.dirname(__file__), "datasets/us_retail.db")

    def __init__(self):
        self.connection = sqlite3.connect(self.DATABASE_URL)
        self.cursor = self.connection.cursor()

    def get_all_available_retails(self) -> pd.DataFrame:
        return pd.read_sql("SELECT DISTINCT kind_of_business FROM retail_sales ORDER BY 1", self.connection)

    def get_retails_data_per_month(self, retail: str, rolling_window: int) -> pd.DataFrame:
        roll = rolling_window - 1 if rolling_window > 0 else rolling_window

        sql_raw = """
        SELECT *
        FROM (
            SELECT 
                sales_month AS 'Months-Year',
                CAST(sales AS REAL) AS 'Sales Per Month',
                ROUND(AVG(sales) OVER (ORDER BY sales_month ROWS BETWEEN ? PRECEDING AND CURRENT ROW), 2) 
                AS 'Moving Average',
                COUNT(sales) OVER (ORDER BY sales_month ROWS BETWEEN ? PRECEDING AND CURRENT ROW) AS records_count
            FROM retail_sales
            WHERE kind_of_business = ?
        ) AS subQ
        WHERE records_count > 0 AND records_count = ? + 1
        """

        return pd.read_sql(sql_raw, self.connection, params=(roll, roll, retail, roll))

    def get_retails_index_evolution(self, retail: str) -> pd.DataFrame:
        sql_raw = """
        SELECT 
            sales_year AS 'Year', 
            total_business_sales,
            first_value(total_business_sales) OVER (ORDER BY sales_year) AS 'Index',
            round((CAST(total_business_sales AS REAL) / first_value(total_business_sales) OVER 
            (ORDER BY sales_year) - 1) * 100, 3) AS 'Evolution (%)'
        FROM (
            SELECT 
                strftime('%Y', sales_month) as sales_year,
                sum(CASE WHEN kind_of_business = ? THEN sales ELSE 0 END) AS total_business_sales
            FROM retail_sales
            WHERE kind_of_business = ?
            GROUP BY 1
            HAVING sum(CASE WHEN kind_of_business = ? THEN sales ELSE 0 END) > 0
        ) AS a;
        """

        return pd.read_sql(sql_raw, self.connection, params=(retail, retail, retail))

    def get_retails_growth(self, retail: str) -> pd.DataFrame:
        sql_raw = """
        SELECT 
            strftime('%Y', sales_month) AS 'Year', 
            SUM(sales) AS 'Total Sales',
            (CAST(SUM(sales) AS REAL) / lag(SUM(sales)) OVER (PARTITION BY kind_of_business ORDER BY 
            strftime('%Y', sales_month)) - 1) * 100 as 'Previous Year Growth (%)'
        FROM retail_sales
        WHERE kind_of_business = ?
        GROUP BY 1;
        """

        return pd.read_sql(sql_raw, self.connection, params=(retail,))
