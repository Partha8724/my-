"""init

Revision ID: 0001
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('assets', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('symbol', sa.String(length=20), nullable=False), sa.Column('asset_type', sa.String(length=20), nullable=False), sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    op.create_table('watchlist_items', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('symbol', sa.String(length=20), nullable=False), sa.Column('min_confidence', sa.Integer(), nullable=False), sa.Column('whale_threshold', sa.Float(), nullable=False), sa.Column('cooldown_seconds', sa.Integer(), nullable=False), sa.Column('enabled', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_table('watchlist_items')
    op.drop_table('assets')
