"""some

Revision ID: c737226bf2eb
Revises: 848c5e79a6f5
Create Date: 2024-03-11 16:34:47.033477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c737226bf2eb'
down_revision: Union[str, None] = '848c5e79a6f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'cover_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('cover_url', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    # ### end Alembic commands ###