from app.db.database import Base, engine

def init_db():
    print("databse is initialised")
    Base.metadata.create_all(bind=engine)