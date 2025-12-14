"""rename password to hashed_password

Revision ID: 765019ef270c
Revises: 4f18306ce1ab
Create Date: 2025-11-04 20:58:09.735531

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "765019ef270c"
down_revision: Union[str, None] = "4f18306ce1ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("hashed_password", sa.String(length=200), nullable=True))

    op.execute("UPDATE users SET hashed_password = password")

    op.alter_column("users", "hashed_password", nullable=False)

    op.drop_column("users", "password")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("password", sa.VARCHAR(length=200), nullable=True),
    )

    op.execute("UPDATE users SET password = hashed_password")

    op.alter_column("users", "password", nullable=False)

    op.drop_column("users", "hashed_password")
