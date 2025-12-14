from datetime import datetime
from uuid import uuid4

from sqlalchemy import Foreignkey, String, Text, Column, Biginteger
from sqlalchemy.orm import relationship

from app.shared.models.base import Base
