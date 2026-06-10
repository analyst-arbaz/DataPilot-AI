import logging
from utils.llm import llm

logger = logging.getLogger(__name__)


def business_analysis(prompt, tables_info, df=None):
    context = ""

    if df is not None:
        try:
            context += f"\nSample rows:\n{df.head().to_string()}\n"
            context += f"\nStats:\n{df.describe().to_string()}\n"
        except Exception as e:
            logger.warning(f"Could not build data context: {e}")

    full_prompt = f"""You are a senior business analyst reviewing a dataset.

Schema:
{tables_info}
{context}

Question: {prompt}

Give a thorough analysis covering:

## Key Insights
What stands out in this data?

## Risks
What problems or warning signs do you see?

## Opportunities
Where is there room to grow or improve?

## Recommended Actions
What should the business actually do next?

## Summary
Two or three sentences for a busy executive.

Be specific — mention actual column names and numbers where relevant.
"""

    response = llm.invoke(full_prompt)
    return response.content