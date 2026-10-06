"""Agregar usuario a personalizaciones

Revision ID: 8d94c072f483
Revises: 682deeaf810b
Create Date: 2026-10-05 23:27:21.675178

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8d94c072f483"
down_revision = "682deeaf810b"
branch_labels = None
depends_on = None


def upgrade():

    op.add_column(
        "personalizaciones",
        sa.Column(
            "usuario_id",
            sa.Integer(),
            nullable=True
        )
    )

    op.execute(
        """
        UPDATE personalizaciones
        SET usuario_id = 1
        WHERE usuario_id IS NULL
        """
    )

    op.create_foreign_key(
        "fk_personalizaciones_usuario",
        "personalizaciones",
        "usuarios",
        ["usuario_id"],
        ["id"]
    )

    op.alter_column(
        "personalizaciones",
        "usuario_id",
        existing_type=sa.Integer(),
        nullable=False
    )


def downgrade():

    op.drop_constraint(
        "fk_personalizaciones_usuario",
        "personalizaciones",
        type_="foreignkey"
    )

    op.drop_column(
        "personalizaciones",
        "usuario_id"
    )