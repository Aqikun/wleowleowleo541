# backend/src/domains/collaboration/router.py

# # Mengimpor semua komponen yang kita butuhkan
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

# # Impor dari dalam proyek kita
from src.core.database import get_db
# # Kita gunakan dependency baru yang tadi dibuat
from src.core.dependencies import get_current_user_from_ws
from src.domains.users.models import User
from . import crud, schemas, services

# # Membuat instance APIRouter
router = APIRouter(
    tags=["Collaboration"],
    prefix="/collaboration"
)

# # Endpoint utama untuk WebSocket
@router.websocket("/ws/{room_name}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_name: str,
    # # Menggunakan dependency otentikasi khusus WebSocket kita
    current_user: User = Depends(get_current_user_from_ws),
    db: Session = Depends(get_db)
):
    # # Hubungkan pengguna ke manajer koneksi
    await services.manager.connect(websocket, room_name)
    
    # # Siarkan pesan bahwa pengguna telah bergabung
    await services.manager.broadcast(f"Info: '{current_user.username}' has joined the room.", room_name)

    try:
        # # Loop untuk terus mendengarkan pesan dari klien ini
        while True:
            data = await websocket.receive_text()

            # # Simpan pesan ke database menggunakan fungsi CRUD
            message_schema = schemas.ChatMessageCreate(content=data)
            db_message = crud.create_chat_message(
                db=db, 
                message=message_schema, 
                sender_id=current_user.id, 
                room_name=room_name
            )

            # # Buat data broadcast dalam format JSON yang benar menggunakan skema
            broadcast_data = schemas.ChatMessageInDB.from_orm(db_message).json()
            
            # # Siarkan pesan yang sudah diformat ke semua orang di ruangan
            await services.manager.broadcast(broadcast_data, room_name)

    # # Blok ini berjalan jika koneksi terputus
    except WebSocketDisconnect:
        services.manager.disconnect(websocket, room_name)
        # # Siarkan pesan bahwa pengguna telah keluar
        await services.manager.broadcast(f"Info: '{current_user.username}' has left the room.", room_name)