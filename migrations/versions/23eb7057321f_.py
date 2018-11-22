"""empty message

Revision ID: 23eb7057321f
Revises: 
Create Date: 2018-11-22 10:35:45.335887

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '23eb7057321f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_first_name', table_name='users')
    op.drop_index('ix_users_last_name', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_roles_default', table_name='roles')
    op.drop_table('roles')
    op.drop_column('transcript', 'date_created')
    op.drop_column('transcript', 'confidence')
    op.drop_column('transcript', 'date_modified')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transcript', sa.Column('date_modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('transcript', sa.Column('confidence', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('transcript', sa.Column('date_created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), server_default=sa.text(u"nextval('roles_id_seq'::regclass)"), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('index', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('default', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('permissions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'roles_pkey'),
    sa.UniqueConstraint('name', name=u'roles_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_roles_default', 'roles', ['default'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('confirmed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], [u'roles.id'], name=u'users_role_id_fkey'),
    sa.PrimaryKeyConstraint('id', name=u'users_pkey')
    )
    op.create_index('ix_users_last_name', 'users', ['last_name'], unique=False)
    op.create_index('ix_users_first_name', 'users', ['first_name'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###
