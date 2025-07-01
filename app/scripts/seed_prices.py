# seed_prices.py

import yfinance as yf
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Stock, Price
from sqlalchemy.exc import IntegrityError

def fetch_and_store_prices(session: Session, start="2000-01-01", end=None):
    if not end:
        end = datetime.today().strftime('%Y-%m-%d')

    stocks = session.query(Stock).all()
    print(f"Found {len(stocks)} stocks.")

    for stock in stocks:
        print(f"Fetching {stock.ticker}...", end=" ")
        try:
            df = pd.DataFrame()
            df = yf.download(stock.ticker, start=start, end=end, progress=False)
            if df.empty:
                print("No data.")
                continue

            prices = []
            for date, row in df.iterrows():
                prices.append(Price(
                    stock_id=stock.id,
                    date=date.date(),
                    close=row["Close"]
                ))

            session.bulk_save_objects(prices)
            session.commit()
            print(f"{len(prices)} records inserted.")
        except IntegrityError:
            session.rollback()
            print("Skipped (duplicates found).")
        except Exception as e:
            session.rollback()
            print(f"Failed: {e}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        fetch_and_store_prices(db)
    finally:
        db.close()