import os
import re
from pathlib import Path
from typing import Final, Match

import regex_pattern

"""
Refactoring logic:
1. Throw meaningful error messages + path and env_var validation
2. Cleared up the repetitive logics
3. More robust regex (Only allow 1 instance of the keyword) 
"""

# Constants
BASE_DIR: Final[Path] = Path(
    os.path.join(os.environ["SourcePath"], "develop", "global", "src")
)
SCONSTRUCT_PATH: Final[Path] = Path(os.path.join(BASE_DIR, "SConstruct"))
VERSION_PATH: Final[Path] = Path(os.path.join(BASE_DIR, "VERSION"))

BUILD_NUM: Final[str] = os.environ.get("BuildNum", "")


# Validation
def _validate_dir(dir: Path):
    if not dir.is_dir():
        raise NotADirectoryError(f"{dir} is not a directory")


def _validate_file(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} can't be found")


def _validate_is_int(num: str, var: str):
    if not num.strip().isdigit():
        raise ValueError(f"{var}: {num} is not integer.")


def _chmod_to_executable(path: Path):
    try:
        path.chmod(0o755)
    except PermissionError:
        print("Warning: No Permission to chmod 755")
    except Exception as e:
        raise e


def validation(path: Path):
    _validate_dir(BASE_DIR)
    _validate_file(path)
    _validate_is_int(BUILD_NUM, "Environment Variable: BuildNum")
    _chmod_to_executable(path)


def replace_in_file(path: Path, regex_pattern: re.Pattern[str], replacer_func):
    validation(path)
    file = path.read_text(encoding="utf-8")

    matches = regex_pattern.findall(file)

    if len(matches) != 1:
        raise ValueError(f"Expected exactly 1 matches, found {len(matches)}")

    match_obj = regex_pattern.search(file)
    new_block = replacer_func(match_obj)

    new_content = file[: match_obj.start(1)] + new_block + file[match_obj.end(1) :]

    path.write_text(new_content, encoding="utf-8")


# SCONSTRUCT file interesting lines
# config.version = Version(
# major=15,
# minor=0,
# point=6,
# patch=0
# )
def replace_Sconstruct(match: Match[str]) -> str:
    return re.sub(
        regex_pattern.POINT_PATTERN,
        f"point={BUILD_NUM}",
        match.group(0),
        flags=re.IGNORECASE,
    )


# VERSION file interesting line
# ADLMSDK_VERSION_POINT=6
def replace_version(match: Match[str]) -> str:
    return re.sub(
        regex_pattern.VERSION_FILE_POINT_PATTERN,
        rf"ADLMSDK_VERSION_POINT={BUILD_NUM}",
        match.group(0),
    )


def updateSconstruct():
    """
    Assume there'll always be valid Version block. i.e.
    Version(
    major=int,
    minor=int,
    point=int,
    patch=int
    )
    """
    replace_in_file(
        SCONSTRUCT_PATH, regex_pattern.RE_PATTERN_SCONSTRUCT_VERSION, replace_Sconstruct
    )


def updateVersion():
    """
    Assume there'll always be the keyword ADLMSDK_VERSION_POINT=(int)
    """
    replace_in_file(
        VERSION_PATH, regex_pattern.VERSION_FILE_POINT_PATTERN, replace_version
    )


def main():
    updateSconstruct()
    print(f"Sconstruct point updated to {BUILD_NUM}")
    updateVersion()
    print(f"ADLMSDK version updated to {BUILD_NUM}")


main()
