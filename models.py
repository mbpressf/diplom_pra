from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    account_type = Column(String, nullable=False, default="individual")  # individual | organization
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    vault = relationship("SavingsVault", back_populates="user", cascade="all, delete-orphan", uselist=False)
    organization_memberships = relationship("OrganizationMember", back_populates="user", cascade="all, delete-orphan")
    organization_consents = relationship("UserOrgConsent", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, default="#10B981")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income | expense
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, default="")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="transactions")
    user = relationship("User", back_populates="transactions")


class SavingsVault(Base):
    __tablename__ = "savings_vaults"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, default="Финансовый сейф")
    balance = Column(Float, nullable=False, default=0)
    target_amount = Column(Float, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="vault")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=False, default="")
    invite_code = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    members = relationship("OrganizationMember", back_populates="organization", cascade="all, delete-orphan")
    consents = relationship("UserOrgConsent", back_populates="organization", cascade="all, delete-orphan")
    report_runs = relationship("OrgReportRun", back_populates="organization", cascade="all, delete-orphan")


class OrganizationMember(Base):
    __tablename__ = "organization_members"
    __table_args__ = (UniqueConstraint("organization_id", "user_id", name="uq_org_member"),)

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String, nullable=False, default="viewer")  # owner | manager | viewer
    status = Column(String, nullable=False, default="active")  # active | invited | disabled
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="organization_memberships")


class UserOrgConsent(Base):
    __tablename__ = "user_org_consents"
    __table_args__ = (UniqueConstraint("organization_id", "user_id", name="uq_org_consent"),)

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    consent_given_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, nullable=False, default=True)

    organization = relationship("Organization", back_populates="consents")
    user = relationship("User", back_populates="organization_consents")


class OrgReportRun(Base):
    __tablename__ = "org_report_runs"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    period_type = Column(String, nullable=False)  # week | month
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    users_csv_link = Column(String, nullable=False, default="")
    report_xlsx_link = Column(String, nullable=False, default="")
    report_pdf_link = Column(String, nullable=False, default="")
    kpi_snapshot = Column(Text, nullable=False, default="{}")

    organization = relationship("Organization", back_populates="report_runs")
