from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_master_db
from app.models import AdminUser
from app.schemas import AdminLogin, Token
from app.auth import verify_password, create_access_token

router = APIRouter(prefix="/admin", tags=["authentication"])


@router.post("/login", response_model=Token)
def admin_login(login_data: AdminLogin, db: Session = Depends(get_master_db)):
    admin = db.query(AdminUser).filter(
        AdminUser.email == login_data.email
    ).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password, Please try again",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(login_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password, Please try again",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # If all success, create access token
    access_token = create_access_token(
        data={"sub": admin.email, "org_id": admin.organization_id}
    )
    return {"access_token": access_token, "token_type": "bearer"}