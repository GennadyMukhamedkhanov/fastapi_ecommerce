"""change grade enum to native integer 333

Revision ID: 4dc7facbfb82
Revises: b73d1296d164
Create Date: 2026-02-25 12:43:09.609123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dc7facbfb82'
down_revision: Union[str, Sequence[str], None] = 'b73d1296d164'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # 1️⃣ Добавляем временный столбец
    op.add_column('reviews', sa.Column('grade_int', sa.Integer(), nullable=True))

    # 2️⃣ Заполняем его из enum (или текста)
    op.execute("""
        UPDATE reviews
        SET grade_int = CASE grade
            WHEN 'ONE'   THEN 1
            WHEN 'TWO'   THEN 2
            WHEN 'THREE' THEN 3
            WHEN 'FOUR'  THEN 4
            WHEN 'FIVE'  THEN 5
        END
    """)

    # 3️⃣ Удаляем старый столбец
    op.drop_column('reviews', 'grade')

    # 4️⃣ Переименовываем новый столбец в grade
    op.alter_column('reviews', 'grade_int', new_column_name='grade')

    # 5️⃣ (Опционально) Добавляем ограничение CHECK
    op.create_check_constraint(
        'ck_reviews_grade_range',
        'reviews',
        'grade >= 0 AND grade <= 5'
    )

def downgrade():
    # Откат, если понадобится
    op.add_column('reviews', sa.Column('grade_enum', sa.Enum('ONE', 'TWO', 'THREE', 'FOUR', 'FIVE'), nullable=True))
    op.execute("""
        UPDATE reviews
        SET grade_enum = CASE grade
            WHEN 1 THEN 'ONE'
            WHEN 2 THEN 'TWO'
            WHEN 3 THEN 'THREE'
            WHEN 4 THEN 'FOUR'
            WHEN 5 THEN 'FIVE'
        END
    """)
    op.drop_column('reviews', 'grade')
    op.alter_column('reviews', 'grade_enum', new_column_name='grade')
