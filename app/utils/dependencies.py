from app.db.session import SessionLocal


# Dependency: Get SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
