import pandas as pd
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)
logger = logging.getLogger("excel_reader")

TARGET_COLUMNS = [
    "Transaction type",
    "Primary / Addon Customer Name",
    "DATE",
    "Description",
    "AMT",
    "Debit / Credit",
]


def find_column_indices(df: pd.DataFrame, header_row: int) -> tuple:
    """Auto-detect column indices by scanning the header row."""
    header_vals = df.iloc[header_row].astype(str)
    
    indices = {}
    
    for col_idx, val in enumerate(header_vals):
        val_lower = str(val).lower().strip()
        
        if "transaction" in val_lower and "type" in val_lower:
            indices["txn_type"] = col_idx
        elif "primary" in val_lower or "addon" in val_lower or "customer" in val_lower:
            indices["name"] = col_idx
        elif "date" in val_lower:
            indices["date"] = col_idx
        elif "description" in val_lower or "merchant" in val_lower:
            indices["desc"] = col_idx
        elif "amt" in val_lower or "amount" in val_lower:
            indices["amt"] = col_idx
        elif "debit" in val_lower or "credit" in val_lower:
            indices["debit"] = col_idx
    
    return (
        indices.get("txn_type"),
        indices.get("name"),
        indices.get("date"),
        indices.get("desc"),
        indices.get("amt"),
        indices.get("debit"),
    )


def load_transactions(filename: str) -> pd.DataFrame:
    """Load and clean transactions from a single Excel file."""
    base_path = Path.cwd()
    file_path = base_path / "fin_guard_ai" / "resources" / filename

    try:
        df = pd.read_excel(file_path, header=None)

        # Find the header row (contains "Transaction type")
        header_row_idx = df.index[
            df.apply(
                lambda r: r.astype(str)
                .str.contains("Transaction type", case=False, na=False)
                .any(),
                axis=1,
            )
        ]
        
        if len(header_row_idx) == 0:
            logger.warning(f"No 'Transaction type' header found in {filename}")
            return pd.DataFrame()

        header_row = header_row_idx[0]
        logger.info(f"  Header row index: {header_row}")

        # Auto-detect column indices for this specific file
        col_indices = find_column_indices(df, header_row)
        txn_type_idx, name_idx, date_idx, desc_idx, amt_idx, debit_idx = col_indices
        
        logger.info(f"  Detected indices: txn_type={txn_type_idx}, name={name_idx}, date={date_idx}, desc={desc_idx}, amt={amt_idx}, debit={debit_idx}")

        # Validate that all required columns were found
        if None in col_indices:
            logger.warning(f"  Could not find all required columns in {filename}")
            logger.info(f"  Available columns: {df.iloc[header_row].tolist()}")
            return pd.DataFrame()

        # Extract data starting from next row
        data_block = df.iloc[header_row + 1 :].copy()

        # Select only the detected columns (USING AUTO-DETECTED INDICES)
        data_block = data_block.iloc[:, [txn_type_idx, name_idx, date_idx, desc_idx, amt_idx, debit_idx]]
        data_block.columns = TARGET_COLUMNS
        data_block = data_block.dropna(how="all")

        # Keep only valid transaction rows
        data_block = data_block[
            data_block["Transaction type"].notna() & data_block["AMT"].notna()
        ]

        # Normalize Debit / Credit values
        data_block["Debit / Credit"] = data_block["Debit / Credit"].fillna("Debited")
        data_block["Debit / Credit"] = data_block["Debit / Credit"].replace(
            {"Cr": "Credited", "DR": "Debited", "Dr": "Debited"}
        )

        return data_block

    except Exception as e:
        logger.error(f"Error processing {filename}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return pd.DataFrame()


def process_all_excel_files():
    """Read all Excel files from resources directory and save as CSVs."""
    base_path = Path.cwd()
    resources_dir = base_path / "fin_guard_ai" / "resources"

    if not resources_dir.exists():
        logger.error(f"Resources directory not found: {resources_dir}")
        return

    # Find all Excel files
    excel_files = list(resources_dir.glob("*.xls")) + list(resources_dir.glob("*.xlsx"))
    
    if not excel_files:
        logger.warning("No Excel files found in resources directory")
        return

    logger.info(f"Found {len(excel_files)} Excel files to process\n")

    processed_count = 0
    failed_count = 0
    
    for excel_file in sorted(excel_files):
        logger.info(f"Processing: {excel_file.name}")

        df = load_transactions(excel_file.name)

        if df.empty:
            logger.warning(f"  ✗ No transactions extracted\n")
            failed_count += 1
            continue

        csv_name = excel_file.stem + "_transactions.csv"
        csv_path = resources_dir / csv_name

        df.to_csv(csv_path, index=False)
        logger.info(f"  ✓ Wrote {len(df)} transactions to {csv_path}\n")
        processed_count += 1

    logger.info(f"\n{'='*60}")
    logger.info(f"Processing complete!")
    logger.info(f"  ✓ Successfully processed: {processed_count} files")
    logger.info(f"  ✗ Failed: {failed_count} files")
    logger.info(f"{'='*60}")

def merge_all_csv_to_one():
    """Merge all individual CSV transaction files into a single CSV."""
    base_path = Path.cwd()
    resources_dir = base_path / "fin_guard_ai" / "resources"
    merged_csv_path = resources_dir / "all_transactions_merged.csv"

    csv_files = list(resources_dir.glob("*_transactions.csv"))
    
    if not csv_files:
        logger.warning("No individual transaction CSV files found to merge")
        return

    merged_df = pd.DataFrame()

    for csv_file in sorted(csv_files):
        logger.info(f"Merging: {csv_file.name}")
        df = pd.read_csv(csv_file)
        merged_df = pd.concat([merged_df, df], ignore_index=True)

    merged_df.to_csv(merged_csv_path, index=False)
    logger.info(f"\n✓ Merged {len(csv_files)} files into {merged_csv_path} with {len(merged_df)} total transactions")

if __name__ == "__main__":
    # process_all_excel_files()
    merge_all_csv_to_one()
