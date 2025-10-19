"""chat resume

Revision ID: 49558e77037f
Revises: a5a432359f77
Create Date: 2025-10-18 23:30:16.527296
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '49558e77037f'
down_revision: Union[str, Sequence[str], None] = 'a5a432359f77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создание таблицы чатов
    op.create_table(
        'chats',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    # Создание таблицы резюме с использованием существующего ENUM educationlevel
    op.create_table(
        'resumes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(50), nullable=True),
        sa.Column('summary', sa.Text, nullable=True),
        sa.Column('experience', postgresql.JSONB, nullable=True),  # JSON
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('skills', postgresql.ARRAY(sa.String), nullable=True),
        sa.Column('languages', postgresql.ARRAY(sa.String), nullable=True), # массив строк
        sa.Column('salary_expectation', sa.String(100), nullable=True),
        sa.Column('education', postgresql.ENUM(name="educationlevel",  create_type=False), nullable=True, server_default='ANY'),
        sa.Column('employment_form', sa.Enum(name='employmentform',create_type=False),nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=True)
    )

    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)

    # Создание таблицы сообщений
    op.create_table(
        'messages',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('chat_id', sa.Integer(), sa.ForeignKey('chats.id', ondelete='CASCADE'), nullable=True),
        sa.Column('sender', sa.Enum('user', 'bot', name='messagesender'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )




def downgrade() -> None:
    """Downgrade schema."""
    # Возврат skills в JSON

    op.drop_table('messages')
    op.drop_index(op.f('ix_resumes_id'), table_name='resumes')
    op.drop_table('resumes')
    op.drop_table('chats')
    op.execute("DROP TYPE IF EXISTS messagesender;")
