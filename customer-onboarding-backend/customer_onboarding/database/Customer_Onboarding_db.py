'''Customer Onboarding app Database set up.'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from customer_onboarding.constants.default import (
    DATABASE,
    DB,
    USER,
    PASSWORD,
    HOST,
    DB_NAME,
)
from customer_onboarding.init.helpers import configs



db = SQLAlchemy()

def CustomerOnboarding_db():
    """Create connection engine and return session."""
    engine = create_engine(
        f"{configs[DATABASE][DB]}://{configs[DATABASE][USER]}:{configs[DATABASE][PASSWORD]}@{configs[DATABASE][HOST]}/{configs[DATABASE][DB_NAME]}"
    )
    session = sessionmaker(bind=engine)
    return session()