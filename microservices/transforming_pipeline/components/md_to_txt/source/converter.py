import pandas as pd
import markdown
import logging
from docutils.core import publish_parts
import asyncio


async def md_to_text(text: str) -> str:
    """
    Convert Markdown text to plain text.
    Args:
        text (str): The Markdown text to convert.
    Returns:
        str: The converted plain text.
    """
    try:
        return await asyncio.to_thread(markdown.markdown, text)
    except Exception as e:
        logging.error(f"Error converting Markdown to text: {e}")
        return text

async def rst_to_text(text: str) -> str:
    """
    Convert reStructuredText to plain text.
    Args:
        text (str): The reStructuredText to convert.
    Returns:
        str: The converted plain text.
    """
    try:
        parts = await asyncio.to_thread(publish_parts, text, writer_name='html')
        return parts['html_body']
    except Exception as e:
        logging.error(f"Error converting reStructuredText to text: {e}")
        return text

class FileConverter:
    def __init__(self, input_df: pd.DataFrame, extensions: list = None):
        self.input_df = input_df
        self.extensions = extensions

    async def file_to_text(self) -> pd.DataFrame:
        function_map = {
            '.md': md_to_text,
            '.rst': rst_to_text
        }
        dfs = []
        for ext in self.extensions:
            func = function_map.get(ext)
            if func:
                mask = self.input_df['name'].str.endswith(ext)
                filtered_df = self.input_df[mask].copy()
                if not filtered_df.empty:
                    filtered_df['content'] = await asyncio.gather(
                        *[func(text) for text in filtered_df['content']])
                    dfs.append(filtered_df)
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        else:
            return pd.DataFrame()
