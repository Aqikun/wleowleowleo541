# backend/src/domains/collaboration/crud.py

# # Mengimpor komponen yang diperlukan dari SQLAlchemy dan skema kita.
from sqlalchemy.orm import Session
from . import models, schemas

# # Fungsi untuk membuat dan menyimpan satu pesan chat ke database.
def create_chat_message(db: Session, message: schemas.ChatMessageCreate, sender_id: int, room_name: str) -> models.ChatMessage:
    # # Membuat objek model SQLAlchemy dari data yang diberikan.
    db_message = models.ChatMessage(
        content=message.content,
        sender_id=sender_id,
        room_name=room_name
    )
    # # Menambahkan objek ke sesi database.
    db.add(db_message)
    # # Menyimpan perubahan secara permanen ke database.
    db.commit()
    # # Memuat ulang objek dari database untuk mendapatkan data yang dibuat otomatis (seperti id dan timestamp).
    db.refresh(db_message)
    # # Mengembalikan objek pesan yang sudah lengkap.
    return db_message


# # Fungsi untuk mengambil riwayat pesan dari sebuah ruangan.
def get_messages_by_room(db: Session, room_name: str, skip: int = 0, limit: int = 100) -> list[models.ChatMessage]:
    # # Menjalankan query ke database untuk mendapatkan pesan.
    return (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.room_name == room_name)
        # # Mengurutkan berdasarkan waktu, dari yang terlama ke terbaru.
        .order_by(models.ChatMessage.timestamp.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )