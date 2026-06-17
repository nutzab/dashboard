import datetime
import pandas as pd
from datetime import date 
from database import connection

class UserManager:

    @staticmethod
    def register_user(username,password):
        try:
            conn=connection()
            cursor=conn.cursor()
            cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"რეგისტრაციის შეცდომა: {e}")
            return False
        



    @staticmethod
    def verify_user(username,password):
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username =? AND password=?",(username,password))
        user_row=cursor.fetchone()
        conn.close()
        return True if user_row else False
    


class FinanceManager:

    @staticmethod
    def add_transaction(title,amount,date=None,tx_type="expense",currency='GEL'):
        if not date:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
       
        final_category="other"
        final_title=title
        title_lower=title.lower()



        lookup_table={"groceries":["nikora","carrefour","spar","agrohub","ორი ნაბიჯი","goodwill"],
                      "transport":["bolt","yandex","socar","wissol","gulf"],
                      "entertainment":["wolt","glovo","mcdonalds","cinema","pub","restaurant"],
                      "health":["aversi","psp","pharmadepot","კლინიკა","hospital"],
                      "taxes":["rs.ge","ჯარიმა","საშემოსავლო","კომუნალური","სახელმწიფო"]
                      }
     

        for category,keywords in lookup_table.items():
            for kw in keywords:
                if kw in title_lower:
                    final_category=category
                    final_title=kw.upper()
                    break
            if final_category!="other":
                break


        conn=connection()
        cursor=conn.cursor()

        query="""INSERT INTO transactions(title,amount,category,date,type,currency)
        VALUES (?,?,?,?,?,?)"""


        values=(final_title,amount,final_category,date,tx_type,currency)

        cursor.execute(query,values)
        conn.commit()
        conn.close()



    @staticmethod
    def get_all_transactions_as_df():
        conn=connection()

        query_="SELECT * FROM transactions"
        #pandas მონაცემების ჩასატვირთად
        df=pd.read_sql_query(query_, conn)

        conn.close()

        return df



    @staticmethod
    def set_budget(category,amount_limit):
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO budgets(category,amount_limit) VALUES (?,?)", (category, amount_limit))
        conn.commit()
        conn.close()


    @staticmethod
    def get_budget_asdf():
        conn=connection()
        query="Select * FROM budgets"
        df=pd.read_sql_query(query,conn)
        conn.close()
        return df

    @staticmethod
    def set_starting_networth(amount):
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings(key,value) VALUES ('initial_net_worth',?)", (str(amount),))
        conn.commit()
        conn.close()


    @staticmethod
    def get_initial_networth():
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = 'initial_net_worth'")
        row=cursor.fetchone()
        conn.close()
        return float(row['value']) if row else 0.0

    @staticmethod
    def dashboard():
        df=FinanceManager.get_all_transactions_as_df()
        #იძახებს ჩემს ფუნქციას,რომელიც ბაზიდან იღებს ყველა ტრანზაქციას და სვამს პანდას ცხრილში

        initial_net_worth=FinanceManager.get_initial_networth()

        if df.empty:
            return {"net_worth":initial_net_worth,"income":0.0,"expenses":0.0,"savings":0.0}
        #ამოწმებს არის თუ არა რაიმე ბაზაში(როცა მომხმარებელი პირველად იწერს აპს),
        #თუ ცარიელია, დააბრუნებს ნულებს
        
        #montly income and spendings
        current_month = datetime.date.today().strftime("%Y-%m")
        #დღევანდელი ზუსტი დრო(strftime-ით ტოვებს მხოლოდ წელს და თვეს ტექსტის სახით)
        df["date_month"]=pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
        monthly_df=df[df["date_month"]==current_month]

        income = monthly_df[monthly_df['type']=='income']['amount'].sum()
        expenses = monthly_df[monthly_df['type']=='expense']['amount'].sum()

        #savings=income-expenses
        savings=income-expenses

        #net worth
        total_income =df[df['type']=='income']['amount'].sum()
        total_expenses=df[df['type']=='expense']['amount'].sum()
        

        current_net_worth=initial_net_worth + (total_income-total_expenses)

        return {"net_worth": round(current_net_worth,2),
                "income": round(income,2),
                "expenses": round(expenses,2),
                "savings":round(savings,2)}