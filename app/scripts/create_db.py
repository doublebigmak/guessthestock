from app.database import Base, engine
from app import models


def create_db():
    print("Creating SQLite database and tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done!")

if __name__ == "__main__":
    create_db()