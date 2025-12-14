"""make user email unique

Revision ID: 4f18306ce1ab
Revises: 6b9a8ae6ed6a
Create Date: 2025-11-03 11:31:35.797544

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4f18306ce1ab"
down_revision: Union[str, None] = "6b9a8ae6ed6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
