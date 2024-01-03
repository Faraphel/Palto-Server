from pathlib import Path

from django.core.management.utils import get_random_secret_key


path_dotenv = Path("./.env")


def create_dotenv(force: bool = False) -> Path:
    # if not forced and the file already exist, ignore
    if not force and path_dotenv.exists():
        return path_dotenv

    # otherwise create the file
    path_dotenv.write_text(
        (
            f"DJANGO_SETTINGS_MODULE='Palto.settings'\n"
            f"DJANGO_SECRET={get_random_secret_key()!r}\n"
        ),
        encoding="utf-8"
    )

    return path_dotenv
