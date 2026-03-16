import secrets
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_utils import create_access_token, get_current_user, get_password_hash, verify_password
from database import get_db
from models import Organization, OrganizationMember, SavingsVault, User, UserOrgConsent
from schemas import Token, UserCreate, UserLogin, UserMeOut

router = APIRouter(prefix="/auth", tags=["Auth"])

VALID_ACCOUNT_TYPES = {"individual", "organization"}


def _generate_invite_code(db: Session, length: int = 10) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    for _ in range(20):
        candidate = "".join(secrets.choice(alphabet) for _ in range(length))
        exists = db.query(Organization).filter(Organization.invite_code == candidate).first()
        if not exists:
            return candidate
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not generate invite code")


@router.post("/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    account_type = payload.account_type if payload.account_type in VALID_ACCOUNT_TYPES else "individual"
    if account_type == "organization" and not payload.organization_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Organization name is required for organization account",
        )

    user = User(
        email=payload.email.lower(),
        hashed_password=get_password_hash(payload.password),
        account_type=account_type,
    )
    db.add(user)
    db.flush()

    if account_type == "organization":
        org = Organization(
            name=(payload.organization_name or "").strip(),
            industry=(payload.organization_industry or "").strip(),
            invite_code=_generate_invite_code(db),
        )
        db.add(org)
        db.flush()
        db.add(OrganizationMember(organization_id=org.id, user_id=user.id, role="owner", status="active"))
        db.add(
            UserOrgConsent(
                organization_id=org.id,
                user_id=user.id,
                is_active=True,
                consent_given_at=datetime.now(timezone.utc),
            )
        )

    db.add(SavingsVault(user_id=user.id, name="Финансовый сейф", balance=0, target_amount=0))
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)


@router.get("/me", response_model=UserMeOut)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    has_organizations = (
        db.query(OrganizationMember)
        .filter(OrganizationMember.user_id == current_user.id, OrganizationMember.status == "active")
        .first()
        is not None
    )
    account_type = current_user.account_type if current_user.account_type in VALID_ACCOUNT_TYPES else "individual"
    return UserMeOut(
        id=current_user.id,
        email=current_user.email,
        account_type=account_type,
        has_organizations=has_organizations,
    )
