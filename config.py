from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DBSettings():
    @staticmethod
    def get_session():
        engine = create_engine(
            "postgresql+psycopg2://master:cockMaster@localhost:5432/master-cockMaster"
        )
        return Session(bind=engine)
