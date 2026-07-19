from tools.utility.company_resolver import resolve_company
from tools.financial.stock_tool import get_stock_data
from tools.financial.technical_tool import technical_analysis
from tools.market.news_tool import get_company_news

TOOLS = [
    resolve_company,
    get_stock_data,
    technical_analysis,
    get_company_news,
]

TOOL_MAP = {tool.name: tool for tool in TOOLS}