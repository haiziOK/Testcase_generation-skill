"""
Main entry point for Testcase_generation skill.
Provides interactive prompts and command-line interface.
"""
import os
import sys
import logging
import io
import click
from document_parser import DocumentParser
from testcase_generator import TestCaseGenerator
from excel_writer import ExcelWriter

# Fix encoding issues on Windows with GBK console
if hasattr(sys.stdout, 'buffer') and (sys.stdout.encoding is None or sys.stdout.encoding.upper() not in ('UTF-8', 'UTF8')):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass  # Keep original stdout if any error

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def interactive_prompt():
    """Interactive prompt for generating test cases."""
    print("=" * 60)
    print("测试用例生成技能")
    print("=" * 60)

    # Get design document path
    while True:
        doc_path = input("输入设计文档路径 (TXT, PDF, DOCX): ").strip()
        if not doc_path:
            print("未提供路径。退出。")
            return
        if os.path.exists(doc_path):
            break
        else:
            print(f"文件未找到: {doc_path}. 请重试。")

    # Get output path
    default_output = os.path.join(os.path.dirname(doc_path), "test_cases.xlsx")
    output_path = input(f"输入输出Excel文件路径 [默认: {default_output}]: ").strip()
    if not output_path:
        output_path = default_output

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get optional parameters
    max_cases = input("每个需求的最大测试用例数 [默认: 5]: ").strip()
    max_cases = int(max_cases) if max_cases.isdigit() else 5

    print("\n生成测试用例中...")
    print(f"输入文档: {doc_path}")
    print(f"输出文件: {output_path}")
    print(f"每个需求的最大用例数: {max_cases}")

    try:
        # Initialize components
        parser = DocumentParser()
        generator = TestCaseGenerator()
        writer = ExcelWriter()

        # Parse document and extract requirements
        print("解析文档中...")
        requirements = parser.parse_and_extract(doc_path)
        print(f"提取到 {len(requirements)} 个需求")

        # Generate test cases
        print("使用LLM生成测试用例...")
        test_cases = generator.generate_test_cases(requirements, max_cases_per_req=max_cases)
        print(f"生成 {len(test_cases)} 个测试用例")

        # Write to Excel
        print("写入Excel文件...")
        writer.write_test_cases(test_cases, output_path)
        print(f"成功创建: {output_path}")

        # Summary
        print("\n" + "=" * 60)
        print("生成完成!")
        print(f"总计测试用例: {len(test_cases)}")
        print(f"输出文件: {output_path}")
        print("=" * 60)

    except Exception as e:
        logger.error(f"Failed to generate test cases: {e}")
        print(f"错误: {e}")
        sys.exit(1)

@click.command()
@click.option('--document', '-d', required=False, help='Path to design document')
@click.option('--output', '-o', default='test_cases.xlsx', help='Output Excel file path')
@click.option('--max-cases', '-m', default=5, help='Maximum test cases per requirement')
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
def main(document, output, max_cases, interactive):
    """Generate Excel test cases from design documents."""
    if interactive or not document:
        interactive_prompt()
        return

    # Validate document exists
    if not os.path.exists(document):
        print(f"Error: Document not found: {document}")
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Generating test cases from: {document}")
    print(f"Output file: {output}")
    print(f"Max cases per requirement: {max_cases}")

    try:
        # Use the integrated writer method for simplicity
        writer = ExcelWriter()
        writer.write_from_document(document, output, max_cases_per_req=max_cases)
        print(f"Successfully created: {output}")
    except Exception as e:
        logger.error(f"Failed to generate test cases: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()