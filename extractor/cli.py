#!/usr/bin/env python3

import argparse
import logging
import sys
from typing import Optional, List

from extractor.core import DataExtractor
from extractor.utils import logger, config_loader
from extractor.utils.monitoring import start_monitoring
from extractor.version import __version__

def configure_logging(verbose: bool = False) -> None:
    """Set up logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('extractor.log'),
            logging.StreamHandler()
        ]
    )

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Company System Data Extraction Tool",
        epilog=f"Version {__version__}"
    )

    parser.add_argument(
        '--source',
        choices=['all', 'system', 'database', 'api', 'files'],
        default='all',
        help="Data sources to extract (default: all)"
    )
    parser.add_argument(
        '--output',
        type=str,
        default='./data/',
        help="Output directory path (default: ./data/)"
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help="Path to config file (default: config/config.yaml)"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Simulate extraction without saving data"
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help="Enable verbose output"
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f"%(prog)s {__version__}"
    )

    return parser.parse_args(args)

def main() -> None:
    """Entry point for CLI"""
    args = parse_args()
    
    # Initialize components
    configure_logging(args.verbose)
    logger.info("Starting System Data Extractor")
    config = config_loader.load(args.config)
    
    # Start monitoring endpoint
    start_monitoring(port=config.get('monitoring_port', 8000))
    
    try:
        extractor = DataExtractor(config)
        
        if args.dry_run:
            logger.info("DRY RUN MODE - No data will be saved")
            
        results = extractor.run(
            source=args.source,
            output_dir=args.output,
            dry_run=args.dry_run
        )
        
        logger.info(f"Extraction complete. Processed {len(results)} sources")
        sys.exit(0)
        
    except Exception as e:
        logger.critical(f"Extraction failed: {str(e)}", exc_info=args.verbose)
        sys.exit(1)

if __name__ == "__main__":
    main()