import sys

from src.cds_app import CDSApp


def main():
    app = CDSApp(sys.argv[1:])
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
