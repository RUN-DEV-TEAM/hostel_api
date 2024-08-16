from enum import Enum






class PortalsLodgeProxy(Enum):
    YES = 'YES'
    NO = 'NO'


class Airy(Enum):
    YES = 'YES'
    NO = 'NO'

class WaterAccess(Enum):
    YES = 'YES'
    NO = 'NO'

class BlockStatus(Enum):
    OCCUPIED = 'OCCUPIED'
    AVAILABLE = 'AVAILABLE'


class RoomType(Enum):
    NORMAL = "NORMAL"
    CORNER = "CORNER"

class UserStatus(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

    
class UserType(Enum):
    ADMIN = 'ADMIN'
    PORTAL = 'PORTAL'

# room_status
class RoomStatus(Enum):
    OCCUPIED = "OCCUPIED"
    AVAILABLE = "AVAILABLE"


# room_condition	set('GOOD', 'BAD')
class RoomCondition(Enum):
    GOOD = "GOOD"
    BAD = "BAD"

class Deleted(Enum):
    N = "N"
    Y = "Y"

class Gender(Enum):
    F = "F"
    M = "M"
