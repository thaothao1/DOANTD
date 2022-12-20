"""add column image showProduct

Revision ID: 688a27b24e76
Revises: eb56cd566581
Create Date: 2022-12-11 12:28:53.095470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '688a27b24e76'
down_revision = 'eb56cd566581'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('showProducts', sa.Column('image', sa.String(length=1200), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('showProducts', 'image')
    # ### end Alembic commands ###