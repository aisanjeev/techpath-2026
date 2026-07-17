"""Merge the three divergent migration heads

Collapses the branched history into a single head so that later migrations have one
unambiguous parent and ``alembic upgrade head`` works without the plural form.

The three heads being merged:
  d5e6f7g8h9i0 — pilot_signups
  k1l2m3n4o5p6 — services_add_bento_layout
  q2r3s4t5u6v7 — pages

This is a pure merge: it has no schema effect. On upgrade, Alembic replaces the three
rows in ``alembic_version`` with this single revision.

Revision ID: m1n2o3p4q5r6
Revises: d5e6f7g8h9i0, k1l2m3n4o5p6, q2r3s4t5u6v7
Create Date: 2026-07-16

"""

# revision identifiers, used by Alembic.
revision = 'm1n2o3p4q5r6'
down_revision = ('d5e6f7g8h9i0', 'k1l2m3n4o5p6', 'q2r3s4t5u6v7')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
