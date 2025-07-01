# seed_stocks.py

import csv
from app.database import SessionLocal
from app.models import Stock
from sqlalchemy.exc import IntegrityError

CSV_FILE = "constituents.csv"  # path to your CSV file

def seed_stocks():
    db = SessionLocal()
    with open(CSV_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        added, skipped = 0, 0

        for row in reader:
            ticker = row['Symbol'].strip().upper()
            existing = db.query(Stock).filter_by(ticker=ticker).first()
            if existing:
                skipped += 1
                continue

            stock = Stock(
                ticker=ticker,
                name=row['Security'],
                sector=row['GICS Sector'],
                industry=row['GICS Sub-Industry']
            )
            db.add(stock)
            try:
                db.commit()
                added += 1
            except IntegrityError:
                db.rollback()
                skipped += 1

    db.close()
    print(f"Added {added} stocks. Skipped {skipped} (duplicates).")

if __name__ == "__main__":
    seed_stocks()