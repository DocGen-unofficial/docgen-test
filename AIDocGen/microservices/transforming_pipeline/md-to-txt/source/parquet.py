import pandas as pd
import markdown


def convert_to_html(md_text):
    """
    Convert Markdown text to HTML.
    Args:
        md_text (str): The Markdown text to convert.
    Returns:
        str: The converted HTML text.
    """
    html = markdown.markdown(md_text)
    return html


class MarkdownParquetTransformer:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def load_parquet(self):
        """
        Load the Parquet file into a DataFrame.
        Returns:
            dataframe: the loaded DataFrame.
        """
        return pd.read_parquet(self.input_path)

    def convert_to_html(self):
        """
        Transform the loaded DataFrame by converting Markdown content to HTML.
        """
        df = self.load_parquet()
        
        md_files = df[df['name'].str.endswith(('.md', '.markdown'))]

        md_files.loc[:, 'content'] = md_files.loc[:, 'content'].apply(convert_to_html)

        md_files.to_parquet(self.output_path)