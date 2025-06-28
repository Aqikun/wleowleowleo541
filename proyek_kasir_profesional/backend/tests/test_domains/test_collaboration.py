# Lokasi file: tests/test_domains/test_collaboration.py
# PERBAIKAN: Menambahkan field "email" saat membuat objek User

import pytest
from src.domains.collaboration.models import ChatMessage
from src.domains.users.models import User
from src.core.security import get_password_hash

@pytest.mark.usefixtures("db_session")
def test_create_and_retrieve_chat_message(db_session):
    # TAHAP 1: SETUP
    test_user = User(
        username="testuser_chat",
        email="chat@example.com",  # <-- DITAMBAHKAN
        hashed_password=get_password_hash("password123"),
        role="Kasir"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # Buat objek ChatMessage di memori
    new_message = ChatMessage(
        content="Ini adalah pesan untuk verifikasi.",
        room_name="verifikasi_awal",
        sender_id=test_user.id
    )

    # TAHAP 2: ACTION
    db_session.add(new_message)
    db_session.commit()

    # TAHAP 3: ASSERTION
    retrieved_message = db_session.query(ChatMessage).filter(
        ChatMessage.id == new_message.id
    ).first()

    assert retrieved_message is not None
    assert retrieved_message.content == "Ini adalah pesan untuk verifikasi."
    assert retrieved_message.sender.username == "testuser_chat"