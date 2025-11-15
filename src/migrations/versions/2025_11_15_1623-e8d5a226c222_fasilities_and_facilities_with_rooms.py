"""fasilities and facilities with rooms

Revision ID: e8d5a226c222
Revises: bd1102352a48
Create Date: 2025-11-15 16:23:07.093935

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e8d5a226c222"
down_revision: Union[str, None] = "bd1102352a48"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "facilities_and_rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("facilities", sa.Integer(), nullable=False),
        sa.Column("rooms", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["facilities"],
            ["facilities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["rooms"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("facilities_and_rooms")
    op.drop_table("facilities")
