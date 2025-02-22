"""Add sequence number

Revision ID: add_sequence_number
Revises: initial_migration
Create Date: 2024-02-20

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'add_sequence_number'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sequence
    op.execute("CREATE SEQUENCE IF NOT EXISTS itinerary_seq")
    
    # Add sequence_number column
    op.add_column(
        'itinerary_queries',
        sa.Column(
            'sequence_number',
            sa.Integer(),
            sa.Sequence('itinerary_seq'),
            nullable=False,
            unique=True,
            index=True
        )
    )
    
    # Create index
    op.create_index(
        'ix_itinerary_queries_sequence_number',
        'itinerary_queries',
        ['sequence_number']
    )


def downgrade() -> None:
    # Drop index
    op.drop_index('ix_itinerary_queries_sequence_number')
    
    # Drop column
    op.drop_column('itinerary_queries', 'sequence_number')
    
    # Drop sequence
    op.execute("DROP SEQUENCE IF EXISTS itinerary_seq") 