from database import Base, engine
from models import User, SavedSequence, DecodingHistory

Base.metadata.create_all(bind=engine)