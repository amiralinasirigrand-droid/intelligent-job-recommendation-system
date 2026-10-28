from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey

from database import Base


class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    job_title = Column(String(150), nullable=False)

    company = Column(String(150), nullable=False)

    description = Column(Text)

    start_date = Column(Date, nullable=False)

    end_date = Column(Date, nullable=True)