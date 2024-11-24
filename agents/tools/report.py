from langchain_core.tools import StructuredTool
from pydantic.v1 import BaseModel

import os

def write_report(filename: str, html: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # write report in the directory above the current directory
    with open(os.path.join(current_dir, "..", filename), "w") as f:
        f.write(html)
    return f"Report written to {filename}"

class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str

write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write an HTML report to a file. Use this tool whenever asked to write a report.",
    func=write_report,
    args_schema=WriteReportArgsSchema
)