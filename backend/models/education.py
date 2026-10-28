from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="educations")
    degree = Column(String(100), nullable=False)
    field_of_study = Column(String(150), nullable=False)
    institution = Column(String(200), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)