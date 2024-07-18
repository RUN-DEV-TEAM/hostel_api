# from sqlalchemy import Column, Integer, String, DateTime, text, ForeignKey, Enum,UniqueConstraint
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from db.connection import Base
# from schemas.helperSchema import Deleted
# from models.userModel import RoomModel


# class StudentModel(Base):
#     __tablename__ = 't_occupants'
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     matric_number = Column(String(65), nullable=False)
#     room_id = Column(Integer, ForeignKey('t_rooms.id'), nullable=False)
#     acad_session = Column(String(9), nullable=False)
#     deleted = Column(Enum(Deleted), default=Deleted.N)
#     created_at = Column(DateTime, server_default= text('CURRENT_TIMESTAMP'))
#     updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
#     rooms = relationship('RoomModel', back_populates='occupants')


#     __table_args__ = (
#         UniqueConstraint('matric_number', 'acad_session', name='_matric_number_acad_session_uniq'),
#         UniqueConstraint('matric_number', 'room_id', name='_matric_number_room_id_uniq'),
#         )