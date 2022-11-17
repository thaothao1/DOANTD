"""create new data

Revision ID: 51bcf7882305
Revises: 
Create Date: 2022-11-16 13:38:21.217210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51bcf7882305'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labels',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('link', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_labels_id'), 'labels', ['id'], unique=False)
    op.create_table('shops',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('link', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_shops_id'), 'shops', ['id'], unique=False)
    op.create_table('products',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=1150), nullable=True),
    sa.Column('link', sa.String(length=2150), nullable=True),
    sa.Column('image', sa.String(length=5000), nullable=True),
    sa.Column('price', sa.String(length=1150), nullable=True),
    sa.Column('priceSale', sa.String(length=1150), nullable=True),
    sa.Column('rating', sa.String(length=1000), nullable=True),
    sa.Column('shopId', sa.Integer(), nullable=True),
    sa.Column('labelId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['labelId'], ['labels.id'], ),
    sa.ForeignKeyConstraint(['shopId'], ['shops.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_table('showProducts',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('changed_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('price', sa.String(length=200), nullable=True),
    sa.Column('thegioididongId', sa.Integer(), nullable=True),
    sa.Column('lazadaId', sa.Integer(), nullable=True),
    sa.Column('fptId', sa.Integer(), nullable=True),
    sa.Column('shopeeId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fptId'], ['products.id'], ),
    sa.ForeignKeyConstraint(['lazadaId'], ['products.id'], ),
    sa.ForeignKeyConstraint(['shopeeId'], ['products.id'], ),
    sa.ForeignKeyConstraint(['thegioididongId'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_showProducts_id'), 'showProducts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_showProducts_id'), table_name='showProducts')
    op.drop_table('showProducts')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    op.drop_index(op.f('ix_shops_id'), table_name='shops')
    op.drop_table('shops')
    op.drop_index(op.f('ix_labels_id'), table_name='labels')
    op.drop_table('labels')
    # ### end Alembic commands ###
