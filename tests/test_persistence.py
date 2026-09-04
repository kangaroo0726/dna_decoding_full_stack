from api.database import SessionLocal
from api.models import User, SavedSequence, DecodingHistory
from sqlalchemy import select

db = SessionLocal()


def test_users():
    user = User(username="testuser", email="test@example.com", password_hash="dummy_hash")

    db.add(user)
    db.commit()

    db.refresh(user)

    statement = select(User).where(User.username == "testuser")
    result = db.execute(statement)
    found_user = result.scalar_one()

    assert found_user.id == user.id
    assert found_user.username == "testuser"
    assert found_user.email == "test@example.com"
    assert found_user.password_hash == "dummy_hash"

    db.delete(user)
    db.commit()

def test_sequence():
    user = User(username="sequence_testuser", email="sequence_test@example.com", password_hash="dummy_hash")
    db.add(user)
    db.commit()
    db.refresh(user)

    saved_sequence = SavedSequence(
        user_id=user.id,
        name="new_sequence",
        sequence="AUG",
        sequence_type="mrna",
        five_to_three=True,
    )

    db.add(saved_sequence)
    db.commit()

    db.refresh(saved_sequence)

    statement = select(SavedSequence).where(SavedSequence.name == "new_sequence")
    result = db.execute(statement)
    found_sequence = result.scalar_one()

    assert found_sequence.user_id == user.id
    assert found_sequence.id == saved_sequence.id
    assert found_sequence.name == "new_sequence"
    assert found_sequence.sequence == "AUG"
    assert found_sequence.sequence_type == "mrna"
    assert found_sequence.five_to_three is True
    assert found_sequence.user.saved_sequences[0].name == "new_sequence"
    assert found_sequence.user.saved_sequences[0].sequence == "AUG"
    assert found_sequence.created_at is not None
    assert found_sequence.updated_at is not None

    db.delete(found_sequence)
    db.delete(user)
    db.commit()


def test_decoding_history():
    user = User(username="history_testuser", email="history_test@example.com", password_hash="dummy_hash")
    db.add(user)
    db.commit()
    db.refresh(user)

    decoding_history = DecodingHistory(
        user_id=user.id,
        input_sequence="AUGGCUUAA",
        input_type="mrna",
        five_to_three=True,
        converted_sequence="AUG GCU UAA",
        proteins=["methionine", "alanine", "stop"],
    )

    db.add(decoding_history)
    db.commit()
    db.refresh(decoding_history)

    statement = select(DecodingHistory).where(DecodingHistory.id == decoding_history.id)
    result = db.execute(statement)
    found_history = result.scalar_one()

    assert found_history.user_id == user.id
    assert found_history.id == decoding_history.id
    assert found_history.input_sequence == "AUGGCUUAA"
    assert found_history.input_type == "mrna"
    assert found_history.five_to_three is True
    assert found_history.converted_sequence == "AUG GCU UAA"
    assert found_history.proteins == ["methionine", "alanine", "stop"]
    assert found_history.user.decoding_history[0].input_sequence == "AUGGCUUAA"
    assert found_history.created_at is not None

    db.delete(found_history)
    db.delete(user)
    db.commit()

