import os


def migrate():
    os.system("alembic upgrade head")


if __name__ == "__main__":
    migrate()
