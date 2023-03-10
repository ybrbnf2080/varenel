"""create_tables

Revision ID: 81c0f7c3f989
Revises: 
Create Date: 2022-12-24 03:09:48.778967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81c0f7c3f989'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('participants',
    sa.Column('number', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('patronymic', sa.String(), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('rank', sa.Enum('NO_RANK', 'THREE_JUN', 'TWO_JUN', 'ONE_JUN', 'THREE_MID', 'TWO_MID', 'ONE_MID', name='rank'), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('team', sa.String(), nullable=False),
    sa.Column('group', sa.Enum('MAN_YOUTH', 'WOMAN_YOUTH', 'MAN_TEEN', 'WOMAN_TEEN', 'MAN_SUPERTEEN', 'WOMAN_SUPERTEEN', 'MAN_MICRO', 'WOMAN_MICRO', name='group'), nullable=False),
    sa.Column('couch', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('number')
    )
    op.create_table('tracks',
    sa.Column('number', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('group', sa.Enum('MAN_YOUTH', 'WOMAN_YOUTH', 'MAN_TEEN', 'WOMAN_TEEN', 'MAN_SUPERTEEN', 'WOMAN_SUPERTEEN', 'MAN_MICRO', 'WOMAN_MICRO', name='group'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('number')
    )
    op.create_table('results_participant',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('participant_number', sa.BigInteger(), nullable=False),
    sa.Column('point', sa.Float(), nullable=False),
    sa.Column('total_time', sa.Interval(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['participant_number'], ['participants.number'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('participant_number')
    )
    op.create_table('trys_festival',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('participant_number', sa.Integer(), nullable=False),
    sa.Column('track', sa.Integer(), nullable=False),
    sa.Column('result', sa.Float(), nullable=False),
    sa.Column('time', sa.Interval(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("timezone('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['participant_number'], ['participants.number'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['track'], ['tracks.number'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trys_festival')
    op.drop_table('results_participant')
    op.drop_table('tracks')
    op.drop_table('participants')
    # ### end Alembic commands ###
