/**
 * 体质评分算法测试（前端版本）
 * Constitution Scoring Algorithm Tests (Frontend)
 *
 * 可在浏览器控制台直接运行，验证核心算法正确性
 */

// ============== 体质评分器类 ==============

class ConstitutionScorer {
  constructor() {
    // 分数转换系数
    this.SCORE_CONVERT_FACTOR = 2.5;
    // 判定阈值
    this.THRESHOLD_PRIMARY = 40;      // 主要体质阈值
    this.THRESHOLD_SECONDARY = 30;    // 次要体质阈值
    this.THRESHOLD_PEACE = 60;        // 平和质阈值

    // 体质类型映射
    this.CONSTITUTION_TYPES = {
      "peace": "平和质",
      "qi_deficiency": "气虚质",
      "yang_deficiency": "阳虚质",
      "yin_deficiency": "阴虚质",
      "phlegm_damp": "痰湿质",
      "damp_heat": "湿热质",
      "blood_stasis": "血瘀质",
      "qi_depression": "气郁质",
      "special": "特禀质"
    };

    // 题目到体质类型的映射
    this.QUESTION_TYPE_MAPPING = {
      1: "peace", 2: "peace", 3: "peace", 4: "peace",
      5: "qi_deficiency", 6: "qi_deficiency", 7: "qi_deficiency", 8: "qi_deficiency",
      9: "yang_deficiency", 10: "yang_deficiency", 11: "yang_deficiency", 12: "yang_deficiency",
      13: "yin_deficiency", 14: "yin_deficiency", 15: "yin_deficiency", 16: "yin_deficiency",
      17: "phlegm_damp", 18: "phlegm_damp", 19: "phlegm_damp",
      20: "damp_heat", 21: "damp_heat", 22: "damp_heat",
      23: "blood_stasis", 24: "blood_stasis", 25: "blood_stasis",
      26: "qi_depression", 27: "qi_depression", 28: "qi_depression",
      29: "special", 30: "special"
    };
  }

  /**
   * 计算原始分数
   */
  calculateScores(answers) {
    if (answers.length !== 30) {
      throw new Error(`Expected 30 answers, got ${answers.length}`);
    }

    // 验证答案范围
    for (let answer of answers) {
      if (answer < 1 || answer > 5) {
        throw new Error(`Answer must be between 1 and 5, got ${answer}`);
      }
    }

    // 初始化各维度分数
    const rawScores = {
      peace: 0,
      qi_deficiency: 0,
      yang_deficiency: 0,
      yin_deficiency: 0,
      phlegm_damp: 0,
      damp_heat: 0,
      blood_stasis: 0,
      qi_depression: 0,
      special: 0
    };

    // 按题目归属累加分数
    for (let i = 0; i < answers.length; i++) {
      const questionNum = i + 1;
      const constitutionType = this.QUESTION_TYPE_MAPPING[questionNum];
      if (constitutionType) {
        rawScores[constitutionType] += answers[i];
      }
    }

    return rawScores;
  }

  /**
   * 转换为百分制
   */
  convertToPercentage(rawScores) {
    const percentageScores = {};
    for (let type in rawScores) {
      percentageScores[type] = Math.min(100, rawScores[type] * this.SCORE_CONVERT_FACTOR);
    }
    return percentageScores;
  }

  /**
   * 判定体质类型
   */
  determineConstitution(scores) {
    let resultTypes = [];
    let maxScore = 0;
    let primaryType = "";

    // 找出所有达到阈值的体质
    for (let type in scores) {
      if (scores[type] >= this.THRESHOLD_SECONDARY) {
        resultTypes.push({
          type: type,
          name: this.CONSTITUTION_TYPES[type],
          score: Math.round(scores[type] * 100) / 100
        });
        if (scores[type] > maxScore) {
          maxScore = scores[type];
          primaryType = type;
        }
      }
    }

    // 平和质判定
    if (scores.peace >= this.THRESHOLD_PEACE) {
      const othersBelowThreshold = Object.keys(scores)
        .filter(type => type !== "peace")
        .every(type => scores[type] < 40);

      if (othersBelowThreshold) {
        return {
          primary_constitution: "peace",
          primary_constitution_name: "平和质",
          secondary_constitutions: [],
          scores: scores
        };
      }
    }

    // 如果没有体质达到阈值，选择分数最高的
    if (resultTypes.length === 0) {
      for (let type in scores) {
        if (scores[type] > maxScore) {
          maxScore = scores[type];
          primaryType = type;
        }
      }
      resultTypes.push({
        type: primaryType,
        name: this.CONSTITUTION_TYPES[primaryType] || primaryType,
        score: Math.round(maxScore * 100) / 100
      });
    }

    // 确定次要体质
    const secondaryConstitutions = resultTypes
      .filter(rt => rt.type !== primaryType)
      .sort((a, b) => b.score - a.score)
      .slice(0, 3);

    return {
      primary_constitution: primaryType,
      primary_constitution_name: this.CONSTITUTION_TYPES[primaryType] || primaryType,
      secondary_constitutions: secondaryConstitutions,
      scores: scores
    };
  }

  /**
   * 完整分析流程
   */
  analyze(answers) {
    const rawScores = this.calculateScores(answers);
    const percentageScores = this.convertToPercentage(rawScores);
    return this.determineConstitution(percentageScores);
  }
}

// ============== 测试框架 ==============

class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  assertEqual(actual, expected, message = "") {
    if (actual !== expected) {
      throw new Error(
        `Assertion failed: ${message}\n` +
        `  Expected: ${expected}\n` +
        `  Actual: ${actual}`
      );
    }
  }

  assertTrue(value, message = "") {
    if (!value) {
      throw new Error(`Assertion failed: ${message}\n  Expected: true\n  Actual: false`);
    }
  }

  assertGreaterThan(actual, expected, message = "") {
    if (actual <= expected) {
      throw new Error(
        `Assertion failed: ${message}\n` +
        `  Expected: > ${expected}\n` +
        `  Actual: ${actual}`
      );
    }
  }

  async run() {
    console.log("\n🧪 开始运行前端测试...\n");

    for (let test of this.tests) {
      try {
        await test.fn();
        this.passed++;
        console.log(`✅ PASS: ${test.name}`);
      } catch (error) {
        this.failed++;
        console.error(`❌ FAIL: ${test.name}`);
        console.error(`   ${error.message}`);
      }
    }

    console.log(`\n📊 测试结果: ${this.passed} 通过, ${this.failed} 失败\n`);
    return this.failed === 0;
  }
}

// ============== 测试用例 ==============

const runner = new TestRunner();
const scorer = new ConstitutionScorer();

// 测试1: 全选"没有"(1分)
runner.test("全选1分 - 各体质原始分数正确", () => {
  const answers = Array(30).fill(1);
  const scores = scorer.calculateScores(answers);

  runner.assertEqual(scores.peace, 4, "平和质分数");
  runner.assertEqual(scores.qi_deficiency, 4, "气虚质分数");
  runner.assertEqual(scores.yang_deficiency, 4, "阳虚质分数");
  runner.assertEqual(scores.yin_deficiency, 4, "阴虚质分数");
  runner.assertEqual(scores.phlegm_damp, 3, "痰湿质分数");
  runner.assertEqual(scores.damp_heat, 3, "湿热质分数");
  runner.assertEqual(scores.blood_stasis, 3, "血瘀质分数");
  runner.assertEqual(scores.qi_depression, 3, "气郁质分数");
  runner.assertEqual(scores.special, 2, "特禀质分数");
});

// 测试2: 全选"总是"(5分)
runner.test("全选5分 - 各体质原始分数正确", () => {
  const answers = Array(30).fill(5);
  const scores = scorer.calculateScores(answers);

  runner.assertEqual(scores.peace, 20, "平和质分数");
  runner.assertEqual(scores.qi_deficiency, 20, "气虚质分数");
  runner.assertEqual(scores.special, 10, "特禀质分数(只有2题)");
});

// 测试3: 百分制转换
runner.test("百分制转换 - 计算正确", () => {
  const rawScores = { peace: 16, qi_deficiency: 8, yang_deficiency: 12 };
  const percentage = scorer.convertToPercentage(rawScores);

  runner.assertEqual(percentage.peace, 40, "平和质百分制");
  runner.assertEqual(percentage.qi_deficiency, 20, "气虚质百分制");
  runner.assertEqual(percentage.yang_deficiency, 30, "阳虚质百分制");
});

// 测试4: 百分制最大值限制
runner.test("百分制转换 - 最大值不超过100", () => {
  const rawScores = { peace: 50 }; // 超过100的原始分
  const percentage = scorer.convertToPercentage(rawScores);

  runner.assertEqual(percentage.peace, 100, "应该限制为100");
});

// 测试5: 平和质判定
runner.test("平和质判定 - 60分且其他<40", () => {
  const scores = {
    peace: 70,
    qi_deficiency: 30,
    yang_deficiency: 25,
    yin_deficiency: 20,
    phlegm_damp: 20,
    damp_heat: 20,
    blood_stasis: 20,
    qi_depression: 20,
    special: 15
  };

  const result = scorer.determineConstitution(scores);
  runner.assertEqual(result.primary_constitution, "peace", "应判定为平和质");
  runner.assertEqual(result.secondary_constitutions.length, 0, "无次要体质");
});

// 测试6: 气虚质判定
runner.test("气虚质判定 - 分数最高", () => {
  const scores = {
    peace: 30,
    qi_deficiency: 50,
    yang_deficiency: 35,
    yin_deficiency: 25,
    phlegm_damp: 20,
    damp_heat: 20,
    blood_stasis: 20,
    qi_depression: 20,
    special: 15
  };

  const result = scorer.determineConstitution(scores);
  runner.assertEqual(result.primary_constitution, "qi_deficiency", "应判定为气虚质");
});

// 测试7: 阳虚质判定
runner.test("阳虚质判定 - 手脚发凉典型症状", () => {
  const answers = [
    3, 3, 3, 3,  // 平和质
    3, 3, 3, 3,  // 气虚质
    5, 5, 5, 5,  // 阳虚质 - 明显症状
    3, 3, 3, 3,  // 阴虚质
    3, 3, 3,     // 痰湿质
    3, 3, 3,     // 湿热质
    3, 3, 3,     // 血瘀质
    3, 3, 3,     // 气郁质
    3, 3         // 特禀质
  ];

  const result = scorer.analyze(answers);
  runner.assertEqual(result.primary_constitution, "yang_deficiency", "应判定为阳虚质");
  runner.assertGreaterThan(result.scores.yang_deficiency, 40, "阳虚质分数应>40");
});

// 测试8: 阴虚质判定
runner.test("阴虚质判定 - 口干咽燥典型症状", () => {
  const answers = [
    3, 3, 3, 3,  // 平和质
    3, 3, 3, 3,  // 气虚质
    3, 3, 3, 3,  // 阳虚质
    5, 5, 5, 5,  // 阴虚质 - 明显症状
    3, 3, 3,     // 痰湿质
    3, 3, 3,     // 湿热质
    3, 3, 3,     // 血瘀质
    3, 3, 3,     // 气郁质
    3, 3         // 特禀质
  ];

  const result = scorer.analyze(answers);
  runner.assertEqual(result.primary_constitution, "yin_deficiency", "应判定为阴虚质");
});

// 测试9: 痰湿质判定
runner.test("痰湿质判定 - 胸闷腹胀典型症状", () => {
  const answers = [
    3, 3, 3, 3,  // 平和质
    3, 3, 3, 3,  // 气虚质
    3, 3, 3, 3,  // 阳虚质
    3, 3, 3, 3,  // 阴虚质
    5, 5, 5,     // 痰湿质 - 明显症状
    3, 3, 3,     // 湿热质
    3, 3, 3,     // 血瘀质
    3, 3, 3,     // 气郁质
    3, 3         // 特禀质
  ];

  const result = scorer.analyze(answers);
  runner.assertEqual(result.primary_constitution, "phlegm_damp", "应判定为痰湿质");
});

// 测试10: 湿热质判定
runner.test("湿热质判定 - 面部油腻典型症状", () => {
  const answers = [
    3, 3, 3, 3,  // 平和质
    3, 3, 3, 3,  // 气虚质
    3, 3, 3, 3,  // 阳虚质
    3, 3, 3, 3,  // 阴虚质
    3, 3, 3,     // 痰湿质
    5, 5, 5,     // 湿热质 - 明显症状
    3, 3, 3,     // 血瘀质
    3, 3, 3,     // 气郁质
    3, 3         // 特禀质
  ];

  const result = scorer.analyze(answers);
  runner.assertEqual(result.primary_constitution, "damp_heat", "应判定为湿热质");
});

// 测试11: 血瘀质判定
runner.test("血瘀质判定 - 皮肤瘀斑典型症状", () => {
  const answers = [
    3, 3, 3, 3,  // 平和质
    3, 3, 3, 3,  // 气虚质
    3, 3, 3, 3,  // 阳虚质
    3, 3, 3, 3,  // 阴虚质
    3, 3, 3,     // 痰湿质
    3, 3, 3,     // 湿热质
    5, 5, 5,     // 血瘀质 - 明显症状
    3, 3, 3,     // 气郁质
    3, 3         // 特禀质
  ];

  const result = scorer.analyze(answers);
  runner.assertEqual(result.primary_constitution, "blood_stasis", "应判定为血瘀质");
});

// 测试12: 气郁质判定
runner.test("气郁质判定 - 情绪低沉典型症状", () => {
  const answers = [
    3, 3, 3, 3,  // 平和质
    3, 3, 3, 3,  // 气虚质
    3, 3, 3, 3,  // 阳虚质
    3, 3, 3, 3,  // 阴虚质
    3, 3, 3,     // 痰湿质
    3, 3, 3,     // 湿热质
    3, 3, 3,     // 血瘀质
    5, 5, 5,     // 气郁质 - 明显症状
    3, 3         // 特禀质
  ];

  const result = scorer.analyze(answers);
  runner.assertEqual(result.primary_constitution, "qi_depression", "应判定为气郁质");
});

// 测试13: 次要体质判定
runner.test("次要体质判定 - 气虚阳虚混合", () => {
  const scores = {
    peace: 30,
    qi_deficiency: 50,  // 主要
    yang_deficiency: 40,  // 次要
    yin_deficiency: 35,  // 次要
    phlegm_damp: 32,  // 次要
    damp_heat: 20,
    blood_stasis: 20,
    qi_depression: 20,
    special: 15
  };

  const result = scorer.determineConstitution(scores);
  runner.assertEqual(result.primary_constitution, "qi_deficiency");
  runner.assertTrue(result.secondary_constitutions.length >= 1, "应有次要体质");

  // 验证次要体质按分数降序
  for (let i = 0; i < result.secondary_constitutions.length - 1; i++) {
    runner.assertTrue(
      result.secondary_constitutions[i].score >= result.secondary_constitutions[i + 1].score,
      "次要体质应按分数降序排列"
    );
  }
});

// 测试14: 无阈值时选择最高分
runner.test("无达到阈值 - 选择分数最高", () => {
  const scores = {
    peace: 25,
    qi_deficiency: 28,  // 最高但<30
    yang_deficiency: 25,
    yin_deficiency: 22,
    phlegm_damp: 20,
    damp_heat: 20,
    blood_stasis: 20,
    qi_depression: 20,
    special: 15
  };

  const result = scorer.determineConstitution(scores);
  runner.assertEqual(result.primary_constitution, "qi_deficiency");
});

// 测试15: 答案验证 - 数量不正确
runner.test("答案验证 - 数量不正确应抛错", () => {
  try {
    scorer.calculateScores([1, 2, 3]);
    runner.assertTrue(false, "应该抛出错误");
  } catch (e) {
    runner.assertTrue(e.message.includes("Expected 30 answers"), "错误信息应正确");
  }
});

// 测试16: 答案验证 - 范围不正确
runner.test("答案验证 - 范围不正确应抛错", () => {
  try {
    scorer.calculateScores([0] * 30);
    runner.assertTrue(false, "应该抛出错误");
  } catch (e) {
    runner.assertTrue(e.message.includes("between 1 and 5"), "错误信息应正确");
  }
});

// 测试17: 典型平和质完整流程
runner.test("典型平和质 - 精力充沛面色红润", () => {
  const answers = [
    5, 1, 1, 1,  // 精力充沛、不疲乏、面色红润
    1, 1, 1, 1,
    1, 1, 1, 1,
    1, 1, 1, 1,
    1, 1, 1,
    1, 1, 1,
    1, 1, 1,
    1, 1, 1,
    1, 1
  ];

  const result = scorer.analyze(answers);
  runner.assertEqual(result.primary_constitution, "peace");
});

// 测试18: 气虚阳虚混合体质
runner.test("气虚阳虚混合 - 气阳两虚", () => {
  const answers = [
    3, 3, 4, 3,
    4, 4, 4, 4,  // 气虚
    4, 4, 4, 4,  // 阳虚
    3, 3, 3, 3,
    3, 3, 3,
    3, 3, 3,
    3, 3, 3,
    3, 3, 3,
    3, 3
  ];

  const result = scorer.analyze(answers);
  runner.assertTrue(
    result.primary_constitution === "qi_deficiency" ||
    result.primary_constitution === "yang_deficiency",
    "主要体质应为气虚或阳虚"
  );
});

// 测试19: 完整分析流程返回结构
runner.test("完整分析 - 返回结构完整", () => {
  const answers = [3] * 30;
  const result = scorer.analyze(answers);

  runner.assertTrue("primary_constitution" in result, "应有主要体质");
  runner.assertTrue("primary_constitution_name" in result, "应有体质名称");
  runner.assertTrue("scores" in result, "应有分数");
  runner.assertTrue("secondary_constitutions" in result, "应有次要体质");
});

// 测试20: 分数精度
runner.test("分数精度 - 保留两位小数", () => {
  const scores = {
    peace: 30.123456,
    qi_deficiency: 40.789
  };

  const result = scorer.determineConstitution(scores);
  const secondaryScores = result.secondary_constitutions.map(c => c.score);

  // 验证分数保留两位小数
  for (let score of secondaryScores) {
    const decimalPlaces = (score.toString().split(".")[1] || "").length;
    runner.assertTrue(decimalPlaces <= 2, "分数应保留最多2位小数");
  }
});

// ============== 运行测试 ==============

// 导出供外部使用
if (typeof module !== "undefined" && module.exports) {
  module.exports = { ConstitutionScorer, TestRunner };
}

// 如果在浏览器中直接运行
if (typeof window !== "undefined") {
  window.ConstitutionScorer = ConstitutionScorer;
  window.runConstitutionTests = () => runner.run();

  // 自动运行测试（可选）
  console.log("💡 提示: 运行 runConstitutionTests() 来执行所有测试");
}
