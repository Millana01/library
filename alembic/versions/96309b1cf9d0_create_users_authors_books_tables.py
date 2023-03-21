"""create users authors books tables

Revision ID: 96309b1cf9d0
Revises: 
Create Date: 2023-02-21 17:17:38.393735

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "96309b1cf9d0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String(50), unique=False, index=True),
        sa.Column("hashed_password", sa.String(100)),
        sa.Column("is_active", sa.Boolean, default=True),
    )
    op.create_table(
        "user_books",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer),
        sa.Column("book_id", sa.Integer),
        sa.Column("count", sa.Integer),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("title", sa.String(50), index=True),
        sa.Column("description", sa.String(50)),
        sa.Column("author_id", sa.Integer),
        sa.Column("total_count", sa.Integer),
        sa.Column("available_count", sa.Integer),
    )
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column("name", sa.String(50), unique=True, index=True),
    )
    op.create_table(
        "author_books",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("author_id", sa.Integer),
        sa.Column("book_id", sa.Integer),
    )
    op.create_foreign_key(
        "fk_books_author_id", "books", "authors", ["author_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_user_books_user_id", "user_books", "users", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_user_books_book_id", "user_books", "books", ["book_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_author_books_author_id", "author_books", "authors", ["author_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_author_books_book_id", "author_books", "books", ["book_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("fk_books_author_id", "books", type_="foreignkey")
    op.drop_constraint("fk_user_books_user_id", "user_books", type_="foreignkey")
    op.drop_constraint("fk_user_books_book_id", "user_books", type_="foreignkey")
    op.drop_constraint("fk_author_books_author_id", "author_books", type_="foreignkey")
    op.drop_constraint("fk_author_books_book_id", "author_books", type_="foreignkey")
    op.drop_table("users")
    op.drop_table("books")
    op.drop_table("authors")
    op.drop_table("user_books")
    op.drop_table("author_books")
