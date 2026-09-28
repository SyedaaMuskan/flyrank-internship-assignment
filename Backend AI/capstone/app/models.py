from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="tenant")
    widgets = relationship("Widget", back_populates="tenant")
    submissions = relationship("Submission", back_populates="tenant")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    is_active = Column(Boolean, default=True)

    tenant = relationship("Tenant", back_populates="users")


class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship("Tenant", back_populates="widgets")
    submissions = relationship("Submission", back_populates="widget")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)

    widget_id = Column(
        Integer,
        ForeignKey("widgets.id"),
        nullable=False,
        index=True,
    )

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    data = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    widget = relationship("Widget", back_populates="submissions")
    tenant = relationship("Tenant", back_populates="submissions")