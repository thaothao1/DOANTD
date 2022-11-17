"""update Label

Revision ID: 9e569ea5da68
Revises: 51bcf7882305
Create Date: 2022-11-16 15:57:15.930173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e569ea5da68'
down_revision = '51bcf7882305'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('labels', 'link')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('labels', sa.Column('link', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
