from toml import load


class AppUtil:
    @staticmethod
    def get_version() -> str:
        try:
            pyproject_data = load("pyproject.toml")
            return str(pyproject_data["project"]["version"])
        except Exception:
            return "0.0.0"
