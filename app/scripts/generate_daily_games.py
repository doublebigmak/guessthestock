
import random
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Game, Price, Stock
from sqlalchemy import func

NUM_GAMES = 3
MIN_DAYS = 90    # ~3 months
MAX_DAYS = 180   # ~6 months

def ensure_prices(session: Session, stock: Stock) -> bool:
    """Download full history if this ticker has no prices yet."""
    has = session.query(Price.id).filter(Price.stock_id == stock.id).first()
    if has:
        return True
    df = yf.download(stock.ticker, start="2000-01-01", progress=False)
    if df.empty:
        return False
    rows = [
        Price(stock_id=stock.id, date=idx.date(), close=float(row["Close"]))
        for idx, row in df.iterrows()
        if ("Close" in row and (row["Close"].values == row["Close"].values))  # not NaN
    ]
    session.bulk_save_objects(rows)
    session.commit()
    return True

def ensure_prices_up_to_date(session, stock):
    """
    Make sure we have prices up to the most recent market day.
    - If no prices: download full history since 2000-01-01.
    - If we have prices: download from (last_date+1) to today (idempotent with unique constraint).
    Returns True if we have any prices after refresh, else False.
    """
    # Latest stored date for this stock
    last = session.query(func.max(Price.date)).filter(Price.stock_id == stock.id).scalar()

    if last is None:
        # No data yet → full download
        df = yf.download(stock.ticker, start="2000-01-01", progress=False)
    else:
        # Incremental update: from next calendar day after last stored date
        start = last + timedelta(days=1)
        # If already up to date (start > today), nothing to fetch
        if start > date.today():
            return True
        df = yf.download(stock.ticker, start=start.isoformat(), progress=False)

    if df is None or df.empty:
        # Could be a delisted or no‑data ticker
        return last is not None  # we still have something if we had old data

    new_rows = []
    for idx, row in df.iterrows():
        close = float(row.get("Close", float("nan")))
        if close == close:  # not NaN
            new_rows.append(Price(
                stock_id=stock.id,
                date=idx.date(),
                close=close
            ))

    if new_rows:
        session.bulk_save_objects(new_rows)
        session.commit()

    # Confirm we have at least one price
    any_price = session.query(Price.id).filter(Price.stock_id == stock.id).first()
    return any_price is not None

def get_date_range(session: Session, stock_id: int):
    result = (
        session.query(Price.date)
        .filter(Price.stock_id == stock_id)
        .order_by(Price.date)
        .all()
    )
    dates = [r[0] for r in result]
    return dates

def download_prices_for_stock(session: Session, stock: Stock):
    print(f"Fetching data for {stock.ticker}...")
    df = yf.download(stock.ticker, start="2000-01-01", progress=False, auto_adjust=False)
    if df.empty:
        print("No data found.")
        return False

    prices = []
    for dt, row in df.iterrows():
        prices.append(Price(
            stock_id=stock.id,
            date=dt.date(),
            close=row["Close"]
        ))

    session.bulk_save_objects(prices)
    session.commit()
    print(f"{len(prices)} prices inserted for {stock.ticker}.")
    return True


def pick_random_window(dates):
    if len(dates) < MAX_DAYS:
        return None

    max_start_idx = len(dates) - MAX_DAYS
    start_idx = random.randint(0, max_start_idx)
    end_idx = start_idx + random.randint(MIN_DAYS, MAX_DAYS)

    return dates[start_idx], dates[min(end_idx, len(dates)-1)]

def pick_latest_window(dates,target_len=120):
    if not dates:
        return None
    # last index is most recent trading day
    end_idx = len(dates) - 1

    
    start_idx = max(0, end_idx - target_len)

    return dates[start_idx], dates[end_idx]

def upsert_game(session: Session, *, stock_id: int, start_date, end_date, mode: str, game_day: date):
    # delete existing game for today+mode to ensure only one
    session.query(Game).filter(Game.game_day == game_day, Game.mode == mode).delete()
    session.commit()

    g = Game(
        stock_id=stock_id,
        start_date=start_date,
        end_date=end_date,
        game_day=game_day,
        game_index=0 if mode == "hard" else 1,
        mode=mode,
    )
    session.add(g)
    session.commit()
    return g


def generate_games():
    session = SessionLocal()
    today = date.today()

    stocks = session.query(Stock).order_by(func.random()).all()

    if not stocks:
        print("No stocks in DB.")
        session.close()
        return
    
    # hard game
    hard_game_done = False
    for stock in stocks:
        if not ensure_prices(session, stock):
            continue
        dates = get_date_range(session, stock.id) # type: ignore
        window = pick_random_window(dates)
        if not window:
            continue
        start_date, end_date = window
        upsert_game(session, stock_id=stock.id, start_date=start_date, end_date=end_date, mode="hard", game_day=today) # type: ignore
        print(f"HARD: {stock.ticker} {start_date} -> {end_date}")
        hard_game_done = True
        break

    #EASY: latest 4–6 months ending at the most recent trading date
    easy_game_done = False
    # reshuffle for variety (or reuse same order)
    stocks2 = session.query(Stock).order_by(func.random()).all()
    for stock in stocks2:
        if not ensure_prices_up_to_date(session, stock):
            continue

        dates = get_date_range(session, stock.id)
        window = pick_latest_window(dates, target_len=120)  # or random in [MIN_DAYS, MAX_DAYS]
        if not window:
            continue

        start_date, end_date = window
        upsert_game(session,
                    stock_id=stock.id,
                    start_date=start_date,
                    end_date=end_date,
                    mode="easy",
                    game_day=today)
        print(f"EASY (fresh): {stock.ticker} {start_date} → {end_date}")
        easy_game_done = True
        break


    if not hard_game_done:
        print("⚠️ Failed to create HARD game (not enough data?)")
    if not easy_game_done:
        print("⚠️ Failed to create EASY game (not enough data?)")
    session.close()

if __name__ == "__main__":
    generate_games()