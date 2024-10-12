from sqlalchemy import Column, Integer, String, DateTime, text, ForeignKey,Enum,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.connection import Base
from schemas.helperSchema import ( RoomCondition,RoomStatus,RoomType,Deleted,Gender,MedicalAttention,
                                  BlockStatus,UserStatus,UserType, Airy, WaterAccess,PortalsLodgeProxy)
from pydantic import ValidationError
# from models.studentModel import StudentModel


class UserModel(Base):
    __tablename__ = 't_users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(45),  unique=True, index=True,nullable=False)
    password = Column(String(191), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.INACTIVE)
    gender = Column(Enum(Gender), default=Gender.M)
    user_type = Column(Enum(UserType), default=UserType.PORTAL)
    deleted = Column(Enum(Deleted), default=Deleted.N)
    created_at = Column(DateTime, server_default= text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())



class BlockModel(Base):
    __tablename__ = 't_blocks'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    block_name = Column(String(45), nullable=False)
    description = Column(String(191), nullable=False)
    gender = Column(Enum(Gender))
    num_rooms_in_block = Column(Integer, nullable=False)
    num_of_allocated_rooms = Column(Integer, default=0)
    num_norm_rooms_in_block = Column(Integer, default=0)
    num_corn_rooms_in_block = Column(Integer, default=0)
    block_status = Column(Enum(BlockStatus), default=BlockStatus.AVAILABLE)
    airy = Column(Enum(Airy), default=Airy.NO)
    water_access = Column(Enum(WaterAccess), default=WaterAccess.NO)
    proxy_to_portals_lodge = Column(Enum(PortalsLodgeProxy), default=PortalsLodgeProxy.NO)
    deleted = Column(Enum(Deleted), default=Deleted.N)
    created_at = Column(DateTime, server_default= text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    rooms = relationship('RoomModel', back_populates='blocks')
    block_proximity = relationship('BlockProximityToFacultyModel', back_populates='_blocks')


    __table_args__ = (
        UniqueConstraint('block_name', 'gender', name='_block_name_gender_uniq'),
        )


class BlockProximityToFacultyModel(Base):
    __tablename__ = 't_block_proximity_to_faculty'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    faculty = Column(String(65), nullable=False)
    block_id = Column(Integer, ForeignKey('t_blocks.id'), nullable=False)
    _blocks = relationship('BlockModel', back_populates='block_proximity')


class RoomModel(Base):
    __tablename__ = 't_rooms'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_name = Column(String(45), nullable=False)
    capacity = Column(Integer, nullable=False)
    num_space_occupied = Column(Integer, default=0)
    room_type = Column(Enum(RoomType), default=RoomType.NORMAL)
    block_id = Column(Integer, ForeignKey('t_blocks.id'), nullable=False)
    room_status = Column(Enum(RoomStatus), default=RoomStatus.AVAILABLE)
    room_condition = Column(Enum(RoomCondition), default=RoomCondition.GOOD)
    deleted = Column(Enum(Deleted), default=Deleted.N)
    created_at = Column(DateTime, server_default= text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    blocks = relationship('BlockModel', back_populates='rooms')
    occupants = relationship('StudentModel', back_populates='rooms')

    __table_args__ = (
        UniqueConstraint('room_name', 'block_id', name='_room_name_block_id_uniq'),
        )


class StudentModel(Base):
    __tablename__ = 't_occupants'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    matric_number = Column(String(65), nullable=False)
    surname = Column(String(100), nullable=True)
    firstname = Column(String(100), nullable=True)
    othernames = Column(String(100), nullable=True)
    sex = Column(String(1), nullable=True)
    isFresher = Column(String(1), nullable=True)
    medical_attention = Column(Enum(MedicalAttention), default=MedicalAttention.NO)
    program = Column(String(100), nullable=True)
    program_code = Column(String(45), nullable=True)
    dpt = Column(String(191), nullable=True)
    college = Column(String(65), nullable=True)
    college_id = Column(Integer, nullable=True)
    level = Column(String(3), nullable=True)
    email = Column(String(100), nullable=True)
    email_alternate = Column(String(100), nullable=True)
    accountBalance = Column(String(65), nullable=True)
    accom_paid = Column(String(65), nullable=True)
    accom_payable = Column(String(65), nullable=True)
    special_accom_paid = Column(String(65), nullable=True)
    special_accom_payable = Column(String(65), nullable=True)
    exemption_id = Column(Integer, nullable=True)
    exemption_reason = Column(String(191), nullable=True)
    room_id = Column(Integer, ForeignKey('t_rooms.id'), nullable=False)
    curr_session = Column(String(9), nullable=False)
    deleted = Column(Enum(Deleted), default=Deleted.N)
    created_at = Column(DateTime, server_default= text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    rooms = relationship('RoomModel', back_populates='occupants')


    __table_args__ = (
        UniqueConstraint('matric_number', 'curr_session', name='_matric_number_acad_session_uniq'),
        UniqueConstraint('matric_number', 'room_id', name='_matric_number_room_id_uniq'),
        )

