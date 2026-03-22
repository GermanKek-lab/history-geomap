from app.db.models.document import Document


def test_document_has_unique_filename_constraint() -> None:
    constraint_names = {constraint.name for constraint in Document.__table__.constraints}

    assert "uq_documents_filename" in constraint_names
