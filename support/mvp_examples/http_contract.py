"""Construct response envelopes locally without sending HTTP requests."""

# Adapted from lifan99/utility; provenance is recorded in SOURCES.json.

from dataclasses import dataclass, field
import json


RULES = {
    "invalid_request": (422, "请求字段不符合约定。"),
    "duplicate_request": (409, "相同请求标识的审核仍在执行。"),
    "capacity_exceeded": (429, "当前审核名额已满。"),
    "model_error": (502, "模型服务调用失败。"),
    "invalid_output": (502, "模型输出未通过审核契约校验。"),
    "network_timeout": (504, "模型网络操作超时。"),
    "model_timeout": (504, "本次模型调用预算耗尽。"),
    "total_timeout": (504, "本次审核总预算耗尽。"),
    "service_unavailable": (503, "服务正在关闭，暂不接受新审核。"),
}


@dataclass(frozen=True)
class Failure:
    """Teaching model for Failure."""
    code: str
    stage: str | None = None
    private_detail: str = field(default="", repr=False)


def public_error(failure):
    """Map internal failures to the published response policy."""
    status, message = RULES.get(failure.code, (500, "服务内部错误。"))
    code = failure.code if failure.code in RULES else "internal_error"
    stage = failure.stage if failure.stage in {"Analyst", "Critic", "Judge"} else None
    return status, {"code": code, "message": message, "stage": stage}


def main():
    """Run the offline demonstration and verify its behavior."""
    expected = {
        "invalid_request": 422, "duplicate_request": 409,
        "capacity_exceeded": 429, "model_error": 502,
        "invalid_output": 502, "network_timeout": 504,
        "model_timeout": 504, "total_timeout": 504,
        "service_unavailable": 503, "unexpected": 500,
    }
    for code, expected_status in expected.items():
        status, error = public_error(Failure(code, private_detail="synthetic-private-detail"))
        assert status == expected_status
        assert "synthetic-private-detail" not in json.dumps(error)


    upstream = Failure("model_error", "Critic", "upstream HTTP 429: private body")
    assert public_error(upstream)[0] == 502
    assert public_error(Failure("capacity_exceeded"))[0] == 429

    final_review = {
        "summary": "教学输入缺少验证资料，无法确认全部主张。",
        "verdict": "insufficient_evidence",
        "findings": [],
        "limitations": ["这是人工预置样例，没有执行真实审核或外部核验。"],
    }
    responses = [
        {"agent": "Analyst", "model": "fake-a", "content": "人工预置分析。"},
        {"agent": "Critic", "model": "fake-c", "content": "人工预置批评。"},
        {"agent": "Judge", "model": "fake-j", "content": json.dumps(final_review, ensure_ascii=False)},
    ]
    success = {
        "request_id": "day4-demo-001",
        "review_id": "00000000-0000-4000-8000-000000000001",
        "execution_mode": "fake",
        "status": "succeeded",
        "responses": responses,
        "stages": [
            {"agent": r["agent"], "model": r["model"], "status": "succeeded", "error_code": None,
             "raw_output": r["content"]}
            for r in responses
        ],
        "final_review": final_review,
        "error": None,
    }
    assert json.loads(success["responses"][-1]["content"]) == success["final_review"]
    print("人工构造的 201 响应体（未启动 HTTP 服务）：")
    print(json.dumps(success, ensure_ascii=False, indent=2))

    status, error = public_error(upstream)
    failure = {
        **success,
        "status": "failed",
        "responses": responses[:1],
        "stages": [
            success["stages"][0],
            {"agent": "Critic", "model": "fake-c", "status": "failed", "error_code": "model_error", "raw_output": None},
            {"agent": "Judge", "model": "fake-j", "status": "skipped", "error_code": None, "raw_output": None},
        ],
        "final_review": None,
        "error": error,
    }
    assert status == 502 and failure["final_review"] is None
    assert [r["agent"] for r in failure["responses"]] == ["Analyst"]
    assert "private body" not in json.dumps(failure)
    print("错误映射检查通过：本地满载 429，上游 429 映射为 502。")
    print("失败响应检查通过：保留 Analyst，最终报告为空，私有错误细节未输出。")


if __name__ == "__main__":
    main()
