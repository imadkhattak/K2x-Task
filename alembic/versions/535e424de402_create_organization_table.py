"""create organization table

Revision ID: 535e424de402
Revises: 
Create Date: 2025-08-16 08:39:08.737685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '535e424de402'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("USE orgs_db")
    
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255)),
        sa.Column('industry', sa.String(255)),
        sa.Column('location', sa.String(255)),
        sa.Column('description', sa.Text),
    )
    
    op.bulk_insert(
        sa.table('organizations',
            sa.column('name'),
            sa.column('industry'),
            sa.column('location'),
            sa.column('description')
        ),
        [
            {'name': 'Acme Analytics', 'industry': 'Data & AI', 
             'location': 'Peshawar', 'description': 'Analytics consultancy for retail.'},
            {'name': 'Northwind Health', 'industry': 'Healthcare', 
             'location': 'Karachi', 'description': 'Primary care clinics network.'}
        ]
    )


def downgrade():
    op.execute("DROP DATABASE IF EXISTS orgs_db")