"""empty message

Revision ID: 51db27416009
Revises: 53fe4acd2d3d
Create Date: 2024-08-08 22:24:35.057208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51db27416009'
down_revision = '53fe4acd2d3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.Column('planets_id', sa.Integer(), nullable=True),
    sa.Column('species_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.uid'], ),
    sa.ForeignKeyConstraint(['planets_id'], ['planets.uid'], ),
    sa.ForeignKeyConstraint(['species_id'], ['species.uid'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=250), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    op.drop_table('favorites')
    # ### end Alembic commands ###
