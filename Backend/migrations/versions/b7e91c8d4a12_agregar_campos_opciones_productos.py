"""agregar campos opciones productos

Revision ID: b7e91c8d4a12
Revises: e340bb54f575
Create Date: 2026-09-22

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7e91c8d4a12'
down_revision = 'e340bb54f575'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table(
        'opciones_productos',
        schema=None
    ) as batch_op:

        batch_op.add_column(
            sa.Column(
                'activa',
                sa.Boolean(),
                nullable=False,
                server_default=sa.true()
            )
        )

        batch_op.add_column(
            sa.Column(
                'opcion_principal_id',
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            'fk_opciones_productos_opcion_principal',
            'opciones_productos',
            ['opcion_principal_id'],
            ['id']
        )


def downgrade():

    with op.batch_alter_table(
        'opciones_productos',
        schema=None
    ) as batch_op:

        batch_op.drop_constraint(
            'fk_opciones_productos_opcion_principal',
            type_='foreignkey'
        )

        batch_op.drop_column('opcion_principal_id')
        batch_op.drop_column('activa')
