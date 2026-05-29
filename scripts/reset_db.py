import asyncio
import os
import sys
from datetime import date

# Add the parent directory to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import delete
from app.core.db import SessionLocal
from app.models.user import User
from app.core.security import hash_password

async def run():
    async with SessionLocal() as db:
        print("Deletando todos os usuários...")
        await db.execute(delete(User))
        
        print("Criando usuário iruziky...")
        new_user = User(
            nickname="iruziky",
            email="iruziky@gmail.com",
            password_hash=hash_password("omilhor"),
            daily_score=1000,
            has_played_today=True,
            streak_days=10,
            last_played_date=date.today()
        )
        db.add(new_user)
        await db.commit()
        print("Sucesso! Banco limpo e usuário criado.")

if __name__ == "__main__":
    asyncio.run(run())
