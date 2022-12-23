"""fix_tables

Revision ID: 3359c8dc98cf
Revises: 5166afb29d4f
Create Date: 2022-12-22 13:11:48.029628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3359c8dc98cf'
down_revision = '5166afb29d4f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'results_participant', ['participant_number'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'results_participant', type_='unique')
    # ### end Alembic commands ###