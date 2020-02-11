"""create indexing to banners

Revision ID: 9563d631e60d
Revises:
Create Date: 2020-02-10 18:40:26.224325

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '9563d631e60d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("idx_title_url_visible", "banner", ["title", "url", "visible"])


def downgrade():
    op.drop_index('idx_title_url_visible', table_name='banner')
