import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from models import FinanceManager


class FinancialAnalytics:
    @staticmethod
    def get_income_vs_expense_graph():
        """აბრუნებს მიმდინარე თვის ჯამურ შემოსავალს და ხარჯს (Pie Chart-ისთვის)"""
        df=FinanceManager.get_all_transactions_as_df()
        if df.empty: return {"income": 0.0, "expense": 0.0}


        current_month=datetime.today().strftime("%Y-%m")
        df['date_month']=pd.to_datetime(df['date']).dt.strftime("%Y-%m")
        m_df=df[df["date_month"]==current_month]

        income=m_df[m_df['type']=='income']['amount'].sum()
        expense=m_df[m_df['type']=='expense']['amount'].sum()

        return {"income": round(income, 2), "expense": round(expense, 2)}
    

    @staticmethod
    def get_recent_transactions(limit=5):
        """აბრუნებს ბოლო 5 ტრანზაქციას მთავარ გვერდზე საჩვენებლად"""
        df= FinanceManager.get_all_transactions_as_df()
        if df.empty: return []
        df = df.sort_values(by='date', ascending=False)
        return df.head(limit).to_dict(orient='records')







    @staticmethod
    def get_financial_health_score():
        """ითვლის მომხმარებლის ფინანსური ჯანმრთელობის ქულას (0 - 100)"""
        df=FinanceManager.get_all_transactions_as_df()
        if df.empty: return 100

        score=100
        current_month=datetime.today().strftime("%Y-%m")
        df['date_month']=pd.to_datetime(df['date']).dt.strftime("%Y-%m")
        m_df=df[df["date_month"]==current_month]


        income=m_df[m_df['type']=='income']['amount'].sum()
        expense=m_df[m_df['type']=='expense']['amount'].sum()


        # ა) დაზოგვის მარჟა (25 ქულა)
        if income>0:
            savings_rate=((income-expense)/income)*100
            if savings_rate < 20: score -= 15
            if savings_rate < 0: score -= 10


        # ბ) ბიუჯეტების გადაცილება (მაქსიმუმ -30 ქულა)
        budgets= FinancialAnalytics.get_budget_status()
        overbudget_count=sum(1 for b in budgets if b['remaining'] < 0)
        score -= min(30, overbudget_count*10)

        # გ) ანომალიების რაოდენობა (მაქსიმუმ -20 ქულა)
        anomalies_count=len(FinancialAnalytics.detect_anomalies())
        score-= min(20,anomalies_count*5)

        return  max(0, min(score, 100))
    


    @staticmethod
    def detect_anomalies():
        """პოულობს უჩვეულოდ დიდ ხარჯებს კატეგორიების მიხედვით"""
        df=FinanceManager.get_all_transactions_as_df()
        expense_df=df[df['type']=='expense'].copy()

        if expense_df.empty or len(expense_df) < 5:
            return []
        

        anomalies=[]
        for category, cat_df in expense_df.groupby("category"):
            if len(cat_df)< 3: continue

            mean=cat_df['amount'].mean()
            std_dev= cat_df['amount'].std()
            if std_dev==0: std_dev=1


            for _, row in cat_df.iterrows():
                z_score = (row['amount']-mean)/std_dev
                if z_score > 2: # ეროვნული ნორმიდან მკვეთრი გადახრა
                    anomalies.append({
                        "title": row['title'],
                        "amount": row['amount'],
                        "category": category,
                        "date": row['date'],
                        "message": f"Detected anomaly expense: {row['amount']} GEL in '{category}' (Avarage is {round(mean, 2)} GEL"
                    })

        return anomalies
                

    @staticmethod
    def simulate_what_if(target_category, reduction_percentage):
        """სიმულაცია: რა მოხდება თუ ხარჯებს შევამცირებთ X პროცენტით"""
        df= FinanceManager.get_all_transactions_as_df()
        if df.empty: return "No data available"

        current_month=datetime.today().strftime("%Y-%m")
        df['date_month']=pd.to_datetime(df['date']).dt.strftime("%Y-%m")

        cat_expense = df[
            (df['date_month']==current_month) &
            (df['type']=='expense') &
            (df['category']== target_category)
        ]['amount'].sum()


        if cat_expense==0:
            return f"You haven't spent anything in '{target_category}' this month."
        

        monthly_savings=cat_expense*(reduction_percentage/100)
        yearly_savings=monthly_savings*12

        return {
            "summary_text": f"If you reduce '{target_category}' by {reduction_percentage}%, you will save {round(monthly_savings, 2)} GEL this month and {round(yearly_savings, 2)} GEL in a year!"
        }
    

    @staticmethod
    def check_early_spending_alert():
        """აფრთხილებს მომხმარებელს, თუ თვის დასაწყისშივე ბევრს ხარჯავს"""
        transactions_df=FinanceManager.get_all_transactions_as_df()
        budgets_df=FinanceManager.get_budget_asdf()

        if transactions_df.empty or budgets_df.empty: return None
        total_limit=budgets_df['amount_limit'].sum()
        if total_limit == 0: return None


        today=datetime.today()
        current_day= today.day
        current_month=today.strftime("%Y-%m")

        transactions_df['date_month'] = pd.to_datetime(transactions_df['date']).dt.strftime("%Y-%m")
        this_month_exp=transactions_df[
            (transactions_df['date_month']==current_month) & (transactions_df['type']=='expense')
        ]['amount'].sum()


        spent_percentage = (this_month_exp / total_limit) * 100

        if current_day <= 10 and spent_percentage >50:
            return f"⚠️ ALERT: You spent {round(spent_percentage, 1)}% of your budget in just {current_day} days!"
        elif 10<current_day<= 20 and spent_percentage> 80:
            return f"⚠️ WARNING: High spending pace! Used {round(spent_percentage,1)}% of budget by day {current_day}."
        return "Budget conditon is healthy. Keep it up!"
    

    
    @staticmethod
    def get_calender_daily_expenses():
        """დაჯამებული დღიური ხარჯები კალენდრისთვის"""
        df=FinanceManager.get_all_transactions_as_df()
        if df.empty: return {}
        current_month = datetime.today().strftime("%Y-%m")
        df['date_month'] = pd.to_datetime(df['date']).dt.strftime("%Y-%m")
        m_exp = df[(df['date_month'] == current_month) & (df['type'] == 'expense')]
        return m_exp.groupby('date')['amount'].sum().to_dict()
    

    @staticmethod
    def get_balance_trend():
        """ბალანსის ისტორიული დინამიკა ხაზოვანი გრაფიკისთვის"""
        df=FinanceManager.get_all_transactions_as_df()
        initial=FinanceManager.get_initial_networth()
        if df.empty: return []

        df['date'] = pd.to_datetime(df['date'])
        df=df.sort_values(by='date')
        df['adj'] = df.apply(lambda r: r['amount'] if r['type'] == 'income' else -r['amount'], axis=1)

        daily= df.groupby('date')['adj'].sum().reset_index()
        daily['balance'] = daily['adj'].cumsum() + initial
        daily['date_str'] = daily['date'].dt.strftime('%Y-%m-%d')
        return daily[['date_str', 'balance']].to_dict(orient='records')
    

    @staticmethod
    def predict_month_end_expense():
        """აწარმოებს თვის ბოლომდე სავარაუდო ხარჯის პროგნოზს საშუალო ტემპისა და რეგრესიის მიხედვით"""
        df=FinanceManager.get_all_transactions_as_df()
        if df.empty: return "No data available"

        current_month=datetime.today().strftime("%Y-%m")
        df['date']=pd.to_datetime(df['date'])
        df['date_month']=df["date"].dt.strftime('%Y-%m')


        #ვფილტრავთ მიმდინარე თვის ხარჯებს
        monthly_exp=df[(df['date_month']==current_month) & (df['type']=='expense')].copy()
        if monthly_exp.empty: return "No expenses this month"

        # დღეების ამოღება (მაგალითად: 1, 2, 3... ივნისი)
        monthly_exp['day']=monthly_exp['date'].dt.day
        daily_totals = monthly_exp.groupby('day')['amount'].sum().reset_index()

        # მათემატიკური მოდელი: X არის დღეები, Y არის ხარჯი
        x=daily_totals['day'].values.reshape(-1,1)
        y=daily_totals['amount'].values

        model=LinearRegression()
        model.fit(x,y)


        # ვიგებთ რამდენი დღეა ამ თვეში სულ
        today=datetime.today()
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1,day=1)
        else:
            next_month = today.replace(month=today.month+1, day=1)
        total_days_in_month =(next_month- today.replace(day=1)).days

        # პროგნოზი თვის ბოლო დღისთვის
        predicted_total=daily_totals['amount'].sum()
        current_day=today.day
        remaining_days=total_days_in_month - current_day

        if remaining_days>0:
            # ვიგებთ საშუალო დღიურ ხარჯს
            avg_daily_spent=daily_totals['amount'].sum()/current_day
            predicted_total=daily_totals['amount'].sum() + (avg_daily_spent*remaining_days)

        return f"Based on your current pace, you will spend approximately {round(predicted_total,2)} GEL by the end of the month"
 


    
    

    @staticmethod
    def get_budget_status():
        """აბრუნებს თითოეული კატეგორიის ლიმიტს, დანახარჯს, ნაშთს და პროცენტს"""
        transactions_df=FinanceManager.get_all_transactions_as_df()
        budgets_df=FinanceManager.get_budget_asdf()
        if budgets_df.empty:
            return []
        

        current_month=datetime.today().strftime("%Y-%m")
        if not transactions_df.empty:
            transactions_df['date_month']=pd.to_datetime(transactions_df['date']).dt.strftime("%Y-%m")

            #მხოლოდ მიმდინარე თვის ხარჯები
            monthly_expenses = transactions_df[
            (transactions_df['date_month']==current_month) & 
            (transactions_df['type']=='expense')]

            # დავაჯამოთ ხარჯები კატეგორიების მიხედვით
            expense_by_cat=monthly_expenses.groupby('category')['amount'].sum().to_dict()
        else:
            expense_by_cat = {}
            
        result=[]
        for _,row in budgets_df.iterrows():
            cat = row['category']
            limit =row['amount_limit']
            spent = expense_by_cat.get(cat, 0.0)
            remaining=limit - spent
            percentage=(spent/limit)*100 if limit > 0 else 0

            result.append({
                "category":cat,
                "limit":limit,
                "spent":round(spent,2),
                "remaining":round(remaining,2),
                "percentage":round(percentage,1)
                })
            
        return result

    
    

    

    @staticmethod
    def get_top_expenses():
        """პოულობს Top 10 ყველაზე დიდ ხარჯს და ყველაზე ძვირადღირებულ კატეგორიას"""
        df=FinanceManager.get_all_transactions_as_df()


        # ვფილტრავთ მხოლოდ ხარჯებს
        expenses_df=df[df['type']=='expense']
        if expenses_df.empty:
            return {"top_10":[], "most_expensive_category":"None", "max_cat_amount": 0.0}
        
        # ა) Top 10 კონკრეტული დანახარჯი
        top_10_df=expenses_df.sort_values(by='amount', ascending=False).head(10)
        top_10_list=top_10_df[['title','amount','category','date']].to_dict(orient='records')

        # ბ) ყველაზე ძვირადღირებული კატეგორია ჯამურად
        cat_totals=expenses_df.groupby('category')['amount'].sum()
        most_expensive_cat=cat_totals.idxmax()  # აბრუნებს კატეგორიის სახელს, სადაც მაქსიმუმია
        max_cat_amount=cat_totals.max()

        return {
            "top_10": top_10_list,
            "most_expensive_category":most_expensive_cat,
            "max_cat_amount": round(max_cat_amount,2)
        }
    

    @staticmethod
    def get_comparative_analysis():
        """ადარებს მიმდინარე თვის ხარჯებს წინა თვესთან (პროცენტულად)"""
        df=FinanceManager.get_all_transactions_as_df()
        df['date']=pd.to_datetime(df['date'])

        # მიმდინარე და წინა თვის თარიღების განსაზღვრა
        today = datetime.today()
        this_month_str = today.strftime("%Y-%m")
        
        first_of_this_month = today.replace(day=1)
        last_month_date = first_of_this_month - timedelta(days=1)
        last_month_str=last_month_date.strftime("%Y-%m")

        # ფილტრაცია ხარჯებზე
        df['month_str'] = df['date'].dt.strftime("%Y-%m")
        expenses = df[df['type'] == 'expense']

        this_month_total = expenses[expenses['month_str'] == this_month_str]['amount'].sum()
        last_month_total=expenses[expenses['month_str'] == last_month_str]['amount'].sum()

        # პროცენტული ცვლილების დათვლა
        if last_month_total == 0:
            percentage_change = 0.0 if this_month_total == 0 else 100.0
        else:
            percentage_change = ((this_month_total - last_month_total)/last_month_total)*100

        return {
            "this_month_total": round(this_month_total, 2),
            "last_month_total": round(last_month_total, 2),
            "percentage_change": round(percentage_change, 1)
        }



@staticmethod
def get_savings_analysis():
    """ითვლის დაზოგილი თანხის დინამიკას და დაზოგვის პროცენტს თვეების მიხედვით"""
    df = FinanceManager.get_all_transactions_as_df()
    if df.empty: return []


    df['month'] = pd.to_datetime(df['date']).dt.strftime("%Y-%m")
    # ვაჯამებთ შემოსავლებს და ხარჯებს ცალ-ცალკე თვეების მიხედვით
    monthly_data = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0.0)


    # თუ რომელიმე სვეტი (income ან expense) აკლია, შევქმნათ 0-ებით
    if 'income' not in monthly_data.columns: monthly_data['income'] = 0.0
    if 'expense' not in monthly_data.columns: monthly_data['expense'] = 0.0


    result = []
    for month, row in monthly_data.iterrows():
        inc = row['income']
        exp = row['expense']
        saved=inc-exp

        # დაზოგვის პროცენტი შემოსავალთან მიმართებაში
        savings_rate = (saved/inc) * 100 if inc > 0 else 0.0
        if saved < 0: savings_rate = 0.0


        result.append({
            "month": month,
            "income": round(inc, 2),
            "expense": round(exp, 2),
            "saved": round(saved, 2),
            "savings_rate_percentage": round(savings_rate,1)
        })

    return result
    