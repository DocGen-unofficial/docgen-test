from source.parquet import MarkdownParquetTransformer


parquet_file_path = "C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\docgen-unofficial-docgen-test_part_0.parquet"
output_parquet_path = "C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\output.parquet"


if __name__ == "__main__":

    transformer = MarkdownParquetTransformer(parquet_file_path, output_parquet_path)
    transformer.convert_to_html()
    print(f"Markdown files converted to HTML and saved in {output_parquet_path}")