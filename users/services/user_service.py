from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import User
from schemas.user_schema import UserCreate
from passlib.context import CryptContext
from jose import jwt
import aiosmtplib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def register_or_login(user_data: UserCreate, db: AsyncSession):


    db_user = await db.execute(select(User).filter(User.email == user_data.email))
    db_user = db_user.scalars().first()

    if db_user:
        # If user exists, check if the password matches
        if pwd_context.verify(user_data.password, db_user.hashed_password):
            if db_user.is_active:
                return {"message": "Login successful", "user": db_user}
            else:
                raise HTTPException(status_code=400, detail="User is not active. Check your email to activate.")
        else:
            raise HTTPException(status_code=401, detail="Invalid login credentials")
    else:
        # Register new user
        hashed_password = pwd_context.hash(user_data.password)
        new_user = User(email=user_data.email, hashed_password=hashed_password, is_active=False)
        db.add(new_user)
        await db.commit()
        await send_verification_email(new_user)
        return {"message": "User registered successfully, please check your email to activate your account",
                "user": new_user}


async def send_verification_email(user: User):
    token = jwt.encode({"user_id": user.id}, "SECRET_KEY", algorithm="HS256")
    email_body = f"Please click on the link to verify your account: http://yourdomain.com/verify/{token}"
    message = aiosmtplib.EmailMessage(
        from_email="your-email@example.com",
        to=[user.email],
        subject="Verify your email",
        content=email_body
    )
    await aiosmtplib.send(message, hostname="smtp.example.com", port=587, use_tls=True)

# Add additional functions as needed (e.g., for token verification)
