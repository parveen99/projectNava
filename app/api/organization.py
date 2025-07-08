from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_master_db, create_org_database, get_org_engine
from app.models import Organization, AdminUser
from app.schemas import OrganizationCreate, OrganizationResponse
from app.auth import get_password_hash
from app.utils import (
    validate_organization_name, 
    handle_database_error, 
    create_organization_tables
)

router = APIRouter(prefix="/org", tags=["organizations"])


@router.post("/create", response_model=OrganizationResponse)
def create_organization(
    org_data: OrganizationCreate,
    db: Session = Depends(get_master_db)
):
    
    if not validate_organization_name(org_data.organization_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid organization name format"
        )

    existing_org = db.query(Organization).filter(
        Organization.name == org_data.organization_name
    ).first()
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this name already exists"
        )
    
    # Check if admin email already exists
    existing_admin = db.query(AdminUser).filter(
        AdminUser.email == org_data.email
    ).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists"
        )
    
    try:
        db_name = create_org_database(org_data.organization_name)
        organization = Organization(
            name=org_data.organization_name,
            database_name=db_name
        )
        db.add(organization)
        db.flush()
        
        admin_user = AdminUser(
            email=org_data.email,
            hashed_password=get_password_hash(org_data.password),
            organization_id=organization.id
        )
        db.add(admin_user)
        db.commit()
        db.refresh(organization)
        
        org_engine = get_org_engine(org_data.organization_name)
        create_organization_tables(org_engine)
        
        return organization
        
    except IntegrityError as e:
        db.rollback()
        error_message = handle_database_error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create organization: {str(e)}"
        )


@router.get("/get", response_model=OrganizationResponse)
def get_organization_by_name(
    organization_name: str,
    db: Session = Depends(get_master_db)
):
    """Get organization by name"""
    
    organization = db.query(Organization).filter(
        Organization.name == organization_name
    ).first()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return organization 