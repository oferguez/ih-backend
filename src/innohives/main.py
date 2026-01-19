from __future__ import annotations

from .analyse_trends import run_analysis
from .server import create_app
from .setup import build_arg_parser, configure_logging


def main() -> None:
    args = build_arg_parser().parse_args()
    logger = configure_logging(args.log_level)
    logger.info("Config: %s", vars(args))

    if args.analyse:
        run_analysis(args)

    app = create_app(database_path=args.database)
    logger.info("Listening on http://localhost:3100")
    app.run(host="127.0.0.1", port=3100)


if __name__ == "__main__":
    main()
