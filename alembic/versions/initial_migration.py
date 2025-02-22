"""Initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-02-20

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'itinerary_queries',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('query', sa.String(), nullable=False),
        sa.Column('itinerary_response', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('itinerary_queries') 