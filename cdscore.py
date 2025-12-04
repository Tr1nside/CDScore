import sys

from src import CDSApp


def main() -> int:
    app = CDSApp(sys.argv[1:])
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
