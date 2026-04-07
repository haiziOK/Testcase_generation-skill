"""
Test case generator using LLM.
"""
import json
import logging
from typing import List, Dict, Any
from llm_client import LLMClient

logger = logging.getLogger(__name__)

class TestCaseGenerator:
    """Generate test cases from requirements using LLM."""

    def __init__(self, llm_client: LLMClient = None):
        self.llm_client = llm_client or LLMClient.get_default_client()

    def generate_test_cases(self, requirements: List[Dict], max_cases_per_req: int = 5) -> List[Dict]:
        """Generate test cases from a list of requirements."""
        all_test_cases = []

        for req in requirements:
            req_id = req.get("id", "unknown")
            req_text = req.get("text", "")
            req_type = req.get("type", "functional")

            logger.info(f"Generating test cases for requirement: {req_id}")

            # Generate test cases for this requirement
            test_cases = self._generate_for_requirement(req_id, req_text, req_type, max_cases_per_req)
            all_test_cases.extend(test_cases)

        logger.info(f"Generated {len(all_test_cases)} total test cases")
        return all_test_cases

    def _generate_for_requirement(self, req_id: str, req_text: str, req_type: str, max_cases: int) -> List[Dict]:
        """Generate test cases for a single requirement."""
        prompt = self._build_prompt(req_text, req_type, max_cases)
        system_prompt = """你是一名软件测试专家。根据需求生成全面的测试用例。
        输出必须是有效的JSON数组。每个测试用例应包含：
        - id: 唯一的测试用例标识符（字符串）
        - title: 简短的描述性标题（字符串）
        - description: 详细描述测试验证的内容（字符串）
        - steps: 测试步骤数组，每个步骤为字符串
        - expected_result: 执行步骤后的预期结果（字符串）
        - priority: "high"（高）、"medium"（中）或"low"（低）
        - requirement_id: 需求ID的引用（字符串）

        示例格式：
        [
          {
            "id": "TC001",
            "title": "验证使用有效凭据登录",
            "description": "测试用户可以使用正确的用户名和密码登录",
            "steps": ["导航到登录页面", "输入有效的用户名", "输入有效的密码", "点击登录按钮"],
            "expected_result": "用户成功登录并重定向到仪表板",
            "priority": "high",
            "requirement_id": "REQ001"
          }
        ]

        生成多样化的测试用例，涵盖正向、负向和边界场景。所有输出内容必须使用中文。"""
        try:
            response = self.llm_client.chat(prompt, system=system_prompt, temperature=0.3)
            test_cases = self._parse_response(response)
            # Add requirement ID to each test case
            for tc in test_cases:
                tc["requirement_id"] = req_id
            return test_cases
        except Exception as e:
            logger.error(f"Failed to generate test cases for requirement {req_id}: {e}")
            return []

    def _build_prompt(self, requirement_text: str, requirement_type: str, max_cases: int) -> str:
        """Build a prompt for test case generation."""
        return f"""为以下{requirement_type}需求生成{max_cases}个测试用例：

需求：{requirement_text}

要求：
1. 创建验证需求是否满足的测试用例
2. 包括正向测试（正常操作）、负向测试（错误条件）和边界案例
3. 使测试步骤清晰且可操作
4. 分配适当的优先级（关键功能为高，重要功能为中，可有可无的功能为低）
5. 每个测试用例应独立且自包含

只输出JSON数组，不要额外文本。所有测试用例内容使用中文。"""

    def _parse_response(self, response: str) -> List[Dict]:
        """Parse LLM response into test case objects."""
        try:
            # Extract JSON from response (in case there's extra text)
            # Find first '[' and last ']'
            start = response.find('[')
            end = response.rfind(']') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                if isinstance(data, list):
                    return data
                else:
                    logger.warning(f"Response is not a JSON array: {response[:200]}")
                    return []
            else:
                logger.warning(f"No JSON array found in response: {response[:200]}")
                return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response: {response}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {e}")
            return []

    def generate_from_document(self, document_path: str, max_cases_per_req: int = 5) -> List[Dict]:
        """Generate test cases directly from a document file."""
        from document_parser import DocumentParser

        parser = DocumentParser()
        requirements = parser.parse_and_extract(document_path)
        test_cases = self.generate_test_cases(requirements, max_cases_per_req)
        return test_cases