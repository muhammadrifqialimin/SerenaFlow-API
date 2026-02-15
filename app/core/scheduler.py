from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.database import SessionLocal
from app.models import models
from app.core.email_utils import send_email_notification


scheduler = AsyncIOScheduler()


async def daily_reminder_job():
    db = SessionLocal()
    try:

        users = db.query(models.User).all()
        
        print(f"⏰ Menjalankan Reminder untuk {len(users)} user...")

        for user in users:
            if "@" in user.email:
                subject = "🔔 Waktunya Jurnal Harian!"
                body = f"""
                <h3>Halo {user.email}!</h3>
                <p>Gimana harimu tadi? Jangan lupa cerita di SereneFlow ya.</p>
                <p>Luangkan 5 menit untuk kesehatan mentalmu.</p>
                <br>
                <p><i>- SereneFlow Reminder Bot</i></p>
                """
                
                await send_email_notification([user.email], subject, body)
                
    except Exception as e:
        print(f"Error di Scheduler: {e}")
    finally:
        db.close()

def start_scheduler():

    scheduler.add_job(daily_reminder_job, "interval", minutes=1)
    
    scheduler.start()
    print("🚀 Scheduler Berjalan! Reminder akan dikirim tiap 1 menit (Mode Test).")